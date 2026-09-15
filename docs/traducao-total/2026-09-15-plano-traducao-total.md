# Plano de Tradução Total (PT-BR) — todos os mods instalados

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** zerar o texto traduzível (DefInjected whitelist + Keyed) de todos os 139 alvos instalados pendentes, ~26.290 chaves, em lotes validados e revisados um a um.

**Architecture:** herda o pipeline medieval (`tools/extract_medieval.py` + `tools/validate_medieval.py`) e adiciona um inventariador (`tools/coverage.py`) que gera `tools/targets.json` (alvos, prefixos e lotes). Extração → tradução por subagentes (glossário + constraints) → validação automática → revisão humana → commit por lote. PT-OWN (mods com `PortugueseBrazilian` próprio) ficam fora; DMS/WD2 têm os arquivos fantasma removidos e são retraduzidos de verdade.

**Tech Stack:** Python 3 (stdlib), `xmllint`, git. Sem dependências novas.

**Contexto/spec:** `docs/medieval/2026-09-14-campanha-medieval-design.md` (regras herdadas) + auditoria de 2026-09-15 registrada abaixo.

## Estado atual (auditoria 2026-09-15)

- 253 mods instalados (252 sem contar esta tradução): 158 com pendência, **139 na campanha = 26.290 chaves**; 18 excluídos por terem PT-BR próprio (CE, Medieval Overhaul, DBH Lite, HugsLib etc.); 1 excluído por pacote dedicado (RimHUD ↔ `RimHUD PortugueseBrazilian`); 47 sem defs/keys (retexturas/performance).
- **The Dead Man's Switch**: 9 arquivos PT-BR, 62 entradas — 56 chaves inexistentes; 6 reais com descrição inventada e `{0}` que não existe no EN. Cobertura real: 3 de 753 defs. Não tinha Keyed detectado na v1; o extrator acha 38 chaves Keyed em subpastas DLC.
- **World Domination 2.0**: 6 arquivos PT-BR, 42 entradas — 42 chaves inexistentes (`WD_*`; as reais são `TSA_WD_*`). Cobertura real: 0 de 432 defs / 0 de 5.146 keys.
- Origem dos fantasmas: commit `6deca59`; também copiados para `Mods/Tradução Universal (PT-BR)`.
- Contagens por mod e lotes: tabelas abaixo (geradas pelo extrator real do repo, mesmos critérios que a campanha vai usar).

## Global Constraints

- Fonte dos mods: `~/.local/share/Steam/steamapps/workshop/content/294100/<folderId>`; local: `~/.local/share/Steam/steamapps/common/RimWorld/Mods`.
- Só editar valores; nunca renomear chaves, `defName`s, arquivos ou pastas.
- Preservar verbatim: `{0}`/`{PAWN_*}`/`[TOKEN]`, `\n`, tags `<color>`, entidades XML, encoding UTF-8 (BOM onde existir).
- Seguir `docs/medieval/GLOSSARY.md` + `docs/traducao-total/GLOSSARY.md` (novo); novos termos vão para `cSpell.words` em `.vscode/settings.json`.
- Classificar antes de editar (nomes próprios/técnicos não se traduzem); um termo por conceito, sem sinônimo concorrente no mesmo lote.
- Fase 1 = campos da whitelist do extrator (`label`, `description`, `labelFemale`, `labelPlural`, `jobString`, `verb`, `gerund`, `letterText`, `reportString`, `text`, `title`, `summary`, `tip`, `baseDesc`, títulos, `deathMessage`) + aninhados já suportados (`degreeDatas`, `stages`, `comps.*.tools.*`). `rulePacks` genéricos e strings dentro de `.dll` ficam fora.
- Antes de cada commit: `xmllint --noout` nos XMLs tocados, `python3 tools/validate_medieval.py ...` → `OK`, `git diff --check`, `git status --short` sem sobras.
- Precondição: working tree limpo. Commits com identidade `git -c user.name=OpenCode -c user.email=opencode@universal-ptbr`; conventional commits em PT: `feat(lang): traduz <lote> (PT-BR)`.
- Gate humano obrigatório: glossário e todo lote param para revisão do diff antes do commit.

