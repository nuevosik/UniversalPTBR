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

from extract_medieval import BATCHES, MODS, REPO_LANG, WORKSHOP, parse_xml, resolve_mod, scan_defs

PLACEHOLDER = re.compile(r'\{[^}]+\}')
COLOR_TAG = re.compile(r'</?color[^>]*>')
BRACKET_TOKEN = re.compile(r'\[[^\]]+\]')
NEWLINE = re.compile(r'\\n|\n')


def token_problems(value, src):
    """{...}/<color> exatos; [...] não pode inventar nem repetir token do EN
    (o PT-BR reescreve [PAWN_possessive] como seu/sua — prática do pacote oficial,
    que não usa o token em nenhuma linha traduzida)."""
    if Counter(PLACEHOLDER.findall(value)) != Counter(PLACEHOLDER.findall(src)):
        return True
    if Counter(COLOR_TAG.findall(value)) != Counter(COLOR_TAG.findall(src)):
        return True
    if Counter(BRACKET_TOKEN.findall(value)) - Counter(BRACKET_TOKEN.findall(src)):
        return True
    return len(NEWLINE.findall(value)) != len(NEWLINE.findall(src))


def keyed_values(mod):
    """Valores de Languages/English/Keyed do mod fonte (chave -> texto)."""
    values = {}
    for path in sorted(mod.rglob('*.xml')):
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
                values.setdefault(el.tag, (el.text or '').strip())
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
        key = el.tag
        value = el.text or ''
        checked += 1
        src = source.get(key) if keyed else source.get((path.parent.name, key))
        if src is None:
            failures.append(f'chave órfã: {key}')
        elif not value.strip():
            failures.append(f'valor vazio: {key}')
        elif token_problems(value, src):
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

    if args.batch is not None:
        if args.batch not in BATCHES:
            ap.error(f'lote desconhecido: {args.batch!r} (disponiveis: {", ".join(BATCHES)})')
        targets = [(WORKSHOP/fid, MODS[fid][0]) for fid in BATCHES[args.batch]]
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
        source = keyed_values(mod) if args.keyed else scan_defs(mod)[0]
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
