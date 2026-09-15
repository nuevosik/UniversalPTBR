# Campanha de Tradução Medieval (PT-BR) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Traduzir 100% dos campos escalares (label/description/etc.) dos 40 alvos medievais instalados para PT-BR, com validação automática e revisão humana por lote.

**Architecture:** Pipeline de scripts stdlib: extrator gera esqueletos DefInjected a partir dos Defs dos mods instalados; glossário trava terminologia; agentes traduzem in-place; validador acusa chave órfã e placeholder divergente. Entrega em lotes revisados e commitados.

**Tech Stack:** Python 3 (stdlib), xmllint, git. Sem dependências novas.

**Spec:** `docs/medieval/2026-09-14-campanha-medieval-design.md`

## Global Constraints

- Fonte dos mods: `/home/ngix/.local/share/Steam/steamapps/workshop/content/294100/<folderId>`
- Só editar valores traduzidos; nunca renomear chaves, `defName`s, arquivos ou pastas.
- Preservar: `{0}`, `{PAWN_*}`, `[TOKEN]`, `\n`, entidades XML (`&gt;`, `&amp;`), encoding UTF-8 e BOM quando existir.
- Seguir `docs/medieval/GLOSSARY.md`; novos termos de domínio vão pro `cSpell.words` em `.vscode/settings.json`.
- Antes de cada commit: `xmllint --noout` nos XMLs tocados, `git diff --check`, `git status --short` sem sobras.
- Fase 1: só campos da whitelist. Listas (`<li>`/rulePacks) e DLL ficam fora.
- Precondição: working tree limpo antes de começar (`git status --short`); mudanças pendentes não relacionadas (ex.: fix VCE) devem ser commitadas antes.
- Commit só depois de revisão humana do lote; identidade: `git -c user.name=OpenCode -c user.email=opencode@universal-ptbr`.
- Conventional commits em PT: `feat(lang): traduz <lote> (PT-BR)`.

## File Structure

| Arquivo | Responsabilidade |
|---|---|
| `tools/extract_medieval.py` | Varre mods-alvo, gera esqueletos DefInjected, monta o INVENTORY |
| `tools/validate_medieval.py` | Valida chaves contra o mod fonte + placeholders + XML |
| `docs/medieval/INVENTORY.md` | Tabela: folder id, packageId, contagem por campo, status |
| `docs/medieval/GLOSSARY.md` | Termos EN→PT aprovados |
| `Languages/PortugueseBrazilian/DefInjected/<DefType>/<Prefix>_<DefType>.xml` | Esqueletos e traduções finais |

---

### Task 1: Extrator de esqueletos

**Files:**
- Create: `tools/extract_medieval.py`
- Test: fixture sintética em `/tmp/opencode/fixture-mod/` e `/tmp/opencode/fixture-repo/`

**Interfaces:**
- Consumes: nada
- Produces: CLI `python3 tools/extract_medieval.py (--mod <folderId|path>... | --batch <L> | --all) --out <dir> [--repo <langDir>] [--prefix <Nome>] [--keyed] [--inventory <md>]`. `--mod` aceita folderId (resolve em `WORKSHOP`) ou caminho direto; `--prefix` é obrigatório quando o caminho não está no mapa `MODS`; `--keyed` extrai chaves do `Languages/English` (fase 2). Saída no formato do repo.

- [ ] **Step 1: Criar fixture de teste**

```bash
mkdir -p /tmp/opencode/fixture-mod/Defs /tmp/opencode/fixture-repo/Languages/PortugueseBrazilian/DefInjected/ThingDef
cat > /tmp/opencode/fixture-mod/Defs/Test.xml <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<Defs>
  <ThingDef Abstract="True" Name="BaseTest">
    <label>base</label>
  </ThingDef>
  <ThingDef>
    <defName>TestSword</defName>
    <label>test sword</label>
    <description>A sword with {0} damage and\na point.</description>
  </ThingDef>
</Defs>
XML
printf '<?xml version="1.0" encoding="utf-8"?>\n<LanguageData>\n  <TestSword.label>espada de teste</TestSword.label>\n</LanguageData>\n' > /tmp/opencode/fixture-repo/Languages/PortugueseBrazilian/DefInjected/ThingDef/Existing.xml
```

