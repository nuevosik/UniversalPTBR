# Design: Tradução Universal (PT-BR) — Pipeline de 4 Agentes para DMS + World Domination 2.0

**Data:** 2026-08-25
**Status:** Aprovado (4 seções validadas com o usuário)
**Escopo:** Renomear `VanillaExpandedPTBR` → `UniversalPTBR` e incluir traduções PT-BR para `The Dead Man's Switch` (3121742525, AOBA) e `World Domination 2.0` (3680501610, LikewiseHH)
**Repo:** `VanillaExpandedPTBR` (será renomeado para `UniversalPTBR`)
**Versão alvo RimWorld:** 1.6 (`LoadFolders.xml:3` `<v1.6><li>/</li></v1.6>`)

---

## 1. Contexto e Decisão Arquitetural

### 1.1 Estado atual
- `About/About.xml:1`: `<name>Tradução Vanilla Expanded (PT-BR)</name>`, `<packageId>GitHubVersion.TraducaoVanillaExpanded.PTBR</packageId>`, `supportedVersions` 1.4/1.5/1.6, `loadAfter` ~60 entradas VE-only.
- `Languages/PortugueseBrazilian/`: `DefInjected/` (~919 XMLs), `Keyed/` (~100 XMLs), `Strings/Words/Nouns/*.txt` (BOM), `Patches/*.xml` (11 arquivos `PatchOperationFindMod`).
- Constraints `AGENTS.md` + `docs/superpowers/plans/2026-08-23-revisao-traducoes-ptbr.md`: só editar valores traduzidos, preservar `{0}`/`{PAWN_name}`/`[TOKEN]`/tags XML/`\n`/`LanguageData`, PT-BR com `gravinave`/`hemogênio` consistentes, `xmllint --noout` antes de commit.

### 1.2 Alvos
- **DMS (3121742525)**: 33.399 MB, cyberpunk 1990s, mechs/mecanoides, exosuits, árvore tech standalone, Ideology style, Royalty titles, requer `Biotech` + `Fortified Features Framework` (3498575851), ~250 Defs estimados, 1 `Keyed` grande. Workshop fetch confirma "removed due to violation" mas assinável; 3,494 ratings, 221k subs.
- **WD2 (3680501610)**: 21.391 MB, sucessor do RimWar + Vanilla Outposts Expanded, sistema de outposts/caravanas/mapa-múndi, requer `Harmony` + `VE Framework`, 1.6-only, altamente configurável, XML exposto recentemente. 256 ratings, 7.5k subs.

### 1.3 Decisão: Opção A + Rename
- **Opção A** escolhida: incluir DMS e WD2 no mesmo repo (mesmo `packageId` novo), novos arquivos `Languages/PortugueseBrazilian/Keyed/DMS_*.xml`, `DefInjected/.../DMS_*.xml`, `Patches/Patch_DMS_*.xml`.
- **Rename:** `VanillaExpandedPTBR` → `UniversalPTBR`
  - Novo `<name>Tradução Universal (PT-BR)</name>`
  - Novo `<packageId>GitHubVersion.TraducaoUniversal.PTBR</packageId>`
  - `loadAfter` += `<li>Aoba.DeadMansSwitch</li>` e `<li>LikewiseHH.WorldDomination2</li>` (packageIds confirmados pelo Agente 1, não assumidos)
- Alternativas descartadas: B (repo separado) fragmenta distribuição; C (monorepo híbrido) complica `LoadFolders`.

### 1.4 Abordagem escolhida para os 4 agentes
- **Abordagem 1 — Pipeline Sequencial Especializado** (recomendada): `Extrator → Tradutor → Integrador → Validador`, artefatos em `/tmp/universal-ptbr/`, barrier entre estágios, paralelismo interno DMS || WD2.
- Descartadas: Abordagem 2 (squads por mod, glossário diverge) e 3 (orquestrador, over-engineering).

---

## 2. Arquitetura

```
[Workshop ZIPs: DMS 3121742525 + WD2 3680501610]
        ↓
Agente 1 — EXTRATOR ──→ manifest.json {packageId, supportedVersions, DefTypes[], KeyedKeys[], placeholder inventory}
        ↓
Agente 2 — TRADUTOR ──→ draft XMLs + glossario.csv + cSpell delta  (só /tmp)
        ↓
Agente 3 — INTEGRADOR ──→ Languages/.../{DefInjected,Keyed,Patches}/ + About.xml renomeado (único escritor no repo)
        ↓
Agente 4 — VALIDADOR ──→ xmllint + placeholder diff + git hygiene → validation-report.md (gate)
```