## Decisões

| Tema | Decisão |
|---|---|
| Escopo | Todos os 139 alvos do `targets.json`; PT-OWN e RimHUD fora (já têm tradução) |
| Fantasmas | Deletar antes de reextrair (senão o extrator preserva as entradas órfãs) |
| Extração | In-place em `Languages/PortugueseBrazilian` (fluxo herdado); `--keyed` em passe separado |
| Lotes | Gerados por tamanho (cap 1.500 chaves); B1/B2/B3 traduzidos por vários subagentes em paralelo (1 por arquivo-fonte) e commit único por alvo |
| Fase 2 Keyed | Só onde o mod embarca `Languages/English/Keyed`; validada com `--keyed` |
| Revisão | Humano revisa diff + amostra de 10 strings EN→PT por lote |
| cSpell | Termos novos adicionados no lote que os introduz |

## File Structure

| Arquivo | Responsabilidade |
|---|---|
| `tools/coverage.py` | Novo. Inventaria mods instalados, calcula pendências, emite `targets.json` e relatório; `--selfcheck` embutido |
| `tools/targets.json` | Novo (gerado). folderId → prefixo/nome/packageId/pendências; lotes B1–B16 |
| `tools/extract_medieval.py` | Modificar: resolver alvos pelo `targets.json` quando `--batch` não for lote medieval |
| `tools/validate_medieval.py` | Modificar: idem no `--batch` |
| `docs/traducao-total/GLOSSARY.md` | Novo. Termos EN→PT das novas franquias (WD2, DMS, CQF, Deserters, Memes, utilitários) |
| `docs/traducao-total/INVENTORY.md` | Novo (gerado pelo coverage). Status por mod |
| `Languages/PortugueseBrazilian/**` | Esqueletos e traduções |
| `README.md` | Modificar: verdade sobre DMS/WD2 e lista final |

---

### Task 1: Remover os arquivos fantasma de DMS/WD2

**Files:**
- Delete: `Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml`, `Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml`
- Delete: `Languages/PortugueseBrazilian/DefInjected/FactionDef/DMS_FactionDef.xml`, `DefInjected/FactionDef/WD2_FactionDef.xml`
- Delete: `DefInjected/GeneDef/DMS_GeneDef.xml`, `DefInjected/HediffDef/DMS_HediffDef.xml`, `DefInjected/PawnKindDef/DMS_PawnKindDef.xml`
- Delete: `DefInjected/QuestScriptDef/DMS_QuestScriptDef.xml`, `DefInjected/QuestScriptDef/WD2_QuestScriptDef.xml`
- Delete: `DefInjected/RecipeDef/DMS_RecipeDef.xml`, `DefInjected/ResearchProjectDef/DMS_ResearchProjectDef.xml`
- Delete: `DefInjected/SitePartDef/WD2_SitePartDef.xml`, `DefInjected/ThingDef/DMS_ThingDef.xml`, `DefInjected/ThingDef/WD2_ThingDef.xml`, `DefInjected/WorldObjectDef/WD2_WorldObjectDef.xml`

- [ ] **Step 1: Conferir que são 15 e só os fantasma**

Run: `git ls-files Languages/PortugueseBrazilian | rg '(DMS|WD2)' | wc -l`
Expected: `15`

- [ ] **Step 2: Deletar**

