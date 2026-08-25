# UniversalPTBR — Pipeline 4 Agentes DMS + World Domination 2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Renomear `VanillaExpandedPTBR` para `UniversalPTBR` e entregar traduções PT-BR completas para `The Dead Man's Switch` (3121742525) e `World Domination 2.0` (3680501610) via pipeline de 4 agentes especializados, sem quebrar `xmllint`/placeholders/`loadAfter`.

**Architecture:** Pipeline sequencial `Extrator → Tradutor → Integrador → Validador` com artefatos em `/tmp/universal-ptbr/` e barrier por estágio; DMS e WD2 paralelizáveis dentro de cada agente. Agente 3 é o único escritor no repo; Agente 4 é gate bloqueante. Rename é commit isolado com tag `pre-universal`.

**Tech Stack:** XML RimWorld `LanguageData`/`PatchOperation`, `xmllint 2.15.3`, `rg` (ripgrep), `python3` (placeholder diff), `steamcmd`/`unzip`, `git`, `bash`, `cSpell` (`.vscode/settings.json`)

**Spec:** `docs/superpowers/specs/2026-08-25-universal-ptbr-design.md`

## Global Constraints

- Editar somente valores traduzidos, nunca `defName`, keys, arquivos ou diretórios existentes fora do escopo DMS/WD2.
- Preservar verbatim: `{0}`/`{1}`/`{PAWN_name}`/`{PAWN_possessive}`/`[TOKEN]`/`\n`/tags XML/`LanguageData` estrutura.
- Manter termos canônicos RimWorld quando PT-BR perderia referência (`pawn`, `hediff`, `xenotype`, `hemogen`, `gravship` → `gravinave` já consagrado em `Gravship_Keys.xml:176`).
- PT-BR: acentuação/regência/concordância, gênero/plural consistente por `DefInjected` grupo.
- `README.md` não é texto in-game — não editar como tradução.
- `DefInjected` key = `<DefName>.<field>` typo = falha silenciosa.
- `Patches/` usa `PatchOperationFindMod` + `PatchOperationReplace` com XPath `Defs/GeneDef[defName="..."]/label` exato.
- Encoding: XML `utf-8` sem BOM; TXT com BOM preservado.
- Validar com `xmllint --noout` antes de commit; `git diff --check` limpo.
- Classificar antes de editar: `rg` triage tem falsos positivos em nomes técnicos/procedurais — sem substituição global cega.

---

## File Structure

**Created:**
- `docs/superpowers/plans/2026-08-25-universal-ptbr-plan.md` (este plano)
- `/tmp/universal-ptbr/manifest-dms.json` (Agente 1 output)
- `/tmp/universal-ptbr/manifest-wd2.json`
- `/tmp/universal-ptbr/draft/DMS/DefInjected/**/*.xml` (Agente 2)
- `/tmp/universal-ptbr/draft/WD2/DefInjected/**/*.xml`
- `/tmp/universal-ptbr/draft/DMS/Keyed/DMS_Keys.xml`
- `/tmp/universal-ptbr/draft/WD2/Keyed/WD2_Keys.xml`
- `/tmp/universal-ptbr/glossario.csv` + `glossario-delta.csv`
- `Languages/PortugueseBrazilian/DefInjected/**/DMS_*.xml` (Agente 3, ~8 arquivos)
- `Languages/PortugueseBrazilian/DefInjected/**/WD2_*.xml` (~5 arquivos)
- `Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml`
- `Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml`
- `Patches/Patch_DMS_*.xml` (0-2 arquivos, se necessário)
- `Patches/Patch_WD2_*.xml`
- `/tmp/universal-ptbr/validation-report.md` (Agente 4)

**Modified:**
- `About/About.xml:1-95` — rename `name`/`packageId`/`description`/`loadAfter`
- `.vscode/settings.json` — adicionar `cSpell.words` se faltarem termos DMS/WD2
- `README.md` — nota de migração (única edição permitida)

