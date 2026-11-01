#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import sys

from extract_medieval import (MODSCONFIG, REPO_LANG, WORKSHOP, XML_NAME, active_packages,
                              escape, parse_xml, repo_index, scan_defs, scan_keyed)

TARGETS = pathlib.Path(__file__).with_name('targets.json')
ACTIVE = None


def active_set():
    global ACTIVE
    if ACTIVE is None:
        ACTIVE = active_packages()
    return ACTIVE


def load_targets(only_active=True):
    data = json.loads(TARGETS.read_text(encoding='utf-8'))
    rows = [r for batch in data.get('batches', {}).values() for r in batch]
    if only_active:
        act = active_set()
        rows = [r for r in rows if not act or r['packageId'].lower() in act]
    return rows


def mod_dir(row):
    if row.get('folderId'):
        return WORKSHOP / row['folderId']
    return pathlib.Path(row.get('path', ''))


def collect(row, repo_def, repo_keyed, emitted):
    mod = mod_dir(row)
    defs, keyed = {}, []
    if not mod.is_dir():
        return defs, keyed
    entries, _, _ = scan_defs(mod)
    for (dtype, key), value in entries.items():
        if (dtype, key) in repo_def or key in repo_keyed or (dtype, key) in emitted:
            continue
        if not XML_NAME.fullmatch(key):
            continue
        defs.setdefault(dtype, {})[key] = value
        emitted.add((dtype, key))
    for key, value in scan_keyed(mod).items():
        if not value.strip() or key in repo_keyed or ('Keyed', key) in emitted:
            continue
        if not XML_NAME.fullmatch(key):
            continue
        keyed.append([key, value])
        emitted.add(('Keyed', key))
    return defs, keyed


def chunk_groups(defs, keyed, size, budget):
    items = []
    for dtype, pairs in defs.items():
        items.extend(('defs', dtype, key, value) for key, value in sorted(pairs.items()))
    items.extend(('keyed', '', key, value) for key, value in keyed)
    chunks, cur, chars = [], [], 0
    for item in items:
        weight = len(json.dumps(item[2:], ensure_ascii=False))
        if cur and (len(cur) >= size or chars + weight > budget):
            chunks.append(cur)
            cur, chars = [], 0
        cur.append(item)
        chars += weight
    if cur:
        chunks.append(cur)
    out = {}
    for i, part in enumerate(chunks, 1):
        defs_part, keyed_part = {}, {}
        for kind, dtype, key, value in part:
            if kind == 'defs':
                defs_part.setdefault(dtype, {})[key] = value
            else:
                keyed_part[key] = value
        out[f'part_{i:03d}.json'] = {'defs': defs_part, 'keyed': keyed_part}
    return out