```bash
git rm Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml \
  Languages/PortugueseBrazilian/DefInjected/FactionDef/DMS_FactionDef.xml \
  Languages/PortugueseBrazilian/DefInjected/FactionDef/WD2_FactionDef.xml \
  Languages/PortugueseBrazilian/DefInjected/GeneDef/DMS_GeneDef.xml \
  Languages/PortugueseBrazilian/DefInjected/HediffDef/DMS_HediffDef.xml \
  Languages/PortugueseBrazilian/DefInjected/PawnKindDef/DMS_PawnKindDef.xml \
  Languages/PortugueseBrazilian/DefInjected/QuestScriptDef/DMS_QuestScriptDef.xml \
  Languages/PortugueseBrazilian/DefInjected/QuestScriptDef/WD2_QuestScriptDef.xml \
  Languages/PortugueseBrazilian/DefInjected/RecipeDef/DMS_RecipeDef.xml \
  Languages/PortugueseBrazilian/DefInjected/ResearchProjectDef/DMS_ResearchProjectDef.xml \
  Languages/PortugueseBrazilian/DefInjected/SitePartDef/WD2_SitePartDef.xml \
  Languages/PortugueseBrazilian/DefInjected/ThingDef/DMS_ThingDef.xml \
  Languages/PortugueseBrazilian/DefInjected/ThingDef/WD2_ThingDef.xml \
  Languages/PortugueseBrazilian/DefInjected/WorldObjectDef/WD2_WorldObjectDef.xml
```

- [ ] **Step 3: Validar que nada mais aponta para DMS/WD2**

Run: `git grep -l 'DMS\|WD2' -- Languages | wc -l`
Expected: `0`

- [ ] **Step 4: Commit**

```bash
git add -A
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "fix(lang): remove traduções fantasma de DMS e WD2"
```

---

### Task 2: Corrigir o README

**Files:**
- Modify: `README.md` (tabela "Mods Atualmente Traduzidos", linhas do DMS e WD2)

- [ ] **Step 1: Editar as duas linhas**

Trocar a descrição por:

```markdown
| **The Dead Man's Switch** | ⚠️ em tradução — os arquivos anteriores eram fantasma (chaves inexistentes) e foram removidos. |
| **World Domination 2.0** | ⚠️ em tradução — os arquivos anteriores eram fantasma (chaves inexistentes) e foram removidos. |
```

- [ ] **Step 2: Conferir que nenhuma outra linha promete tradução inexistente**

Run: `rg -n "Dead Man|World Domination" README.md`
Expected: as duas linhas com "em tradução".

- [ ] **Step 3: Commit**

```bash
git add README.md
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "docs: README honesto sobre DMS/WD2"
```

---

### Task 3: Inventariador `tools/coverage.py`

**Files:**
- Create: `tools/coverage.py`
- Test: `--selfcheck` embutido (fixture temporária)

**Interfaces:**
- Consumes: `tools/extract_medieval.py` (`scan_defs`, `scan_keyed`, `repo_index`, `parse_xml`, `WORKSHOP`)
- Produces: CLI `python3 tools/coverage.py [--json tools/targets.json] [--md docs/traducao-total/INVENTORY.md] [--selfcheck]`. JSON: `{"generated": ..., "campaign": {...}, "excluded": [...], "batches": {"B1": [{"folderId","prefix","name","packageId","missingDefs","missingKeys"}...]}}`; lotes gulosos de até 1.500 chaves, PT-OWN/pacotes dedicados fora.

- [ ] **Step 1: Escrever o script**

```python
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
```

- [ ] **Step 2: Rodar o selfcheck**

Run: `python3 tools/coverage.py --selfcheck`
Expected: `selfcheck OK`

- [ ] **Step 3: Gerar os dados reais e conferir contra a auditoria**

Run: `python3 tools/coverage.py`
Expected: `alvos 139 | chaves 26290 | lotes 16 | excluídos 19` (tolerância: ±2 alvos se o Steam atualizar um mod; conferir `git diff tools/targets.json`).

- [ ] **Step 4: `xmllint` no que foi gerado (só markdown/json aqui) e commit**

```bash
git add tools/coverage.py tools/targets.json docs/traducao-total/INVENTORY.md
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(tools): inventariador da tradução total"
```

---