**Untouched (referência):**
- `LoadFolders.xml:1` — permanece `<v1.6><li>/</li></v1.6>`
- `Languages/PortugueseBrazilian/LanguageInfo.xml`
- `Languages/PortugueseBrazilian/DefInjected/**` existente (VE)
- `Languages/PortugueseBrazilian/Keyed/**` existente

---

### Task 1: Rename VanillaExpandedPTBR → UniversalPTBR (chore)

**Files:**
- Modify: `About/About.xml:1-15`
- Modify: `README.md` (seção topo)
- Modify: `.vscode/settings.json` (se necessário)
- Create: git tag `pre-universal`

**Interfaces:**
- Consumes: Spec Seção 1, `About/About.xml` original, `git log`
- Produces: `About/About.xml` renomeado para Tasks 2-5 consumirem; tag `pre-universal` para rollback

- [ ] **Step 1: Registrar estado sujo e criar tag de segurança**

```bash
git status --short > /tmp/pre-universal-status.txt
cat /tmp/pre-universal-status.txt
# Deve mostrar 60+ M (trabalho VE pré-existente) — não commitar esses M agora
git tag pre-universal HEAD
git tag -l pre-universal
```

- [ ] **Step 2: Verificar About.xml atual antes do rename**

```bash
cat About/About.xml | head -n 15
# Esperado: <name>Tradução Vanilla Expanded (PT-BR)</name>
#           <packageId>GitHubVersion.TraducaoVanillaExpanded.PTBR</packageId>
xmllint --noout About/About.xml && echo "About.xml válido"
```

- [ ] **Step 3: Editar About.xml (único arquivo breaking)**

```xml
<!-- About/About.xml:1 — substituir -->
<name>Tradução Universal (PT-BR)</name>
<packageId>GitHubVersion.TraducaoUniversal.PTBR</packageId>
<description>Tradução para Português Brasileiro — Vanilla Expanded + mods universais curados (The Dead Man's Switch, World Domination 2.0 e mais). Em constante atualização para abranger todo o conteúdo disponível.</description>
<!-- loadAfter: manter ordem VE, adicionar ao final -->
<li>Aoba.DeadMansSwitch</li>
<li>LikewiseHH.WorldDomination2</li>
```

Aplicar via `edit` com `oldString` exato de `About/About.xml:3-4` e `About/About.xml:10-11` e inserir os dois `<li>` antes de `</loadAfter>` em `About/About.xml:94`.

- [ ] **Step 4: Validar rename**

```bash
xmllint --noout About/About.xml && echo "OK"
grep -n "Tradução Universal" About/About.xml
grep -n "GitHubVersion.TraducaoUniversal.PTBR" About/About.xml
grep -n "Aoba.DeadMansSwitch" About/About.xml
grep -n "WorldDomination2" About/About.xml
```

- [ ] **Step 5: Atualizar README.md (nota de migração, não tradução)**

Adicionar no topo do `README.md` após título:

```markdown
> **Migrado para UniversalPTBR:** este repositório foi renomeado de `VanillaExpandedPTBR` para `UniversalPTBR` (`packageId` novo: `GitHubVersion.TraducaoUniversal.PTBR`). O item antigo da Workshop recebeu redirect. Assine o novo item.
```

- [ ] **Step 6: Commit isolado do rename**

```bash
git add About/About.xml README.md
git diff --cached --stat
git diff --check
git commit -m "chore: rename VanillaExpandedPTBR → UniversalPTBR

- About.xml: name/packageId/description/loadAfter +2 mods (DMS, WD2)
- README: nota de migração
- tag pre-universal para rollback
- BREAKING CHANGE: packageId GitHubVersion.TraducaoUniversal.PTBR"
```

---

### Task 2: Agente 1 — Extrator Minerador (DMS + WD2 manifests)

**Files:**
- Create: `/tmp/universal-ptbr/manifest-dms.json`
- Create: `/tmp/universal-ptbr/manifest-wd2.json`
- Create: `/tmp/universal-ptbr/extractor-report.md`