- [ ] **Step 2: Rodar o extrator e verificar que falha**

Run: `python3 tools/extract_medieval.py --mod /tmp/opencode/fixture-mod --prefix Fixture --out /tmp/opencode/fixture-out --repo /tmp/opencode/fixture-repo`
Expected: falha (`FileNotFoundError`/`no such file`) porque o script não existe.

- [ ] **Step 3: Implementar o extrator**

Contrato (stdlib only):

```python
#!/usr/bin/env python3
"""Gera esqueletos DefInjected a partir dos Defs de mods instalados."""
import argparse, pathlib, re, xml.etree.ElementTree as ET

WORKSHOP = pathlib.Path.home()/'.local/share/Steam/steamapps/workshop/content/294100'
REPO_LANG = pathlib.Path('Languages/PortugueseBrazilian')

FIELDS = {'label','description','labelFemale','labelPlural','labelNoun','jobString',
          'verb','gerund','letterText','reportString','text','title','summary','tip'}

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
```

Regras de extração: parsear todo `*.xml` fora de `Languages/`; para cada elemento com filho `<defName>`: tipo = tag do elemento; pular `Abstract="True"`; pegar só filhos diretos na whitelist; chave `<defName>.<campo>`; valor = texto do campo. Pular chave já existente em `REPO_LANG/**` (parsear tags de todos os XMLs e `Keyed`). Agrupar por tipo em `DefInjected/<DefType>/<prefixo>_<DefType>.xml` com declaração UTF-8, indentação de 2 espaços e uma entrada por linha. `--inventory` monta a tabela com contagem por campo e status.

- [ ] **Step 4: Rodar na fixture e verificar sucesso**

Run: `python3 tools/extract_medieval.py --mod /tmp/opencode/fixture-mod --prefix Fixture --out /tmp/opencode/fixture-out --repo /tmp/opencode/fixture-repo`
Expected: `DefInjected/ThingDef/Fixture_ThingDef.xml` com **apenas** `<TestSword.description>` (o `label` é pulado por já existir no repo; o `Abstract` é ignorado).

```bash
grep -c '<TestSword' /tmp/opencode/fixture-out/DefInjected/ThingDef/Fixture_ThingDef.xml   # esperado: 1
grep -c 'description' /tmp/opencode/fixture-out/DefInjected/ThingDef/Fixture_ThingDef.xml  # esperado: 1
```

- [ ] **Step 5: Smoke nos mods reais + commit**

```bash
python3 tools/extract_medieval.py --batch L1 --out /tmp/opencode/skel-L1
find /tmp/opencode/skel-L1 -name '*.xml' -exec xmllint --noout {} +   # esperado: sem erros
git add tools/extract_medieval.py
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(tools): extrator de esqueletos DefInjected"
```

---

### Task 2: Validador

**Files:**
- Create: `tools/validate_medieval.py`
- Test: fixture da Task 1

**Interfaces:**
- Consumes: esqueletos/traduções gerados e os mods fonte (`MODS` importado do extrator)
- Produces: CLI `python3 tools/validate_medieval.py --batch <lote> [--mod <folderId|path>] [--prefix <Nome>] [--repo <dir>] [--keyed]`; exit 0 = OK, 1 = falhas; imprime `OK <n> chaves` ou lista de falhas (`chave órfã`, `placeholder divergente`, `valor vazio`, `XML inválido`).

- [ ] **Step 1: Teste que falha — criar esqueleto válido e corromper cópia**

```bash
cp -r /tmp/opencode/fixture-out /tmp/opencode/fixture-bad
# trocar o placeholder {0} por {1} no valor gerado
sed -i 's/{0}/{1}/' /tmp/opencode/fixture-bad/DefInjected/ThingDef/Fixture_ThingDef.xml
python3 tools/validate_medieval.py --mod /tmp/opencode/fixture-mod --prefix Fixture --repo /tmp/opencode/fixture-bad
```
Expected: exit 1 com `placeholder divergente: TestSword.description`.

- [ ] **Step 2: Implementar**

