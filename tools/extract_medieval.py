#!/usr/bin/env python3
"""Gera esqueletos DefInjected a partir dos Defs de mods instalados.

Modo padrao (fase 1): varre os Defs de cada mod, extrai campos escalares da
whitelist e escreve esqueletos em DefInjected/<DefType>/<prefixo>_<DefType>.xml
pulando chaves ja existentes no repo. --keyed (fase 2) faz o mesmo para as
chaves dos arquivos Languages/English/Keyed, com valor vazio.
"""
import argparse
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

WORKSHOP = pathlib.Path.home()/'.local/share/Steam/steamapps/workshop/content/294100'
REPO_LANG = pathlib.Path('Languages/PortugueseBrazilian')
MODSCONFIG = pathlib.Path.home()/'.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Config/ModsConfig.xml'

FIELDS = {'label','description','labelFemale','labelPlural','labelNoun','jobString',
          'verb','gerund','letterText','reportString','text','title','summary','tip',
          'baseDesc','titleShort','titleShortFemale','titleFemale','titleMale','deathMessage'}

NESTED_LISTS = ('degreeDatas', 'stages')
NESTED_FIELDS = ('label', 'description')

MODS = {  # folderId: (prefixo de arquivo, nome)
 '1916352291':('RimTraits','RimTraits - Medieval Talents'), '2101545242':('Prosthetics','Medieval Prosthetics'),
 '2109206579':('Medicines','Medieval Medicines'), '2501486827':('FortMedieval','Fortifications - Medieval'),
 '2501487160':('FortMaterial','Fortifications - Medieval Material'), '2646321064':('MORoyalty','MO: Royalty'),
 '2730497766':('MOTweaks','MO Tweaks'), '2836791007':('RimFantasyMO','RimFantasy MO Edition'),
 '2881104575':('HRKCoffin','HRK deathrest coffin'), '2883228057':('MedMedsMO','Medicines MO Edition'),
 '2883913520':('MedievalWalls','Medieval Walls'), '2942661554':('RareResources','Fantasy Rare Resources'),
 '2955864975':('QuestRewards','Fantasy Quest Rewards'), '2967087032':('MOExtraSigns','MO Extra Signs'),
 '3028566550':('DarkAges','Dark Ages Tools'), '3035624471':('RelicQuests','Fantasy Relic Quests'),
 '3170653412':('BackstoriesPatch','Medieval Backstories'), '3171518917':('GeneAssembler','Gene Assembler'),
 '3216459199':('MOBarbarians','MO: Barbarians'), '3271602770':('MiscTraining','Misc Training Retexture'),
 '3327601396':('HouseVanIlla','MO: House Van Illa'), '3394688448':('Hunts','Adventures: Hunts'),
 '3397035499':('Implants','Adventures: Implants'), '3425601715':('AdaptiveStorage','MO: Adaptive Storage'),
 '3448488157':('TraderAirships','Trader Airships'), '3454176238':('Chemfuel','Chemfuel Retextured'),
 '3455187565':('OverlapRemover','Overlap Remover'), '3464984971':('Geysers','Things: Geysers'),
 '3480089301':('TastyArmory','Tasty Armory'), '3483685923':('CoastalOutfits','Coastal Outfits'),
 '3488857567':('Signs','Medieval Signs'), '3510803927':('DBH','DBH Retexture'),
 '3512201406':('Tailor','Medieval Tailor'), '3526042587':('Roxmont','MO: House Roxmont'),
 '3540876712':('SpaceKnights','Space Knights VFEM2'), '3560507606':('Transport','Medieval Transport'),
 '3562593688':('Anomaly','Medieval Anomaly'), '3583175669':('Hornet','MO: Hornetkeeping'),
 '3648522175':('ReGrowth','MO ReGrowth 2 Patch'), '3712538846':('Ignivar','MO: House Ignivar'),
}

BATCHES = {
 'L1':['2883913520','3488857567','3560507606','3464984971','3583175669','2881104575','2109206579',
       '2967087032','3540876712','3483685923','3510803927','3648522175','3455187565','3562593688',
       '3271602770','3454176238'],
 'L2a':['3327601396','3526042587','3712538846','2730497766','3425601715'],
 'L2b':['2646321064'], 'L2c':['3216459199'],
 'L3a':['3171518917','3170653412','3028566550','3397035499','3394688448','2501486827','2942661554','3448488157'],
 'L3b':['3480089301','3512201406','2501487160','2955864975','3035624471'],
 'L4':['2836791007','1916352291','2101545242','2883228057'],
}
LOTES = {fid: batch for batch, ids in BATCHES.items() for fid in ids}


def parse_xml(path):
    try:
        return ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        print(f'aviso: ignorado {path}: {exc}', file=sys.stderr)
        return None


def text_of(el):
    value = (el.text or '').strip()
    return value.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n')


def escape(value):
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


VERSION_DIR = re.compile(r'\d+(?:\.\d+)*')