**Interfaces:**
- Consumes: Workshop ZIPs 3121742525 + 3680501610, `About/About.xml` pós-Task1
- Produces: `manifest-*.json` com `{packageId, supportedVersions, defTypes[], keyedKeys[], placeholderInventory}` para Task3 consumir

- [ ] **Step 1: Preparar diretório e baixar mods**

```bash
mkdir -p /tmp/universal-ptbr
# Tentar steamcmd (se instalado), fallback para download manual
which steamcmd && steamcmd +login anonymous +workshop_download_item 294100 3121742525 +workshop_download_item 294100 3680501610 +quit || echo "steamcmd não encontrado — baixar zips manualmente para /tmp/universal-ptbr/"
ls -lh /tmp/universal-ptbr/
# Esperado: DMS em ~/Steam/steamapps/workshop/content/294100/3121742525/ ou /tmp/universal-ptbr/dms.zip
```

Se ambos os Workshop retornarem "removed due to violation" (caso do fetch), usar `curl -L` no `db.rimworld` ou pedir ao usuário zip manual — não bloquear, registrar em `extractor-report.md`.

- [ ] **Step 2: Extrair packageId real e supportedVersions de cada mod**

```bash
# Para cada mod descompactado em /tmp/universal-ptbr/dms/ e /tmp/universal-ptbr/wd2/
grep -H "<packageId>" /tmp/universal-ptbr/dms/About/About.xml
grep -H "<packageId>" /tmp/universal-ptbr/wd2/About/About.xml
grep -A2 "<supportedVersions>" /tmp/universal-ptbr/dms/About/About.xml
grep -A2 "<supportedVersions>" /tmp/universal-ptbr/wd2/About/About.xml
# Anotar valores exatos — usar esses valores no About.xml loadAfter, não assumir "Aoba.DMS"
```

- [ ] **Step 3: Catalogar Defs e Keyed (gerar manifests)**

```bash
# DMS
find /tmp/universal-ptbr/dms/Defs -name "*.xml" | head -n 20
rg -n "defName" /tmp/universal-ptbr/dms/Defs --no-heading | wc -l
find /tmp/universal-ptbr/dms/Languages/English -name "*.xml" | head -n 20

# WD2
find /tmp/universal-ptbr/wd2/Defs -name "*.xml" | wc -l
find /tmp/universal-ptbr/wd2/Languages/English -name "*.xml"

# Gerar JSON via python3
python3 << 'PY'
import json, pathlib, re, glob
for mod, path in [("dms","/tmp/universal-ptbr/dms"), ("wd2","/tmp/universal-ptbr/wd2")]:
    defs = glob.glob(f"{path}/Defs/**/*.xml", recursive=True)
    keyed = glob.glob(f"{path}/Languages/English/Keyed/**/*.xml", recursive=True)
    manifest = {"mod": mod, "defs": defs[:50], "defCount": len(defs), "keyed": keyed, "keyedCount": len(keyed)}
    open(f"/tmp/universal-ptbr/manifest-{mod}.json","w").write(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"{mod}: {len(defs)} Defs, {len(keyed)} Keyed")
PY
cat /tmp/universal-ptbr/manifest-dms.json
cat /tmp/universal-ptbr/manifest-wd2.json
```

- [ ] **Step 4: Inventariar placeholders (baseline para Validador)**

```bash
rg -o "\{[0-9]+\}|\{PAWN[^}]+\}|\[TOKEN\]|\\n" /tmp/universal-ptbr/dms/Languages/English --no-heading | sort | uniq -c > /tmp/universal-ptbr/placeholders-dms.txt
rg -o "\{[0-9]+\}|\{PAWN[^}]+\}|\[TOKEN\]|\\n" /tmp/universal-ptbr/wd2/Languages/English --no-heading | sort | uniq -c > /tmp/universal-ptbr/placeholders-wd2.txt
cat /tmp/universal-ptbr/placeholders-dms.txt
cat /tmp/universal-ptbr/placeholders-wd2.txt
```

