#!/usr/bin/env python3
"""Valida alvos DefInjected (ou Keyed) contra os Defs do mod fonte.

Para cada chave `defName.campo` do alvo compara o valor com o valor em ingles do
mod fonte e acusa: chave órfã, valor vazio, placeholder divergente e XML
inválido. Exit 0 = OK, 1 = falhas. Mesmo --prefix/--batch do extrator.
"""
import argparse
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter

from extract_medieval import (BATCHES, MODS, REPO_LANG, WORKSHOP, parse_xml, resolve_mod, scan_defs,
                             load_targets, version_of)

PLACEHOLDER = re.compile(r'\{[^}]+\}')
SUBSYMBOL = re.compile(r'\{([^}_}]+)_[^}]+\}')
COLOR_TAG = re.compile(r'</?color[^>]*>')
BRACKET_TOKEN = re.compile(r'\[[^\]]+\]')
GAME_TOKEN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
NEWLINE = re.compile(r'\\n|\n')


def token_problems(value, src, bracket=True):
    """{...}/<color> exatos; [...] não pode inventar nem repetir token do EN
    (o PT-BR reescreve [PAWN_possessive] como seu/sua — prática do pacote oficial,
    que não usa o token em nenhuma linha traduzida)."""
    def base_placeholders(text):
        return Counter(SUBSYMBOL.sub(r'{\1}', token) for token in PLACEHOLDER.findall(text))

    if base_placeholders(value) != base_placeholders(src):
        return True
    if Counter(COLOR_TAG.findall(value)) != Counter(COLOR_TAG.findall(src)):
        return True
    if bracket:
        extra = Counter(BRACKET_TOKEN.findall(value)) - Counter(BRACKET_TOKEN.findall(src))
        if any(GAME_TOKEN.match(token[1:-1]) for token in extra):
            return True
    return len(NEWLINE.findall(value)) != len(NEWLINE.findall(src))


def def_values(mod):
    """scan_defs + listas `rulesStrings` no formato de lista completa (`<li>`)."""
    entries, _, _ = scan_defs(mod)
    for path in sorted(mod.rglob('*.xml')):
        if 'Languages' in path.parts:
            continue
        root = parse_xml(path)
        if root is None:
            continue
        for el in root.iter():
            if (el.get('Abstract') or '').lower() == 'true':
                continue
            name = next(((c.text or '').strip() for c in el if c.tag == 'defName'), '')
            if not name:
                continue
            for rules in el.iter('rulesStrings'):
                items = [re.sub(r'\s*\n\s*', ' ', ''.join(li.itertext())).strip()
                         for li in rules.findall('li')]
                if items:
                    entries[(el.tag, f'{name}.{path_of(el, rules)}')] = '\n'.join(items)
    return entries


def path_of(def_el, target):
    """Caminho relativo do elemento dentro do Def, listas indexadas por `li`."""
    def walk(node, path):
        for i, child in enumerate(node):
            seg = str(i) if child.tag == 'li' else child.tag
            here = f'{path}.{seg}' if path else seg
            if child is target:
                return here
            found = walk(child, here)
            if found:
                return found
        return ''
    return walk(def_el, '')


def keyed_values(mod):
    """Valores de Languages/English/Keyed do mod fonte (chave -> texto); versao mais nova vence."""
    values = {}
    for path in sorted(mod.rglob('*.xml'), key=lambda p: (version_of(p, mod), str(p))):
        parts = path.parts
        if 'Languages' not in parts:
            continue
        i = parts.index('Languages')
        if i + 1 >= len(parts) or parts[i + 1] != 'English' or 'Keyed' not in parts[i + 2:]:
            continue
        root = parse_xml(path)
        if root is None:
            continue
        for el in root:
            if el.tag != 'LanguageData':
                values.setdefault(el.tag, []).append((el.text or '').strip())
    return values


