# AGENTS.md — Tradução Universal PT-BR

RimWorld translation mod. No build system, package manager, tests, or CI. 100% XML/text translation files.

## Structure

- `About/About.xml` — mod metadata: `packageId=GitHubVersion.TraducaoUniversal.PTBR`, `supportedVersions` 1.4/1.5/1.6, `loadAfter` list (~70 entries). Changing load order can break patches.
- `LoadFolders.xml` — `<v1.4>`, `<v1.5>` and `<v1.6>` all point to `/`: content loads from root on all supported versions.
- `Languages/PortugueseBrazilian/` — all translation content:
  - `LanguageInfo.xml` — `LanguageWorker_Portuguese`, `canBeTiny=true`.
  - `Keyed/*.xml` — `<LanguageData><Key>translated text</Key></LanguageData>` — UI, messages, dialogs.
  - `DefInjected/<DefType>/*.xml` — `<LanguageData><DefName.field>text</DefName.field></LanguageData>` — def injections (ThingDef, GeneDef, HediffDef, etc.). 240 DefType subdirs, 1778 XML + 38 TXT no total.
    - Listas de gramática vão sob `<DefName>...rulesStrings>` com um `<li>` por regra (formato do pacote oficial PT-BR). O lado esquerdo da regra (`lhs->`) nunca é traduzido; o lado direito (o texto gerado) **sempre** é — `validate_medieval.py` só confere a presença das regras do EN, então RHS deixado em inglês passa silenciosamente.
    - Chave cujo `defName` não é nome de elemento XML válido (começa com dígito) vai via sintaxe antiga `<rep><path>…</path><trans>…</trans></rep>`.
  - `Strings/Words/{Nouns,BookWords,TeachingWords}/*.txt` e `Strings/Nickname/*.txt` — listas de palavras para geração procedural (uma linha por termo, UTF-8 com BOM; o RimWorld **anexa** às listas EN).
- `Patches/*.xml` — `PatchOperation` XPath overrides (not `LanguageData`). Contain Portuguese strings inline in `<value>` blocks. 12 files (e.g., `Patch_VRE_Starjack.xml`, `Patch_VGE_Chapter1.xml`).

## Validation (no test suite)

```bash
# XML validity — primary check before any commit
xmllint --noout Languages/PortugueseBrazilian/**/*.xml Patches/*.xml About/About.xml

# Diff hygiene
git diff --check
git diff --stat
git status --short   # check dirty state before staging

# Lotes da campanha total (chaves órfãs, valores vazios, placeholders, regras ausentes)
python3 tools/validate_medieval.py --batch B15        # DefInjected
python3 tools/validate_medieval.py --batch B15 --keyed

# Cobertura: lista alvos ainda sem tradução (por chave, sem a pasta de DefType)
python3 tools/coverage.py --json /tmp/targets.json --md /tmp/INVENTORY.md
```

`xmllint` (libxml 2.15.3) and `python3` are available. No `npm`/`dotnet`/`pytest`.

## Translation Constraints

Global constraints for every translation edit:

- Edit **only** translated text values. Never rename keys, `defName` references, files, or directories.
- Preserve verbatim: `{0}`/`{PAWN_name}`/`[TOKEN]` placeholders, XML tags, `\n` escapes, and `LanguageData` structure.
- Keep RimWorld canonical terms when PT-BR would lose reference (e.g., `pawn`, `hediff`, `xenotype`, `hemogen`, `gravship` — check divergence only when context justifies).
- PT-BR only: accentuation/regência/concordância, consistent gender/plural per `DefInjected` group.
- `README.md` is project docs, not in-game text — don't edit as translation.
- Classify before editing: `rg` triage produces false positives on names/technical terms/procedural words — no blind global replacements.

## Conventions & Gotchas

- Encoding: XML is `utf-8` with occasional BOM in TXT files — preserve it.
- `DefInjected` key format is `<DefName>.<field>` (`.label`, `.description`, `.labelFemale` etc.) — typo breaks injection silently in-game.
- `Keyed` keys are free-form but case-sensitive; fuzzy keys like `Generated_*.xml` are auto-generated IDs — still must match exactly.
- `Patches/` uses `PatchOperationFindMod` + `PatchOperationReplace` with `Defs/GeneDef[defName="..."]/label` XPath — wrong `defName` or `packageId` alias does nothing.
- `.vscode/settings.json` holds `cSpell.words` (507 entries) for spell-check — add new domain terms there (e.g., `gravinave`, `hemogênio`, `criptoforja`) rather than ignoring warnings.
- `.gitignore` cobre `tools/__pycache__/` e `.superpowers/` — o resto do repo é versionado; confira `git status` antes de adicionar.

## Working Efficiently

- Prefer `rg` over `grep` for triage (`rg "pattern" Languages/PortugueseBrazilian`).
- Validate a single file: `xmllint --noout Languages/PortugueseBrazilian/Keyed/Keys.xml`.
- Bulk-validate: `find Languages Patches -name "*.xml" -exec xmllint --noout {} +`.
- Compare key/token integrity after edits: diff placeholders between HEAD and working tree, don't just eyeball text.