- [ ] **Step 5: Validar XML original e escrever relatório**

```bash
find /tmp/universal-ptbr/dms -name "*.xml" -exec xmllint --noout {} + && echo "DMS XML OK"
find /tmp/universal-ptbr/wd2 -name "*.xml" -exec xmllint --noout {} + && echo "WD2 XML OK"
cat > /tmp/universal-ptbr/extractor-report.md << 'MD'
# Extractor Report
- DMS packageId: (colado do grep)
- WD2 packageId: (colado)
- DMS Defs: N, Keyed: N
- WD2 Defs: N, Keyed: N
- Placeholders DMS: ver placeholders-dms.txt
- Placeholders WD2: ver placeholders-wd2.txt
MD
cat /tmp/universal-ptbr/extractor-report.md
```

---

### Task 3: Agente 2 — Tradutor PT-BR (drafts em /tmp)

**Files:**
- Create: `/tmp/universal-ptbr/glossario.csv`
- Create: `/tmp/universal-ptbr/draft/DMS/DefInjected/**/*.xml`
- Create: `/tmp/universal-ptbr/draft/WD2/DefInjected/**/*.xml`
- Create: `/tmp/universal-ptbr/draft/DMS/Keyed/DMS_Keys.xml`
- Create: `/tmp/universal-ptbr/draft/WD2/Keyed/WD2_Keys.xml`
- Create: `/tmp/universal-ptbr/glossario-delta.csv`

**Interfaces:**
- Consumes: `manifest-*.json` + `placeholders-*.txt` + `Languages/PortugueseBrazilian/Keyed/Gravship_Keys.xml:176` (seed glossário)
- Produces: drafts em `/tmp` para Task4 materializar; nunca escreve em `Languages/`

- [ ] **Step 1: Semear glossário a partir do repo existente**

```bash
cat > /tmp/universal-ptbr/glossario.csv << 'CSV'
termo_en,termo_pt,fonte,notas
gravship,gravinave,Gravship_Keys.xml:176,consagrado no repo — não usar navegrav
gravship artillery,artilharia da gravinave,Gravship_Keys.xml:4,manter artigo
hemogen,hemogênio,AGENTS.md:13,com acento
xenotype,xenotipo,AGENTS.md:13,
hediff,hediff,AGENTS.md:13,não traduzir quando técnico
pawn,peão/colonista,AGENTS.md:13,colonista para UI, peão só se técnico
mechanoid,mecanoide,DMS,padronizar com VQE
exoskeleton,exo-esqueleto,DMS,
outpost,posto avançado,WD2,verificar consistência com Vanilla Outposts
caravan,caravana,WD2,
CSV
cat /tmp/universal-ptbr/glossario.csv
# Adicionar cSpell delta se novos termos: gravinave, hemogênio, criptoforja, astrocombustível, gravidados, mecanoides
```

- [ ] **Step 2: Traduzir DMS — DefInjected (um arquivo por DefType)**

Para cada `DefType` em `manifest-dms.json` (ex.: `ThingDef`, `GeneDef`, `HediffDef`):

```xml
<!-- /tmp/universal-ptbr/draft/DMS/DefInjected/ThingDef/DMS_ThingDef.xml -->
<?xml version="1.0" encoding="utf-8" ?>
<LanguageData>
  <DMS_Mech_Tarbosaurus.label>tarbossauro mecanizado</DMS_Mech_Tarbosaurus.label>
  <DMS_Mech_Tarbosaurus.description>Unidade pesada de assalto da Nara Industries. Equipe com armas pesadas via clique direito quando o mecanoide estiver selecionado.</DMS_Mech_Tarbosaurus.description>
  <!-- Preservar {0} e \n verbatim — nunca traduzir placeholders -->
</LanguageData>
```

Regra: copiar `defName` do manifest, traduzir só `<label>`/`<description>`; validar `rg "\{[0-9]+\}"` igual ao original.

- [ ] **Step 3: Traduzir DMS — Keyed**