### Task 4: Integrar `targets.json` ao extrator e ao validador

**Files:**
- Modify: `tools/extract_medieval.py` (`import json`; `load_targets`, `resolve_mod`, `main`)
- Modify: `tools/validate_medieval.py` (`--batch` fora de `BATCHES`)

**Interfaces:**
- Consumes: `tools/targets.json` da Task 3
- Produces: `--batch B1..B16` funcionando nos dois CLIs

- [ ] **Step 1: Teste que falha**

Run: `python3 tools/extract_medieval.py --batch B1 --out /tmp/opencode/skel-B1`
Expected: erro `lote desconhecido: 'B1'`.

- [ ] **Step 2: Editar `tools/extract_medieval.py`**

Adicionar `import json` e, após `LOTES = ...`:

```python
TARGETS_JSON = pathlib.Path(__file__).with_name('targets.json')


def load_targets():
    if not TARGETS_JSON.exists():
        return {}, {}
    try:
        data = json.loads(TARGETS_JSON.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}, {}
    flat = {r['folderId']: r for rows in data.get('batches', {}).values() for r in rows}
    return data.get('batches', {}), flat
```

Em `resolve_mod`, antes do `parser.error` final:

```python
    _, flat = load_targets()
    if fid in flat:
        return mod, flat[fid]['prefix'], fid
```

Em `main`, no bloco `if args.batch is not None:`:

```python
    json_batches, _ = load_targets()
    if args.batch is not None:
        if args.batch in BATCHES:
            targets = [(WORKSHOP/fid, MODS[fid][0], fid) for fid in BATCHES[args.batch]]
        elif args.batch in json_batches:
            targets = [(WORKSHOP/r['folderId'], r['prefix'], r['folderId'])
                       for r in json_batches[args.batch]]
        else:
            ap.error(f'lote desconhecido: {args.batch!r} (medievais: {", ".join(BATCHES)}; '
                     f'total: {", ".join(json_batches) or "sem targets.json"})')
```

- [ ] **Step 3: Editar `tools/validate_medieval.py`**

Trocar a importação e o bloco do lote:

```python
from extract_medieval import BATCHES, MODS, REPO_LANG, WORKSHOP, parse_xml, resolve_mod, scan_defs, load_targets
```

No `main`:

```python
    json_batches, _ = load_targets()
    if args.batch is not None:
        if args.batch in BATCHES:
            targets = [(WORKSHOP/fid, MODS[fid][0]) for fid in BATCHES[args.batch]]
        elif args.batch in json_batches:
            targets = [(WORKSHOP/r['folderId'], r['prefix']) for r in json_batches[args.batch]]
        else:
            ap.error(f'lote desconhecido: {args.batch!r}')
```

- [ ] **Step 4: Extrair B1 (sem traduzir) e conferir contagem**

```bash
python3 tools/extract_medieval.py --batch B1 --out /tmp/opencode/skel-B1
python3 tools/extract_medieval.py --batch B1 --keyed --out /tmp/opencode/skel-B1
find /tmp/opencode/skel-B1 -name '*.xml' -exec xmllint --noout {} +
```
Expected: mensagens `WorldDomination: <n> chaves novas`; `xmllint` sem erros; total de chaves ≈ 5.408 (defs + keys).

- [ ] **Step 5: Commit**

```bash
git add tools/extract_medieval.py tools/validate_medieval.py
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(tools): lotes do targets.json no extrator e validador"
```

---

### Task 5: Glossário da campanha total (GATE humano)

**Files:**
- Create: `docs/traducao-total/GLOSSARY.md`
- Modify: `.vscode/settings.json` (cSpell.words)

**Interfaces:**
- Consumes: esqueletos reais (B1–B16 em `/tmp/opencode/skel-*`), `docs/medieval/GLOSSARY.md`, PT-BR oficial do jogo
- Produces: mapa EN→PT aprovado, usado por todos os subagentes de tradução