Para cada chave `defName.campo` nos arquivos-alvo: indexar o mod fonte (`defName` → campos presentes) e comparar o multiset de placeholders (`\{[^}]+\}`) do valor atual com o do inglês fonte; se o def/campo não existir na fonte → `chave órfã`; se XML inválido → `XML inválido`. Reportar tudo e sair 1 se houver falha.

- [ ] **Step 3: Rodar validador nos dois casos**

Run: `python3 tools/validate_medieval.py --mod /tmp/opencode/fixture-mod --prefix Fixture --repo /tmp/opencode/fixture-out`
Expected: `OK 1 chaves` (exit 0).
Run: `python3 tools/validate_medieval.py --mod /tmp/opencode/fixture-mod --prefix Fixture --repo /tmp/opencode/fixture-bad`
Expected: exit 1 com a falha do passo 1.

- [ ] **Step 4: Commit**

```bash
git add tools/validate_medieval.py
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(tools): validador DefInjected (chave órfã + placeholder)"
```

---

### Task 3: Inventário

**Files:**
- Create: `docs/medieval/INVENTORY.md`

**Interfaces:**
- Consumes: `tools/extract_medieval.py --inventory`
- Produces: tabela por alvo: folder id, packageId, nome, labels, descriptions, total, status (`sem`/`parcial`/`coberto`), ativo no `ModsConfig`, lote.

- [ ] **Step 1: Gerar**

Run: `python3 tools/extract_medieval.py --all --inventory docs/medieval/INVENTORY.md --out /tmp/opencode/skel-all`

- [ ] **Step 2: Conferir totais contra o design**

Expected: 40 linhas; soma de labels+descriptions ≈ **9.377**; mods `MORoyalty`, `MOBarbarians`, `HouseVanIlla`, `Roxmont`, `Ignivar`, `MOTweaks`, `AdaptiveStorage`, `RimFantasyMO` presentes.

- [ ] **Step 3: Commit**

```bash
git add docs/medieval/INVENTORY.md
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "docs: inventário dos alvos medievais"
```

---

### Task 4: Glossário (gate de aprovação humana)

**Files:**
- Create: `docs/medieval/GLOSSARY.md`
- Modify: `.vscode/settings.json` (cSpell.words)

**Interfaces:**
- Consumes: strings extraídas (esqueletos)
- Produces: mapa EN→PT aprovado usado por todos os lotes.

- [ ] **Step 1: Extrair termos recorrentes**

Run: `python3 - <<'EOF'` — contar palavras EN (lowercase, ≥4 letras, sem stopwords) nos valores dos esqueletos e listar top 80 com frequência.
Expected: candidatos como `keep`, `guild`, `barbarian`, `heraldry`, `manor`, `stew`.

- [ ] **Step 2: Redigir `GLOSSARY.md`**

Seções: **Termos de jogo** (label/UI), **Materiais/armas**, **Facções/títulos**, **Verbos de receita/Job**. Formato: `| EN | PT-BR | Obs |`. Regra: termo único por conceito; se o repo já tiver termo (ex.: `gravinave`), herdar.

- [ ] **Step 3: GATE — apresentar ao humano**

Mostrar a tabela completa e **parar**. Só continuar depois do "aprovado" (ajustes voltam pro Step 2).

- [ ] **Step 4: Aplicar no cSpell e commitar**

```bash
git add docs/medieval/GLOSSARY.md .vscode/settings.json
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "docs: glossário medieval aprovado"
```

---

## Padrão dos lotes de tradução (Tasks 5–14)

Cada lote repete o ciclo abaixo; a tabela do lote muda as entradas.

1. **Extrair:** `python3 tools/extract_medieval.py --batch <B> --out Languages/PortugueseBrazilian`
2. **Validar esqueleto:** `python3 tools/validate_medieval.py --batch <B>` → `OK`
3. **Traduzir (subagentes paralelos, 1 por mod):** cada subagente recebe o glossário + constraints globais + a lista de arquivos do mod; traduz **in-place**, uma entrada por linha, preservando chaves/placeholders/indentação; não toca arquivos fora do lote.
4. **Validar tradução:** validador (`OK`) + `find <arquivos do lote> -exec xmllint --noout {} +` + `git diff --check`
5. **GATE — revisão humana:** apresentar `git diff --stat` + amostra (10 strings EN→PT) + falhas; **parar** até o "ok".
6. **Commit:** `git add <arquivos do lote>` + `git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(lang): traduz <lote> (PT-BR)"`