```bash
# Ler /tmp/universal-ptbr/dms/Languages/English/Keyed/*.xml, gerar /tmp/universal-ptbr/draft/DMS/Keyed/DMS_Keys.xml
# Cada <Key>valor</Key> → traduzir valor, preservar key
# Exemplo: <DMS_EquipMechWeapon>Equipar arma mecanizada</DMS_EquipMechWeapon>
# Placeholder check: rg -o "\{[0-9]+\}" draft vs original deve bater
```

- [ ] **Step 4: Traduzir WD2 — DefInjected + Keyed + Settings**

WD2 tem forte `Keyed` de outposts/caravanas + `ModSettings`:

```xml
<!-- /tmp/universal-ptbr/draft/WD2/Keyed/WD2_Keys.xml -->
<LanguageData>
  <WD_OutpostEstablished>Posto avançado estabelecido em {0}.</WD_OutpostEstablished>
  <WD_CaravanLaunched>Caravana lançada de {0} para {1}.</WD_CaravanLaunched>
  <WD_GoodwillIncreased>Boa vontade com {0} aumentada em {1}.</WD_GoodwillIncreased>
</LanguageData>
```

- [ ] **Step 5: Revisar consistência interna e gerar delta**

```bash
# Conferir que "posto avançado" aparece igual em DefInjected e Keyed
rg "posto avançado" /tmp/universal-ptbr/draft/WD2 --no-heading | wc -l
rg "gravinave" /tmp/universal-ptbr/draft --no-heading | head
# Escrever glossario-delta.csv com novos termos para .vscode/settings.json
cat > /tmp/universal-ptbr/glossario-delta.csv << 'CSV'
gravinave,hemogênio,astrocombustível,gravidados,mecanoides,exo-esqueleto,posto avançado,caravana
CSV
```

---

### Task 4: Agente 3 — Integrador (materializa no repo)

**Files:**
- Create: `Languages/PortugueseBrazilian/DefInjected/**/DMS_*.xml` (~8)
- Create: `Languages/PortugueseBrazilian/DefInjected/**/WD2_*.xml` (~5)
- Create: `Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml`
- Create: `Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml`
- Create: `Patches/Patch_DMS_*.xml` (se necessário, 0-2)
- Modify: `.vscode/settings.json` (cSpell.words)

**Interfaces:**
- Consumes: drafts de Task3 + `manifest-*.json` para XPath exato
- Produces: arquivos finais em `Languages/` e `Patches/` para Task5 validar

- [ ] **Step 1: Criar DefInjected DMS (um por DefType, sem BOM)**

```bash
mkdir -p Languages/PortugueseBrazilian/DefInjected/ThingDef
mkdir -p Languages/PortugueseBrazilian/DefInjected/GeneDef
# Para cada draft em /tmp/universal-ptbr/draft/DMS/DefInjected/**/:
cp /tmp/universal-ptbr/draft/DMS/DefInjected/ThingDef/DMS_ThingDef.xml Languages/PortugueseBrazilian/DefInjected/ThingDef/DMS_ThingDef.xml
# Repetir para HediffDef, RecipeDef, QuestScriptDef, etc.
# Validar cada um:
xmllint --noout Languages/PortugueseBrazilian/DefInjected/ThingDef/DMS_ThingDef.xml && echo "DMS ThingDef OK"
```

*Guardrail:* `DefInjected` key = `<DefName>.label` exato do manifest. `xmllint` por arquivo antes de próximo.

- [ ] **Step 2: Criar DefInjected WD2**

```bash
mkdir -p Languages/PortugueseBrazilian/DefInjected/WorldObjectDef
cp /tmp/universal-ptbr/draft/WD2/DefInjected/WorldObjectDef/WD2_Outposts.xml Languages/PortugueseBrazilian/DefInjected/WorldObjectDef/WD2_Outposts.xml
xmllint --noout Languages/PortugueseBrazilian/DefInjected/WorldObjectDef/WD2_Outposts.xml
```

- [ ] **Step 3: Criar Keyed DMS e WD2**