def version_of(path, mod):
    """Versao do diretorio (1.6 > 1.5 > ... > raiz); diretorios nao-numericos contam como (0,)."""
    for part in path.relative_to(mod).parts[:-1]:
        if VERSION_DIR.fullmatch(part):
            return tuple(int(x) for x in part.split('.'))
    return (0,)


def nested_entries(name, el):
    """Chaves aninhadas indexadas: degreeDatas/stages e comps.<i>.tools.<j>."""
    out = []
    for tag in NESTED_LISTS:
        seq = el.find(tag)
        if seq is None:
            continue
        for i, li in enumerate(seq.findall('li')):
            for field in NESTED_FIELDS:
                child = li.find(field)
                value = text_of(child) if child is not None else ''
                if value:
                    out.append((f'{name}.{tag}.{i}.{field}', value))
    comps = el.find('comps')
    if comps is not None:
        for i, comp in enumerate(comps.findall('li')):
            tools = comp.find('tools')
            if tools is None:
                continue
            for j, tool in enumerate(tools.findall('li')):
                for field in NESTED_FIELDS:
                    child = tool.find(field)
                    value = text_of(child) if child is not None else ''
                    if value:
                        out.append((f'{name}.comps.{i}.tools.{j}.{field}', value))
    tools = el.find('tools')
    if tools is not None:
        for i, tool in enumerate(tools.findall('li')):
            for field in NESTED_FIELDS:
                child = tool.find(field)
                value = text_of(child) if child is not None else ''
                if value:
                    out.append((f'{name}.tools.{i}.{field}', value))
    return out


def scan_english_definjected(mod, entries):
    """DefInjected do proprio mod em Languages/English sobrepoe os valores dos Defs."""
    for path in sorted(mod.rglob('*.xml')):
        parts = path.parts
        if 'Languages' not in parts:
            continue
        i = parts.index('Languages')
        if i + 1 >= len(parts) or parts[i + 1] != 'English' or 'DefInjected' not in parts[i + 2:]:
            continue
        j = parts.index('DefInjected')
        if j + 1 >= len(parts):
            continue
        root = parse_xml(path)
        if root is None:
            continue
        for el in root:
            if el.tag == 'LanguageData' or '.' not in el.tag:
                continue
            value = text_of(el)
            if value:
                entries[(parts[j + 1], el.tag)] = value


def scan_defs(mod):
    """Campos escalares por (DefType, chave); versao mais nova vence + contagem solta."""
    entries, labels, descriptions = {}, 0, 0
    for path in sorted(mod.rglob('*.xml'), key=lambda p: (version_of(p, mod), str(p))):
        if 'Languages' in path.parts:
            continue
        root = parse_xml(path)
        if root is None:
            continue
        for el in root.iter():
            if el.tag == 'label':
                labels += 1
            elif el.tag == 'description':
                descriptions += 1
            if (el.get('Abstract') or '').lower() == 'true':
                continue
            name = next(((c.text or '').strip() for c in el if c.tag == 'defName'), '')
            if not name:
                continue
            for child in el:
                if child.tag in FIELDS:
                    value = text_of(child)
                    if value:
                        entries[(el.tag, f'{name}.{child.tag}')] = value
            for key, value in nested_entries(name, el):
                entries[(el.tag, key)] = value
    scan_english_definjected(mod, entries)
    return entries, labels, descriptions


def scan_keyed(mod):
    entries = {}
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
                entries.setdefault(el.tag, '')
    return entries


def repo_index(repo):
    """(chaves DefInjected por (DefType, chave), chaves Keyed) ja existentes no repo."""
    def_keys, keyed_keys = set(), set()
    if not repo.is_dir():
        print(f'aviso: repo ausente: {repo}', file=sys.stderr)
        return def_keys, keyed_keys
    for path in sorted(repo.rglob('*.xml')):
        parts = path.parts
        root = parse_xml(path)
        if root is None:
            continue
        if 'DefInjected' in parts:
            dtype = parts[parts.index('DefInjected') + 1]
            for el in root.iter():
                if el.tag != 'LanguageData':
                    def_keys.add((dtype, el.tag))
        elif 'Keyed' in parts:
            for el in root.iter():
                if el.tag != 'LanguageData':
                    keyed_keys.add(el.tag)
    return def_keys, keyed_keys


def write_skeleton(path, pairs):
    """Escreve/atualiza o esqueleto preservando entradas ja existentes."""
    existing = []
    if path.exists():
        root = parse_xml(path)
        if root is not None:
            existing = [(el.tag, el.text or '') for el in root if el.tag != 'LanguageData']
    have = {key for key, _ in existing}
    merged = existing + [pair for pair in pairs if pair[0] not in have]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n<LanguageData>\n')
        for key, value in merged:
            fh.write(f'  <{key}>{escape(value)}</{key}>\n')
        fh.write('</LanguageData>\n')