def cmd_extract(args):
    out = pathlib.Path(args.out)
    repo_def, repo_keyed = repo_index(pathlib.Path(args.repo))
    emitted = set()
    total = 0
    for row in load_targets(not args.include_disabled):
        defs, keyed = collect(row, repo_def, repo_keyed, emitted)
        count = sum(len(v) for v in defs.values()) + len(keyed)
        if not count:
            continue
        base = out / row['folderId']
        chunks = base / 'chunks'
        tr = base / 'tr'
        chunks.mkdir(parents=True, exist_ok=True)
        tr.mkdir(parents=True, exist_ok=True)
        (base / 'meta.json').write_text(json.dumps(
            {k: row.get(k) for k in ('folderId', 'name', 'packageId', 'prefix')},
            ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        (base / 'defs.json').write_text(json.dumps(defs, ensure_ascii=False, indent=1) + '\n',
                                        encoding='utf-8')
        (base / 'keyed.json').write_text(json.dumps(keyed, ensure_ascii=False, indent=1) + '\n',
                                         encoding='utf-8')
        for name, payload in chunk_groups(defs, keyed, args.chunk, args.budget).items():
            (chunks / name).write_text(json.dumps(payload, ensure_ascii=False, indent=1) + '\n',
                                       encoding='utf-8')
        total += count
        print(f"{row['prefix']:<24} {count:>5} strings  {row['name'][:40]}")
    print(f'total {total} strings em {out}')
    return 0


def _read_json(path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return default


def clean(value):
    for src, dst in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")):
        value = value.replace(src, dst)
    value = value.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n')
    return re.sub(r'[ \t]+', ' ', value).strip()


MARKUP = re.compile(r'</?(?:color|b|i|size|material|shader|a)(?:=[^>]*)?>')


def write_language_file(path, pairs):
    existing = []
    if path.exists():
        root = parse_xml(path)
        if root is not None:
            existing = [(el.tag, el.text or '') for el in root if el.tag != 'LanguageData']
    have = {key for key, _ in existing}
    merged = existing + [pair for pair in pairs if pair[0] not in have and pair[1]]
    valid = [(k, v) for k, v in merged if XML_NAME.fullmatch(k)]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n<LanguageData>\n')
        for key, value in valid:
            fh.write(f'  <{key}>{escape(value)}</{key}>\n')
        fh.write('</LanguageData>\n')
    return len(pairs)


def cmd_assemble(args):
    out = pathlib.Path(args.out)
    repo = pathlib.Path(args.repo)
    repo_def, repo_keyed = repo_index(repo)
    written = {}
    for meta_path in sorted(out.glob('*/meta.json')):
        base = meta_path.parent
        meta = _read_json(meta_path, {})
        prefix = meta.get('prefix') or base.name
        defs = _read_json(base / 'defs.json', {})
        keyed = dict(_read_json(base / 'keyed.json', []))
        files = {}
        unknown = 0
        for tr_path in sorted((base / 'tr').glob('*.json')):
            payload = _read_json(tr_path, {})
            for dtype, pairs in (payload.get('defs') or {}).items():
                for key, value in pairs.items():
                    if key in defs.get(dtype, {}) and value.strip():
                        files.setdefault(('DefInjected', dtype), {})[key] = clean(value)
                    else:
                        unknown += 1
            for key, value in (payload.get('keyed') or {}).items():
                if key in keyed and value.strip():
                    files.setdefault(('Keyed', ''), {})[key] = clean(value)
                else:
                    unknown += 1
        for (kind, dtype), pairs in sorted(files.items()):
            if kind == 'Keyed':
                path = repo / 'Keyed' / f'{prefix}_Keys.xml'
            else:
                path = repo / 'DefInjected' / dtype / f'{prefix}_{dtype}.xml'
            added = write_language_file(path, sorted(pairs.items()))
            written[base.name] = written.get(base.name, 0) + added
        if unknown:
            print(f'aviso: {prefix}: {unknown} chaves fora do alvo ignoradas', file=sys.stderr)
    print(f'arquivos gravados para {len(written)} mods | strings {sum(written.values())}')
    return 0


PLACEHOLDER = re.compile(r'\{[^}]+\}')
NEWLINE = re.compile(r'\\n')


def token_mismatch(src, value):
    if sorted(PLACEHOLDER.findall(src)) != sorted(PLACEHOLDER.findall(value)):
        return True
    if src.count('<color') != value.count('<color') or src.count('</color>') != value.count('</color>'):
        return True
    if src.count('\\n') != value.count('\\n') + value.count('\n'):
        return True
    return False


def video_problems(src, value):
    return (not value.strip()
            or sorted(PLACEHOLDER.findall(src)) != sorted(PLACEHOLDER.findall(value))
            or src.count('<color') != value.count('<color')
            or src.count('</color>') != value.count('</color>')
            or src.count('\\n') != value.count('\\n') + value.count('\n'))


def cmd_check(args):
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    problems = {}
    total = 0
    done = 0
    for chunk_path in sorted(out.glob('*/chunks/*.json')):
        tr_path = chunk_path.parent.parent / 'tr' / chunk_path.name
        chunk = _read_json(chunk_path, {})
        tr = _read_json(tr_path, {}) if tr_path.exists() else {}
        items = []
        for dtype, pairs in (chunk.get('defs') or {}).items():
            for key, src in pairs.items():
                total += 1
                value = ((tr.get('defs') or {}).get(dtype) or {}).get(key, '')
                if video_problems(src, value):
                    items.append(['defs', dtype, key, src])
                else:
                    done += 1
        for key, src in (chunk.get('keyed') or {}).items():
            total += 1
            value = (tr.get('keyed') or {}).get(key, '')
            if video_problems(src, value):
                items.append(['keyed', '', key, src])
            else:
                done += 1
        if items:
            problems[str(chunk_path)] = items
    (out / '_problems.json').write_text(json.dumps(problems, ensure_ascii=False, indent=1) + '\n',
                                         encoding='utf-8')
    print(f'total {total} | ok {done} | pendencias {total - done} em {len(problems)} chunks')
    return 0 if not problems else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='work/campaign')
    ap.add_argument('--repo', default=str(REPO_LANG))
    sub = ap.add_subparsers(dest='cmd', required=True)
    ex = sub.add_parser('extract')
    ex.add_argument('--chunk', type=int, default=200)
    ex.add_argument('--budget', type=int, default=9000)
    ex.add_argument('--include-disabled', action='store_true')
    sub.add_parser('assemble')
    sub.add_parser('check')
    args = ap.parse_args(argv)
    return {'extract': cmd_extract, 'assemble': cmd_assemble, 'check': cmd_check}[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())