```bash
cp /tmp/universal-ptbr/draft/DMS/Keyed/DMS_Keys.xml Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml
cp /tmp/universal-ptbr/draft/WD2/Keyed/WD2_Keys.xml Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml
xmllint --noout Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml
xmllint --noout Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml
```

Não usar `Generated_*.xml` — usar prefixo `DMS_`/`WD2_` explícito.

- [ ] **Step 4: Criar Patches se necessário (padrão Patch_VRE_Starjack.xml:3)**

Só se algum `ThingDef` DMS não for injetável via `LanguageData` (ex.: `symbolPack`):

```xml
<!-- Patches/Patch_DMS_Symbols.xml -->
<?xml version="1.0" encoding="utf-8" ?>
<Patch>
  <Operation Class="PatchOperationFindMod">
    <mods><li>Aoba.DeadMansSwitch</li><li>The Dead Man's Switch</li></mods>
    <match Class="PatchOperationSequence">
      <operations>
        <li Class="PatchOperationReplace">
          <xpath>Defs/GeneDef[defName="DMS_Tarbosaurus"]/label</xpath>
          <value><label>tarbossauro</label></value>
        </li>
      </operations>
    </match>
  </Operation>
</Patch>
```

Validar: `xmllint --noout Patches/Patch_DMS_*.xml`

- [ ] **Step 5: Atualizar cSpell.words**

```bash
# Ler /tmp/universal-ptbr/glossario-delta.csv, adicionar faltantes em .vscode/settings.json:1
# Exemplo: "gravinave","hemogênio","astrocombustível","gravidados","mecanoides","exo-esqueleto","posto avançado"
# Validar JSON:
python3 -m json.tool .vscode/settings.json > /dev/null && echo "settings.json válido"
```

- [ ] **Step 6: Commit da integração**

```bash
git add Languages/PortugueseBrazilian/DefInjected/**/DMS_*.xml Languages/PortugueseBrazilian/DefInjected/**/WD2_*.xml Languages/PortugueseBrazilian/Keyed/DMS_*.xml Languages/PortugueseBrazilian/Keyed/WD2_*.xml Patches/Patch_DMS_*.xml Patches/Patch_WD2_*.xml .vscode/settings.json
git diff --cached --stat
git commit -m "feat(lang): add DMS + WD2 translations (UniversalPTBR)

- DefInjected DMS: ThingDef/GeneDef/HediffDef/QuestScriptDef
- DefInjected WD2: WorldObjectDef/SitePartDef
- Keyed DMS/WD2 com placeholders preservados
- Patches PatchOperationFindMod onde necessário
- cSpell.words atualizado"
```

---

### Task 5: Agente 4 — Validador QA (gate bloqueante)

**Files:**
- Create: `/tmp/universal-ptbr/validation-report.md`
- Read: `Languages/**`, `Patches/**`, `manifest-*.json`, `placeholders-*.txt`

**Interfaces:**
- Consumes: repo pós-Task4 + baseline Task2
- Produces: `validation-report.md`; bloqueia merge se falhar (retorna para Task3/4)

- [ ] **Step 1: XML válido (bulk + por arquivo)**

```bash
find Languages Patches -name "*.xml" -exec xmllint --noout {} + && echo "BULK OK"
xmllint --noout Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml && echo "DMS Keyed OK"
xmllint --noout Languages/PortugueseBrazilian/Keyed/WD2_Keys.xml && echo "WD2 Keyed OK"
xmllint --noout About/About.xml && echo "About OK"
# Falha = abortar e reportar caminho + linha do erro
```

- [ ] **Step 2: Comparar placeholders (não eyeball)**

```bash
python3 << 'PY'
import re, pathlib, subprocess, json
# Comparar manifest placeholders vs repo
for mod in ["DMS","WD2"]:
    keyed = pathlib.Path(f"Languages/PortugueseBrazilian/Keyed/{mod}_Keys.xml").read_text(encoding="utf-8")
    # Extrair placeholders do repo
    repo_ph = sorted(set(re.findall(r"\{[0-9]+\}|\{PAWN[^}]+\}|\[TOKEN\]", keyed)))
    print(f"{mod} repo placeholders: {repo_ph}")
    # Comparar com /tmp/universal-ptbr/placeholders-*.txt
PY
# Diferença = ERRO — placeholders devem bater 1:1 com original
```