- **Orquestração via `task` subagents:** `task --subagent_type general` sequencial com dependências; Agents 1 e 2 paralelizáveis internamente.
- **Regras globais herdadas (todos):** só valores, nunca `defName`/keys/dirs; preservar placeholders/tags; PT-BR consistente; `cSpell.words` em `.vscode/settings.json`; `xmllint` antes de commit.

---

## 3. Os 4 Agentes em Detalhe

### Agente 1 — EXTRATOR / Minerador (Recon)
- **Objetivo:** Inventariar sem traduzir.
- **Inputs:** Workshop IDs via `steamcmd +workshop_download_item 294100 <id>` ou zip manual; `About/About.xml` e `Patches/*.xml` como referência.
- **Outputs:** `/tmp/universal-ptbr/manifest-{dms,wd2}.json` + `About.xml` original de cada mod.
- **Ferramentas:** `bash` (`unzip`, `rg`, `xmllint --noout`, `python3 -c`), `read`/`glob`.
- **Guardrails:** Não editar `Languages/`; extrair `packageId` real via `grep "<packageId>"`; catalogar placeholders com `rg -o "\{[0-9]+\}|\{PAWN[^}]+\}|\[TOKEN\]"`; estimativa DMS ~250 Defs, WD2 ~80 Defs.
- **Prompt:** "Você é o Extrator. Dado o zip de <mod>, liste todos os Defs com defName+label/description, todo Languages/English/Keyed, gere manifest.json. Valide xmllint no original. Não traduza."

### Agente 2 — TRADUTOR (Linguístico)
- **Objetivo:** Gerar drafts PT-BR consistentes em `/tmp`.
- **Inputs:** `manifest-*.json` + `glossario.csv` (semeado de `Gravship_Keys.xml:176` `gravinave`, `hemogênio`, etc.) + `.vscode/settings.json` `cSpell.words`.
- **Outputs:** `/tmp/universal-ptbr/draft/{DMS,WD2}/DefInjected/**/*.xml`, `Keyed/DMS_*.xml`, `WD2_*.xml`, `glossario-delta.csv`.
- **Ferramentas:** `read`, `write` em `/tmp`, `bash` `rg`.
- **Guardrails:** Só valores, chaves intocadas; preservar `{0}`/`{PAWN_name}`/`\n`; PT-BR acentuação/gênero/plural consistente por `DefInjected` grupo; não traduzir termos canônicos sem necessidade; não traduzir nomes próprios/procedural `Strings/Words`; marcar `TODO` sem contexto.

### Agente 3 — INTEGRADOR / Empacotador (Engenharia)
- **Objetivo:** Materializar no repo e executar rename. Único escritor.
- **Inputs:** Drafts + `About/About.xml` + `LoadFolders.xml` + padrão `Patches/Patch_VRE_Starjack.xml:3`.
- **Outputs:**
  - `Languages/PortugueseBrazilian/DefInjected/<DefType>/DMS_*.xml` e `WD2_*.xml`
  - `Languages/PortugueseBrazilian/Keyed/DMS_Keys.xml`, `WD2_Keys.xml`
  - `Patches/Patch_DMS_*.xml`, `Patch_WD2_*.xml` (se necessário `PatchOperationFindMod`)
  - `About/About.xml` renomeado (name, packageId, description, loadAfter)
  - `.vscode/settings.json` atualizado
- **Ferramentas:** `edit`/`write` após `read`, `bash` lint.
- **Guardrails:** Tag `pre-universal` antes do rename; `DefInjected` key `<DefName>.<field>` exato; `PatchOperationReplace` XPath `Defs/GeneDef[defName="..."]/label` exato; XML `utf-8` sem BOM.

### Agente 4 — VALIDADOR / QA (Porteiro)
- **Objetivo:** Gate da Tarefa 4 do plano.
- **Inputs:** Repo pós-integração + baseline Agente 1.
- **Outputs:** `validation-report.md` + `git diff --stat` + `git diff --check`.
- **Checks:**
  1. `find Languages Patches -name "*.xml" -exec xmllint --noout {} +` → 0 erros
  2. Diff placeholders `python3 -c` entre HEAD e working tree
  3. `rg` triagem re-executada
  4. `git diff --check` + `git status --short`
  5. Smoke in-game 1.6 (opcional)