- [ ] **Step 1: Extrair os termos mais frequentes dos esqueletos**

```bash
python3 - <<'EOF'
import collections, re, pathlib
words = collections.Counter()
for p in pathlib.Path('/tmp/opencode').glob('skel-*'):
    for f in p.rglob('*.xml'):
        text = re.sub(r'<[^>]+>', ' ', f.read_text(encoding='utf-8'))
        for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text):
            words[w.lower()] += 1
stop = set('that this with from will have been they when your their into over only does then than also each other more most some such these those'.split())
for w, c in words.most_common(400):
    if w not in stop:
        print(f'{c:6} {w}')
EOF
```
Expected: topo com `outpost`, `caravan`, `goodwill`, `mech`, `bionic`, `gantry`, `research`, `weapon`, `armor`, `tier`, `threat`, `mortar`, `queue`, `bill`, `storage`.

- [ ] **Step 2: Redigir `docs/traducao-total/GLOSSARY.md`**

Estrutura igual à medieval (seções por domínio; coluna Obs indicando fonte: `oficial`, `repo`, `externo`, `novo`). Fonte obrigatória de consulta:

```bash
rg -N --no-filename '>([A-Za-z][^<]{3,})<' \
  "$HOME/.local/share/Steam/steamapps/common/RimWorld/Data/Core/Languages/PortugueseBrazilian/Keyed/"*.xml \
  | head -40     # termos oficiais para conferência
rg -n 'outpost|goodwill|caravan|mortar|raid' Languages/PortugueseBrazilian | head -40   # precedentes no repo
```

Termos mínimos a decidir (com sugestão, sujeita ao gate): outpost → posto avançado; goodwill → boa vontade; caravan → caravana; mortar → morteiro; raid → incursão/investida (escolher UM); spy ops → operações de espionagem; supply line → linha de suprimentos; garrison → guarnição; threat → ameaça; tier → nível; queue/bill → fila/tarefa (conferir `RimCuisine`/`VFE`); automatroid → autômato; bionic → biônico; gantry → gantry (manter, nome do mod); mech → mecanoide; rearm → rearmar; upgrade → melhoria; stat → atributo (oficial); hediff → ferimento/complicação (seguir oficial); ideoligion → ideologia; meme → meme (oficial); research/project → pesquisa/projeto; trap → armadilha; wall → muralha (medieval) / parede (moderno) — decidir por contexto de mod.

- [ ] **Step 3: GATE — apresentar ao humano**

Mostrar a tabela completa e **parar** até "aprovado". Ajustes voltam ao Step 2.

- [ ] **Step 4: Aplicar no cSpell e commitar**

Adicionar ao `cSpell.words` os termos PT novos (sem duplicar os 368 existentes).

```bash
git add docs/traducao-total/GLOSSARY.md .vscode/settings.json
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "docs: glossário da tradução total aprovado"
```

---

## Padrão dos lotes de tradução (Tasks 6–21)

Cada lote repete o ciclo; só o `--batch` muda.

1. **Extrair:** `python3 tools/extract_medieval.py --batch <B> --out Languages/PortugueseBrazilian` e de novo com `--keyed` (Keyed só existe onde o mod tem `Languages/English/Keyed`).
2. **Conferir esqueleto:** `find $(git diff --name-only) -name '*.xml' -exec xmllint --noout {} +` e contagem de chaves novas vs `targets.json`.
3. **Traduzir:** subagentes em paralelo, **1 por mod** (ou 1 por arquivo-fonte em B1/B2/B3); cada um recebe `GLOSSARY.md`, Global Constraints e a lista de arquivos; traduz in-place, preservando chaves/placeholders/indentação; não toca arquivos fora do lote.
4. **Validar:** `python3 tools/validate_medieval.py --batch <B>` e `--keyed` → `OK`; `git diff --check`; `xmllint` nos arquivos do lote.
5. **GATE — revisão humana:** apresentar `git diff --stat`, amostra de 10 strings EN→PT e falhas; **parar** até "ok".
6. **Commit:** `git add <arquivos do lote>`; `git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(lang): traduz <lote> (PT-BR)"`.