- [ ] **Step 3: Reexecutar triagem Tarefa 2 (rg)**

```bash
rg "  |,,|\!\!|a nivel de|o mesmo" Languages/PortugueseBrazilian --no-heading | head -n 20
rg "[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+" Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml --no-heading | head -n 20
# Se inglês residual fora de nomes próprios → reportar, não auto-fix
```

- [ ] **Step 4: Higiene git**

```bash
git diff --check
git diff --stat
git status --short
# Deve mostrar só arquivos DMS/WD2 + About/README — não os 60+ M pré-existentes de VE
# Se misturar, abortar e pedir git stash dos M VE
```

- [ ] **Step 5: Smoke manual (opcional, 5min)**

```
1. RimWorld 1.6 + Harmony + VE Framework + DMS + WD2 + UniversalPTBR (load order: VE → DMS → WD2 → UniversalPTBR)
2. Novo save, verificar:
   - DMS: tarbossauro label aparece em PT-BR, exo-esqueleto equipável
   - WD2: aba WD dashboard em PT-BR, "Posto avançado estabelecido em {0}." aparece
3. Log sem vermelho
```

- [ ] **Step 6: Escrever relatório e dar veredito**

```bash
cat > /tmp/universal-ptbr/validation-report.md << 'MD'
# Validation Report — UniversalPTBR DMS+WD2
- xmllint bulk: PASS/FAIL (anexar erro)
- placeholders DMS: PASS/FAIL
- placeholders WD2: PASS/FAIL
- rg triagem: PASS/FAIL (listar ocorrências)
- git diff --check: PASS/FAIL
- smoke: PASS/FAIL
- Veredito: MERGE / BLOCK (com motivo)
MD
cat /tmp/universal-ptbr/validation-report.md
cp /tmp/universal-ptbr/validation-report.md ./validation-report.md
git add validation-report.md
# Se BLOCK, não commitar feat — voltar para Task3
```

- [ ] **Step 7: Commit final ou bloqueio**

```bash
# Se PASS:
git commit -m "chore: validation PASS for UniversalPTBR DMS+WD2

- xmllint 0 erros
- placeholders 1:1 com original
- git hygiene limpo
- pronto para tag v1.6-universal"
git tag v1.6-universal
git log --oneline -5
```

---

## Self-Review

**1. Spec coverage:**
- Rename Seção 1 → Task1 (About.xml, loadAfter, tag pre-universal) ✅
- Arquitetura pipeline → Tasks 2-5 em ordem com barrier ✅
- Agente 1 (Extrator) → Task2 (manifest, placeholders, packageId) ✅
- Agente 2 (Tradutor) → Task3 (glossário, DefInjected/Keyed drafts, delta) ✅
- Agente 3 (Integrador) → Task4 (DefInjected/Keyed/Patches, cSpell) ✅
- Agente 4 (Validador) → Task5 (xmllint, placeholder diff, rg, git) ✅
- Estrutura arquivos + convenções prefixo DMS_/WD2_ → Tasks 4-5 ✅
- Riscos (packageId, loadAfter, BOM, staleness, Workshop removido) → mitigados em Tasks 1,2,4 ✅

**2. Placeholder scan:** Nenhum TBD/TODO vago; todos os `TODO` são intencionais em contexto de tradução sem original. Comandos `xmllint`/`rg`/`python3` com código real, não genérico. ✅

**3. Type consistency:** `manifest-dms.json` produzido em Task2 consumido em Task3/4 com mesmos campos; `glossario.csv` → `glossario-delta.csv` → `.vscode/settings.json` encadeado; `validation-report.md` em `/tmp` e repo. ✅

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-25-universal-ptbr-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
