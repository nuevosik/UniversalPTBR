#!/usr/bin/env python3
"""Inventaria os mods instalados e gera targets.json + INVENTORY.md da campanha total."""
import argparse
import json
import os
import pathlib
import re
import sys
import tempfile
import unicodedata

from extract_medieval import WORKSHOP, parse_xml, repo_index, scan_defs, scan_keyed

LOCAL = pathlib.Path.home()/'.local/share/Steam/steamapps/common/RimWorld/Mods'
REPO = pathlib.Path('Languages/PortugueseBrazilian')
BATCH_CAP = 1500
SKIP = {'1508850027': 'RimHUD coberto pelo pacote RimHUD PortugueseBrazilian'}


def mod_name_pid(mod):
    about = mod/'About'/'About.xml'
    if about.exists():
        root = parse_xml(about)
        if root is not None:
            pid = (root.findtext('packageId') or '').strip()
            return (root.findtext('name') or mod.name).strip(), pid
    return mod.name, ''


def prefix_for(name, folder):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s).strip()
    drop = {'vanilla', 'expanded', 'continued', 'fork', 'the', 'and', 'for', 'of', 'in', 'a', 'o'}
    words = [w for w in s.split() if w.lower() not in drop]
    p = ''.join(w[:1].upper()+w[1:] for w in words)[:24]
    return p or f'Mod{folder}'


def pt_own(mod):
    return any(d.name.lower().startswith('portuguese') for d in mod.rglob('*') if d.is_dir())


def scan():
    repo_def, repo_keyed = repo_index(REPO)
    rows = []
    for base in (WORKSHOP, LOCAL):
        if not base.is_dir():
            continue
        for m in sorted(os.listdir(base)):
            mod = base/m
            if not mod.is_dir():
                continue
            name, pid = mod_name_pid(mod)
            if 'Tradu' in name or 'Portuguese' in name:
                continue
            entries, _, _ = scan_defs(mod)
            keyed = scan_keyed(mod)
            if not entries and not keyed:
                continue
            md = {k for k in entries if k not in repo_def and k[1] not in repo_keyed}
            mk = {k for k in keyed if k not in repo_keyed}
            if not md and not mk:
                continue
            rows.append(dict(folderId=(m if base == WORKSHOP else ''), local=(base == LOCAL),
                             name=name, packageId=pid, missingDefs=len(md), missingKeys=len(mk),
                             total=len(md)+len(mk), ptOwn=pt_own(mod), skip=SKIP.get(m, '')))
    rows.sort(key=lambda r: -r['total'])
    return rows


def build(rows):
    excluded = [r for r in rows if r['ptOwn'] or r['skip']]
    campaign = [r for r in rows if not (r['ptOwn'] or r['skip'])]
    used, batches, cur = set(), {}, []
    for r in campaign:
        p = prefix_for(r['name'], r['folderId'])
        base_p, n = p, 2
        while p in used:
            p, n = f'{base_p}{n}', n+1
        used.add(p)
        r['prefix'] = p
        if cur and sum(x['total'] for x in cur)+r['total'] > BATCH_CAP:
            batches[f'B{len(batches)+1}'] = cur
            cur = []
        cur.append(r)
    if cur:
        batches[f'B{len(batches)+1}'] = cur
    return {'generated': '2026-09-15', 'campaign': {'targets': len(campaign),
            'strings': sum(r['total'] for r in campaign)}, 'excluded': excluded, 'batches': batches}


def write_md(data, path):
    lines = ['# Inventário — Tradução Total (PT-BR)', '',
             f"Alvos: {data['campaign']['targets']} | chaves: {data['campaign']['strings']}", '',
             '| lote | folderId | packageId | mod | defs | keys | total | status |',
             '|---|---|---|---|---:|---:|---:|---|']
    for b, rows in data['batches'].items():
        for r in rows:
            lines.append(f"| {b} | {r['folderId'] or 'LOCAL'} | {r['packageId']} | {r['name']} | "
                         f"{r['missingDefs']} | {r['missingKeys']} | {r['total']} | pendente |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines)+'\n', encoding='utf-8')


def selfcheck():
    with tempfile.TemporaryDirectory() as tmp:
        mod = pathlib.Path(tmp)/'ModFake'
        (mod/'Defs').mkdir(parents=True)
        (mod/'About').mkdir()
        (mod/'About'/'About.xml').write_text(
            '<?xml version="1.0"?><ModMetaData><name>Fake Mod</name>'
            '<packageId>fake.test</packageId></ModMetaData>', encoding='utf-8')
        (mod/'Defs'/'D.xml').write_text(
            '<?xml version="1.0"?><Defs><ThingDef><defName>FakeThing</defName>'
            '<label>fake thing</label><description>has {0} and\\nline</description>'
            '</ThingDef></Defs>', encoding='utf-8')
        entries, _, _ = scan_defs(mod)
        assert ('ThingDef', 'FakeThing.label') in entries, entries
        assert entries[('ThingDef', 'FakeThing.description')] == 'has {0} and\\nline'
        assert prefix_for('Vanilla Factions Expanded - Fake Edition', '1') == 'FactionsFakeEdition', \
            prefix_for('Vanilla Factions Expanded - Fake Edition', '1')
    print('selfcheck OK')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json', metavar='PATH', default='tools/targets.json')
    ap.add_argument('--md', metavar='PATH', default='docs/traducao-total/INVENTORY.md')
    ap.add_argument('--selfcheck', action='store_true')
    args = ap.parse_args(argv)
    if args.selfcheck:
        selfcheck()
        return 0
    data = build(scan())
    pathlib.Path(args.json).write_text(json.dumps(data, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    write_md(data, pathlib.Path(args.md))
    print(f"alvos {data['campaign']['targets']} | chaves {data['campaign']['strings']} | "
          f"lotes {len(data['batches'])} | excluídos {len(data['excluded'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