### Task 6 — B1: World Domination 2.0 (5.408 chaves, 3680501610)

Maior alvo: 262 defs + 5.146 keys (`TSA_WD_*`). Dividir entre subagentes por arquivo-fonte do English: `Translations_Outposts` (1.838 — o maior, merece 2 subagentes), `Settings` (1.018), `Diplomacy_SpyOps` (600), `UI_Threat_Notifications` (608), `Raids` (320), `Mortar` (311), `Travelers_WorldMap` (266), `ReleaseNotes` (144), `Quests` (42) e DefInjected (262). Commit único do alvo.

### Task 7 — B2: Custom Quest Framework (2.267 chaves, 2978572782)

203 defs + 2.064 keys. Subagentes por bloco de chaves (`HaiLuan.CustomQuestFramework`).

### Task 8 — B3: The Dead Man's Switch (2.117 chaves, 3121742525)

2.079 defs (ThingDef 837, BodyDef 312, RecipeDef 184, HediffDef 165, BackstoryDef 119, PawnKindDef 79...) + 38 keys. Subagentes por DefType; BackstoryDef é texto longo — separar um subagente só para ele.

### Task 9 — B4: Vanilla Ideology Expanded - Memes and Structures (1.621, 2636329500)

1.535 defs + 86 keys. Memes/precepts exigem consistência de gênero — 1 subagente para `MemeDef`, 1 para `PreceptDef`.

### Task 10 — B5: Dubs Rimatomics (823, 1127530465)

553 defs + 270 keys.

### Task 11 — B6: Alpha Animals + Fortified Features Framework (1.215)

Alpha Animals (1541721856, 693 defs — na maior parte animais já cobertos em parte; só lacunas) e FFF (3498575851, 102 defs + 420 keys).

### Task 12 — B7: Fantasy Biotech + Vanilla Weapons Expanded + Dark Ages: Beasts (1.411)

3632363090 (489), 1814383360 (466), 3472275628 (456).

### Task 13 — B8: ReGrowth 2 + RimCuisine 2 + Achievements (1.245)

2260097569 (437), 2562519366 (414), 2288125657 (394). RimCuisine exige glossário de comida (conferir oficial `VCookE`).

### Task 14 — B9: VPE + CE Armory + Deserters + Ancot (1.442)

2842502659 (390), 2911110083 (363), 3025493377 (354), 2988801276 (335). Deserters: terminologia militar; Ancot é biblioteca (muita string curta).

### Task 15 — B10: Melee Animation + Backstories + Progression + ShowMeYourHands + EPC (1.443)

2944488802 (323), 2861806869 (306), 3590863552 (301), 2475965842 (264), 735106432 (249).

### Task 16 — B11: Simple sidearms + Stonecutting + VFE Pirates + Landforms + Social + Customize Weapon (1.380)

927155256 (241), 2571676542 (231), 2723801948 (231), 2773943594 (228), 2439736083 (227), 3550585103 (222).

### Task 17 — B12: VMF + Search & Rescue + Android + DPA + VFEM2 + AllowTool + CE Guns (1.350)

3426502333 (217), 3796056278 (214), 2975771801 (213), 2038874626 (194), 3444347874 (179), 761421485 (171), 3565025938 (162).

### Task 18 — B13: 11 alvos (1.450)

House Doyle (158), Planning Extended (156), VAE Animals (146), Designator Shapes (144), WVC Work Modes (134), Landmarks (132), Achtung! (122), Nice Health Tab (121), VEE (114), Faction Elves (113), Nice Inventory Tab (110).

### Task 19 — B14: 18 alvos (1.466)

