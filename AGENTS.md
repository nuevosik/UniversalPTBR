# AGENTS.md — Tradução Universal PT-BR

RimWorld translation mod. No build system or package manager; `tools/lint.py` is the repo check and runs in CI (`.github/workflows/lint.yml`).

## Structure

- `About/About.xml` — mod metadata: `packageId=GitHubVersion.TraducaoUniversal.PTBR`, `supportedVersions` 1.6/1.7, `loadAfter` list (~70 entries). Changing load order can break patches.
- `LoadFolders.xml` — `<v1.6>` and `<v1.7>` point to `/`: content loads from root.
- `Languages/PortugueseBrazilian/` — all translation content:
  - `LanguageInfo.xml` — `LanguageWorker_Portuguese`, `canBeTiny=true`.
  - `Keyed/*.xml` — `<LanguageData><Key>translated text</Key></LanguageData>` — UI, messages, dialogs.
  - `DefInjected/<DefType>/*.xml` — `<LanguageData><DefName.field>text</DefName.field></LanguageData>` — def injections (ThingDef, GeneDef, HediffDef, etc.). ~300 DefType subdirs, ~2.300 XML files.
  - `Strings/Words/Nouns/*.txt` — plain word lists for procedural generation (one term per line, UTF-8 with BOM).
- `Patches/*.xml` — `PatchOperation` XPath overrides (not `LanguageData`). Only for text DefInjected cannot reach (rule packs, PipeNet resources, gizmo texts) and for small compatibility fixes. A field already covered by `DefInjected` must not be patched too: DefInjected is applied after patches and wins.
- `tools/` — `lint.py` (repo-only checks), `coverage.py`/`campaign.py`/`extract_medieval.py`/`validate_medieval.py` (need the mods installed locally via Steam).

## Validation

```bash
python3 tools/lint.py            # XML validity, duplicate keys, empty/TODO values, <color>/{} balance
python3 tools/lint.py --selfcheck
git diff --check
```

A Keyed key must live in exactly one file; a duplicate makes the game keep one value and log an error.

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
- `.vscode/settings.json` holds `cSpell.words` (~368 entries) for spell-check — add new domain terms there (e.g., `gravinave`, `hemogênio`, `criptoforja`) rather than ignoring warnings.
- `.gitignore` covers `tools/__pycache__/`, `.superpowers/`, `work/`.

## Working Efficiently

- Prefer `rg` over `grep` for triage (`rg "pattern" Languages/PortugueseBrazilian`).
- Validate a single file: `xmllint --noout Languages/PortugueseBrazilian/Keyed/Keys.xml`.
- Bulk-validate: `find Languages Patches -name "*.xml" -exec xmllint --noout {} +`.
- Compare key/token integrity after edits: diff placeholders between HEAD and working tree, don't just eyeball text.