def check_file(path, source, keyed, failures):
    """Valida um XML alvo; retorna quantas chaves foram conferidas."""
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        failures.append(f'XML inválido: {path}: {exc}')
        return 0
    checked = 0
    for el in root:
        if el.tag == 'LanguageData':
            continue
        if el.tag == 'rep':
            sub = el.findtext('path') or ''
            value = el.findtext('trans') or ''
            checked += 1
            src = keyed and source.get(sub) or None if keyed else source.get((path.parent.name, sub))
            if src is None:
                failures.append(f'chave órfã: {sub} (rep)')
            elif token_problems(value, src):
                failures.append(f'placeholder divergente: {sub} (rep)')
            continue
        key = el.tag
        items = [''.join(li.itertext()).strip() for li in el.findall('li')]
        value = '\n'.join(items) if items else (el.text or '')
        checked += 1
        srcs = source.get(key) if keyed else ([source[(path.parent.name, key)]]
                                              if (path.parent.name, key) in source else [])
        src = srcs[0] if srcs else None
        if src is None:
            failures.append(f'chave órfã: {key}')
        elif not value.strip() and any(s.strip() for s in srcs):
            failures.append(f'valor vazio: {key}')
        elif items or key.endswith('.rulesStrings'):
            missing = (Counter(i.split('->')[0].strip() for i in src.split('\n'))
                       - Counter(i.split('->')[0].strip() for i in value.split('\n')))
            if missing:
                failures.append(f'regra ausente: {key} {dict(missing)}')
        elif not any(token_problems(value, s, bracket=not keyed) is False for s in srcs):
            failures.append(f'placeholder divergente: {key}')
    return checked


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument('--mod', action='extend', nargs='+', metavar='FOLDERID|PATH',
                     help='folderId da Workshop ou caminho direto (repetivel)')
    sel.add_argument('--batch', metavar='L', help=f'lote: {", ".join(BATCHES)}')
    sel.add_argument('--all', action='store_true', help='todos os alvos do mapa MODS')
    ap.add_argument('--repo', default=str(REPO_LANG), metavar='DIR',
                    help='raiz do alvo a validar (default: Languages/PortugueseBrazilian)')
    ap.add_argument('--prefix', metavar='NOME', help='prefixo de arquivo para mod fora do mapa MODS')
    ap.add_argument('--keyed', action='store_true', help='valida Keyed (fase 2)')
    args = ap.parse_args(argv)

    json_batches, _ = load_targets()
    if args.batch is not None:
        if args.batch in BATCHES:
            targets = [(WORKSHOP/fid, MODS[fid][0]) for fid in BATCHES[args.batch]]
        elif args.batch in json_batches:
            targets = [(WORKSHOP/r['folderId'], r['prefix']) for r in json_batches[args.batch]]
        else:
            ap.error(f'lote desconhecido: {args.batch!r}')
    elif args.all:
        targets = [(WORKSHOP/fid, MODS[fid][0]) for fid in MODS]
    else:
        targets = [(mod, prefix) for mod, prefix, _ in
                   (resolve_mod(arg, args.prefix, ap) for arg in args.mod)]

    repo = pathlib.Path(args.repo)
    failures, checked = [], 0
    for mod, prefix in targets:
        if not mod.is_dir():
            print(f'ERRO: mod ausente: {mod}', file=sys.stderr)
            return 1
        source = keyed_values(mod) if args.keyed else def_values(mod)
        base = repo/'Keyed' if args.keyed else repo
        paths = sorted(p for p in base.rglob(f'{prefix}_*.xml')
                       if args.keyed or 'Keyed' not in p.parts)
        if not paths:
            print(f'aviso: sem arquivos {prefix}_*.xml em {repo}', file=sys.stderr)
        for path in paths:
            checked += check_file(path, source, args.keyed, failures)

    if failures:
        print('\n'.join(failures))
        return 1
    print(f'OK {checked} chaves')
    return 0


if __name__ == '__main__':
    sys.exit(main())