Vanilla Books (106), JecsTools (104), Processor Framework (99), VAE Apparel (98), VEF (90), Common Sense (89), Tasty Armory Core (89), VFEPower (84), Research Tree (81), Quarry (76), Performance Optimizer (72), VFESecurity (71), Animals Logic (69), OgreStack (69), VPE Hemosage (69), BetterPawnControl (68), Nice Bill Tab (67), Vanilla Outposts (65).

### Task 20 — B15: 46 alvos (1.491)

Bloco de mods pequenos e médios (VFEArchitect, VFEEmpire, Dual Wield, Work Tab, Neat Storage, Smart Medicine, XML Extensions, Vehicle Framework, VRE Waster, VCookE, Adaptive Storage, Days Matter, Won hair, CE Attachments/Melee, Fishing, VArme, VFECore, VFEClassical, VRESanguophage, VFESettlers, InventoryTab, Visual XML Patches, Animal Gear, Succulents, LightsOut, Better Gene Inheritance, CE Armors, Highmate, Smarter Deconstruction, VWEGrenades, Yayo's Caravan, Pawn Target Fix, VFESpacer, Phytokin, Fridge, Bunk Beds, Blood Animations, Anomaly Gravship).

### Task 21 — B16: cauda de 29 alvos (161)

Mods de 1–13 chaves (Priority Treatment, Shoo!, Realistic Rooms, Vanilla Brewing, VFEMedical, Damage Indicators, Hussar, Show Me Your Tools, Mine Sight, Saurid, Cleaning Speed, Haul After Slaughter, Search and Destroy, Run and Hide, Drug Policy Fix, Genie, WMBP, Joint Battles, Snow IS Beautiful, Auto-Cut Blight, No Quality Filter, VFEArt, Automatic Night Owl, Better Trees/Mountains, VFEFarming, Wololoo, Aspirations, VVE). Um subagente por mod.

### Task 22 — Fechamento

**Files:**
- Modify: `README.md`, `docs/traducao-total/INVENTORY.md` (regerado), `tools/targets.json` (regerado)

- [ ] **Step 1: Rodar o inventariador de novo**

Run: `python3 tools/coverage.py`
Expected: `alvos 0 | chaves 0` (só os excluídos PT-OWN/RimHUD permanecem fora; se sobrar alvo, ele vira novo lote).

- [ ] **Step 2: Validação global**

```bash
find Languages Patches -name '*.xml' -exec xmllint --noout {} +
git diff --check
```
Expected: zero erros.

- [ ] **Step 3: Atualizar README e inventário final**

Substituir a tabela de mods por: lista completa (link `docs/traducao-total/INVENTORY.md`) + contagem final (139 alvos, ~26 mil chaves, exclusões PT-OWN justificadas).

- [ ] **Step 4: Commit final**

```bash
git add README.md docs/traducao-total/INVENTORY.md tools/targets.json
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "docs: README e inventário finais da tradução total"
```

---

## Self-Review

- **Cobertura do estado atual:** fantasmas removidos (T1), README (T2, T22), ferramenta de gate (T3), integração (T4), glossário (T5), 139 alvos em 16 lotes (T6–T21), fechamento (T22). Os 18 PT-OWN + RimHUD ficam documentados como excluídos em `targets.json`.
- **Placeholders:** nenhum TBD; comandos e código completos; contagens vêm de auditoria de 2026-09-15 e são revalidadas por `tools/coverage.py`.
- **Consistência:** `load_targets()` definida na T4 é consumida pelo validador na mesma task; `targets.json` da T3 é a única fonte de lotes; prefixos gerados deterministicamente.
- **Riscos conhecidos (aceitos):** mods atualizam na Workshop durante a campanha (rerodar T3 regera lotes); `Alpha Animals`/`VPE` já têm parte traduzida (o extrator só emite lacunas); VRE Hussar tem 1 XML de GeneDef malformado na própria fonte, ignorado pelo extrator com aviso (o lote B16 cobre o que é parseável); strings dentro de `.dll` permanecem em inglês (limitação do formato, fora do escopo).