def resolve_mod(arg, prefix, parser):
    path = pathlib.Path(arg).expanduser()
    if path.is_dir():
        mod = path.resolve()
        fid = mod.name if mod.parent == WORKSHOP else None
    elif (WORKSHOP/arg).is_dir():
        mod, fid = WORKSHOP/arg, arg
    else:
        parser.error(f'mod nao encontrado: {arg}')
    if fid in MODS:
        return mod, MODS[fid][0], fid
    if not prefix:
        parser.error(f'--prefix obrigatorio para {arg} (fora do mapa MODS)')
    return mod, prefix, fid


def package_id(mod):
    about = mod/'About'/'About.xml'
    if not about.exists():
        return ''
    root = parse_xml(about)
    if root is None:
        return ''
    el = root.find('packageId')
    return (el.text or '').strip() if el is not None else ''


def active_packages():
    if not MODSCONFIG.exists():
        return set()
    root = parse_xml(MODSCONFIG)
    if root is None:
        return set()
    active = root.find('activeMods')
    if active is None:
        return set()
    return {(li.text or '').strip().lower() for li in active.findall('li')}


def write_inventory(path, rows):
    lines = ['# Inventario - Campanha Medieval (PT-BR)', '',
             '| folder id | packageId | nome | labels | descriptions | total | status | ativo | lote |',
             '|---|---|---|---:|---:|---:|---|---|---|']
    for row in rows:
        lines.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument('--mod', action='extend', nargs='+', metavar='FOLDERID|PATH',
                     help='folderId da Workshop ou caminho direto (repetivel)')
    sel.add_argument('--batch', metavar='L', help=f'lote: {", ".join(BATCHES)}')
    sel.add_argument('--all', action='store_true', help='todos os alvos do mapa MODS')
    ap.add_argument('--out', required=True, metavar='DIR', help='diretorio de saida')
    ap.add_argument('--repo', default=str(REPO_LANG), metavar='LANGDIR',
                    help='raiz do repo ou dir de idioma (default: Languages/PortugueseBrazilian)')
    ap.add_argument('--prefix', metavar='NOME', help='prefixo de arquivo para mod fora do mapa MODS')
    ap.add_argument('--keyed', action='store_true', help='fase 2: chaves de Languages/English/Keyed')
    ap.add_argument('--inventory', metavar='MD', help='grava tabela markdown de inventario')
    args = ap.parse_args(argv)
    if args.keyed and args.inventory:
        ap.error('--inventory e apenas da fase 1 (DefInjected)')

    if args.batch is not None:
        if args.batch not in BATCHES:
            ap.error(f'lote desconhecido: {args.batch!r} (disponiveis: {", ".join(BATCHES)})')
        targets = [(WORKSHOP/fid, MODS[fid][0], fid) for fid in BATCHES[args.batch]]
    elif args.all:
        targets = [(WORKSHOP/fid, MODS[fid][0], fid) for fid in MODS]
    else:
        targets = [resolve_mod(arg, args.prefix, ap) for arg in args.mod]

    out = pathlib.Path(args.out)
    repo_def, repo_keyed = repo_index(pathlib.Path(args.repo))
    emitted = set()
    active = active_packages()
    rows = []

    for mod, prefix, fid in targets:
        if not mod.is_dir():
            print(f'ERRO: mod ausente: {mod}', file=sys.stderr)
            return 1
        if args.keyed:
            entries = scan_keyed(mod)
            fresh = [k for k in entries
                     if k not in repo_keyed and ('Keyed', k) not in emitted]
            if fresh:
                write_skeleton(out/'Keyed'/f'{prefix}_Keys.xml', [(k, '') for k in fresh])
            emitted.update(('Keyed', k) for k in fresh)
            print(f'{prefix}: {len(fresh)} chaves Keyed novas')
            continue
        entries, labels, descriptions = scan_defs(mod)
        groups = {}
        for (dtype, key), value in entries.items():
            if (dtype, key) in repo_def or key in repo_keyed or (dtype, key) in emitted:
                continue
            groups.setdefault(dtype, []).append((key, value))
            emitted.add((dtype, key))
        for dtype, pairs in groups.items():
            write_skeleton(out/'DefInjected'/dtype/f'{prefix}_{dtype}.xml', pairs)
        print(f'{prefix}: {sum(len(p) for p in groups.values())} chaves novas '
              f'({labels} labels, {descriptions} descriptions)')
        if args.inventory:
            total = len(entries)
            covered = sum(1 for dtype, key in entries
                          if (dtype, key) in repo_def or key in repo_keyed)
            status = 'coberto' if total and covered == total else ('parcial' if covered else 'sem')
            pid = package_id(mod)
            nome = MODS[fid][1] if fid in MODS else prefix
            rows.append((fid or mod.name, pid, nome, labels, descriptions, labels + descriptions,
                         status, 'sim' if pid.lower() in active else 'nao', LOTES.get(fid, '-')))

    if args.inventory:
        write_inventory(pathlib.Path(args.inventory), rows)
        print(f'inventario: {len(rows)} alvos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