- **Guardrails:** Nunca auto-corrigir; bloquear merge se falhar.

---

## 4. Estrutura de Arquivos e Rename

### 4.1 Árvore alvo
```
UniversalPTBR/
├── About/About.xml  ← RENOMEADO
├── LoadFolders.xml  ← intacto
├── Languages/PortugueseBrazilian/
│   ├── LanguageInfo.xml
│   ├── DefInjected/ThingDef/DMS_Weapons.xml
│   ├── DefInjected/GeneDef/DMS_Genes.xml
│   ├── DefInjected/WorldObjectDef/WD2_Outposts.xml
│   ├── Keyed/DMS_Keys.xml
│   ├── Keyed/WD2_Keys.xml
│   └── Strings/Words/Nouns/ (sem mudança)
├── Patches/Patch_DMS_*.xml
├── Patches/Patch_WD2_*.xml
└── .vscode/settings.json
```

### 4.2 Diff About.xml
```diff
- <name>Tradução Vanilla Expanded (PT-BR)</name>
+ <name>Tradução Universal (PT-BR)</name>
- <packageId>GitHubVersion.TraducaoVanillaExpanded.PTBR</packageId>
+ <packageId>GitHubVersion.TraducaoUniversal.PTBR</packageId>
- <description>Tradução para Português Brasileiro da série Vanilla Expanded...</description>
+ <description>Tradução para Português Brasileiro — Vanilla Expanded + mods universais curados (The Dead Man's Switch, World Domination 2.0 e mais)...</description>
  <loadAfter>
+   <li>Aoba.DeadMansSwitch</li>
+   <li>LikewiseHH.WorldDomination2</li>
  </loadAfter>
```

### 4.3 Convenções
- Prefixo explícito `DMS_`/`WD2_` (não `Generated_*` que é de VE).
- Um arquivo por `DefType` para `git diff --stat` claro.
- Exemplo `DefInjected`: `<DMS_Mech_Tarbosaurus.label>tarbossauro mecanizado</DMS_Mech_Tarbosaurus.label>`
- Exemplo `Patches`: `PatchOperationFindMod` com `<mods><li>Aoba.DeadMansSwitch</li></mods>` + `PatchOperationReplace` XPath exato (padrão `Patch_VRE_Starjack.xml:10`).

---

## 5. Validação, Riscos e Entrega

### 5.1 Validação (Agente 4)
Ver tabela Seção 4; todos os 5 passos devem passar. Agente 4 retorna para 2/3 se falhar.

### 5.2 Riscos
1. **packageId breaking** → tag `pre-universal`, novo Workshop item, redirect no antigo.
2. **loadAfter ordem** → Agente 1 replica ordem original de cada mod.
3. **Placeholders** → diff automatizado.
4. **BOM** → XML sem BOM.
5. **Staleness (DMS 100, WD2 116 changenotes)** → manifest com `Updated`, pipeline re-runnable.
6. **Workshop removido** → fallback `steamcmd` + zip manual.

### 5.3 Critério de sucesso
- Carrega em 1.6 com VE+DMS+WD2 sem vermelho; Keyed 100% + DefInjected cobre manifest; xmllint 0; placeholders preservados; cSpell limpo.

### 5.4 Entrega
- Branch `feat/universal-ptbr` → 3 commits: `chore: rename`, `feat: DMS`, `feat: WD2`
- Spec: este arquivo

---

## 6. Próximos Passos (writing-plans)
- Invocar `superpowers:writing-plans` para gerar plano de implementação com tasks por agente, dependências, comandos `xmllint`/`rg`/`python3` exatos, e prompts `task` copiáveis.

## 7. Referências
- `About/About.xml`, `LoadFolders.xml`, `Patches/Patch_VRE_Starjack.xml`, `Languages/PortugueseBrazilian/Keyed/Gravship_Keys.xml`, `AGENTS.md`, `docs/superpowers/plans/2026-08-23-revisao-traducoes-ptbr.md`
- Workshop: 3121742525 (DMS), 3680501610 (WD2)