### Task 5 — Lote L1 (quick wins, 16 mods, ~267 strings)
Batch: `L1` — Walls, Signs, Transport, Geysers, Hornetkeeping, coffin, Medicines, Extra Signs, Space Knights, Coastal Outfits, DBH, ReGrowth, Overlap Remover, Anomaly.

### Task 6 — Lote L2a (Houses + Tweaks + Adaptive, ~969 strings)
Batch: `L2a` — House Van Illa (262), Roxmont (186), Ignivar (136), MO Tweaks (278), Adaptive Storage (107).

### Task 7 — Lote L2b (MO Royalty, ~881 strings)
Batch: `L2b`.

### Task 8 — Lote L2c (MO Barbarians, ~1.023 strings)
Batch: `L2c`.

### Task 9 — Lote L3a (small standalone, ~538 strings)
Batch: `L3a` — Gene Assembler, Backstories Patch, Dark Ages, Implants, Hunts, Fort Medieval, Rare Resources, Trader Airships.

### Task 10 — Lote L3b (medium standalone, ~1.178 strings)
Batch: `L3b` — Tasty Armory, Tailor, Fort Material, Quest Rewards, Relic Quests.

### Task 11 — Lote L4a (RimFantasy MO Edition, ~1.729 strings)
Batch: `L4` (só `2836791007`).

### Task 12 — Lote L4b (RimTraits Medieval Talents, ~1.013 strings)
Batch: `L4` (só `1916352291`).

### Task 13 — Lote L4c (Medieval Prosthetics, ~863 strings)
Batch: `L4` (só `2101545242`).

### Task 14 — Lote L4d (Medieval Medicines MO Edition, ~918 strings)
Batch: `L4` (só `2883228057`) — completar lacunas do pacote parcial existente.

---

### Task 15: Fase 2 — Keyed (10 mods com English)

**Files:**
- Create: `Languages/PortugueseBrazilian/Keyed/<Prefix>_Keys.xml`
- Test: `tools/validate_medieval.py --keyed`

**Interfaces:**
- Consumes: `Languages/English/Keyed/*.xml` dos mods `MORoyalty`, `MOTweaks`, `GeneAssembler`, `HouseVanIlla`, `AdaptiveStorage`, `TraderAirships`, `Geysers`, `QuestRewards`, `RelicQuests`, `OverlapRemover`
- Produces: Keyed PT-BR com **exatamente** o mesmo conjunto de chaves do English.

- [ ] **Step 1: Extrair chaves English**

Run: script do extrator em modo `--keyed` → um arquivo por mod com as chaves do English e valor vazio.

- [ ] **Step 2: Teste de integridade (falha esperada antes de traduzir)**

Run: `python3 tools/validate_medieval.py --keyed`
Expected: falha `valor vazio: <chave>` em todas (prova que o check funciona).

- [ ] **Step 3: Traduzir (subagentes por mod, glossário)**

- [ ] **Step 4: Validar + `xmllint` + `git diff --check`** → `OK`, nenhuma chave do English sem correspondência.

- [ ] **Step 5: GATE — revisão humana** (mesmo padrão dos lotes).

- [ ] **Step 6: Commit**

```bash
git add Languages/PortugueseBrazilian/Keyed
git -c user.name=OpenCode -c user.email=opencode@universal-ptbr commit -m "feat(lang): Keyed fase 2 dos mods medievais (PT-BR)"
```

---

## Self-Review (feito)

- **Cobertura da spec:** extração (Tasks 1/3), validação (2), glossário (4), lotes L1–L4 (5–14), fase 2 Keyed (15) — todas as seções da spec têm task.
- **Placeholders:** nenhum TBD; todos os comandos e contratos estão explícitos.
- **Consistência:** `BATCHES`/`MODS` definidos na Task 1 e reutilizados nas demais; validador consome o mesmo índice.
- **Gap conhecido:** o gate de glossário (Task 4) bloqueia as traduções de propósito.
