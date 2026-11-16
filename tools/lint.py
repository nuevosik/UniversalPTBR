#!/usr/bin/env python3
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

LANG = pathlib.Path('Languages/PortugueseBrazilian')
KEY = re.compile(r'[A-Za-z_][\w.:-]*')
COLOR_OPEN = re.compile(r'<color[^>]*>')


def lint(lang):
    problems = []
    owners = defaultdict(list)
    for path in sorted(lang.rglob('*.xml')):
        if path.name == 'LanguageInfo.xml':
            continue
        rel = path.relative_to(lang)
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            problems.append(f'{rel}: XML inválido: {exc}')
            continue
        kind = rel.parts[0]
        for el in root:
            key = el.tag
            if not isinstance(key, str):
                continue
            value = ''.join(el.itertext()).strip()
            if key == 'li' or (kind == 'DefInjected' and '.' not in key) or not KEY.fullmatch(key):
                problems.append(f'{rel}: chave inválida <{key}>')
                continue
            scope = 'Keyed' if kind == 'Keyed' else rel.parts[1]
            owners[(scope, key)].append(str(rel))
            if not value or value.lower() in ('todo', 'a fazer', 'texto.todo'):
                problems.append(f'{rel}: {key}: valor vazio/TODO')
            elif len(COLOR_OPEN.findall(value)) != value.count('</color>'):
                problems.append(f'{rel}: {key}: <color> desbalanceado')
            elif value.count('{') != value.count('}'):
                problems.append(f'{rel}: {key}: chaves {{}} desbalanceadas')
            elif re.search(r'\bAlvo[ABC]\b', value):
                problems.append(f'{rel}: {key}: token TargetA/B/C traduzido')
    for (scope, key), files in owners.items():
        if len(files) > 1:
            problems.append(f'{scope}: {key} duplicada em {", ".join(files)}')
    return problems


def selfcheck():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        lang = pathlib.Path(tmp)
        (lang/'Keyed').mkdir()
        (lang/'DefInjected'/'ThingDef').mkdir(parents=True)
        (lang/'Keyed'/'A.xml').write_text('<LanguageData><K1>ok {0}</K1><K2>TODO</K2></LanguageData>', encoding='utf-8')
        (lang/'Keyed'/'B.xml').write_text('<LanguageData><K1>de novo</K1></LanguageData>', encoding='utf-8')
        (lang/'DefInjected'/'ThingDef'/'C.xml').write_text(
            '<LanguageData><li>x</li><T.label>&lt;color=red&gt;a</T.label><T.description>b</T.description></LanguageData>',
            encoding='utf-8')
        out = '\n'.join(lint(lang))
        for needle in ('K2: valor vazio/TODO', 'K1 duplicada', 'chave inválida <li>', 'T.label: <color>'):
            assert needle in out, (needle, out)
        assert 'T.description' not in out, out
    print('selfcheck OK')


def main():
    if '--selfcheck' in sys.argv:
        selfcheck()
        return 0
    problems = lint(LANG)
    for path in [*sorted(pathlib.Path('Patches').glob('*.xml')), pathlib.Path('About/About.xml'),
                 pathlib.Path('LoadFolders.xml')]:
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            problems.append(f'{path}: XML inválido: {exc}')
    print('\n'.join(problems) or 'OK')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
