# Campanha de tradução — mods medievais (PT-BR)

**Data:** 2026-09-14
**Status:** design aprovado, aguardando revisão da spec
**Repo:** UniversalPTBR (`GitHubVersion.TraducaoUniversal.PTBR`)

## Objetivo

Traduzir para PT-BR os 40 alvos medievais inventariados: 34 sem cobertura, 3 parciais (MO Tweaks, Adaptive Storage, Medieval Medicines MO Ed) e 3 com texto mínimo (Misc Training Retexture, Chemfuel Retextured, ReGrowth Patch). Lista completa em `docs/medieval/INVENTORY.md`. Fase 1 cobre apenas campos escalares via DefInjected; fase 2 cobre Keyed (UI/mensagens de C#) apenas nos 10 mods que já embarcam `Languages/English`.

## Não-objetivos (fase 1)

- Listas aninhadas (`rulePacks`, `rulesStrings` e demais `<li>`) — ficam para uma fase futura; os ~102k `<li>` são majoritariamente estruturais.
- Extração de strings de dentro de `.dll` (sem English no mod) — fase 2 só onde há English pronto.
- Renomear mods, packageIds ou defNames; traduzir apenas texto exibido.

## Decisões

| Tema | Decisão |
|---|---|
| Escopo | XML (DefInjected) primeiro; Keyed depois |
| Tradução | Agentes de IA traduzem; humano revisa o diff antes do commit |
| Terminologia | Glossário novo, aprovado pelo humano, + cSpell |
| Estrutura | Mesma árvore do repo (`DefInjected/<DefType>/`, `Keyed/`), arquivo por tipo de def por mod |
| Docs | `docs/medieval/` (o repo não mantém mais `docs/superpowers/`) |
| Commits | Um por lote, conventional commits PT, após revisão humana |

## Arquitetura

```
tools/extract_medieval.py     # gera esqueletos DefInjected a partir dos mods instalados
tools/validate_medieval.py    # validação automática (chaves, placeholders, encoding)
docs/medieval/INVENTORY.md    # folder id, packageId, contagens, status por mod
docs/medieval/GLOSSARY.md     # termos canônicos aprovados
Languages/PortugueseBrazilian/DefInjected/<DefType>/<Mod>_<Tipo>.xml
```

Fluxo: **extrair → esqueleto com inglês → glossário → traduzir por lote → validar → revisar → commitar**.

### Extrator

- Varre `~/.local/share/Steam/steamapps/workshop/content/294100/<id>/` dos alvos.
- Ignora defs `Abstract="True"` e campos não presentes no XML do def.
- Campos escalares: `label`, `description`, `labelFemale`, `labelPlural`, `labelNoun`, `jobString`, `verb`, `gerund`, `letterText`, `reportString`, `text`, `title`, `summary`, `tip`.
- Pula chaves já existentes em `Languages/PortugueseBrazilian/` (overlap com VE/MO cobertos).
- Escreve os esqueletos com o inglês como valor; a tradução acontece in-place preservando chaves, placeholders (`{0}`, `{PAWN_*}`, `[TOKEN]`, `\n`) e encoding.
- Gera `docs/medieval/INVENTORY.md` com contagem por campo, status (sem/parcial/coberto) e flag de ativo no `ModsConfig`.

### Validador

- `xmllint` em todos os XMLs tocados.
- Para cada chave: confirma que `defName` + campo existem no mod instalado (detecta chave órfã).
- Compara placeholders do inglês vs PT; divergência = falha.
- `git diff --check` e status limpo antes do commit.

## Lotes

| Lote | Conteúdo | Mods | Strings (label+desc) |
|---|---|---|---|
| L0 | script + inventário + glossário | — | 0 |
| L1 | quick wins ≤100 strings | 14 | ~265 |
| L2 | ecossistema Medieval Overhaul | 7 | ~2.873 |
| L3 | standalone médios | 13 | ~1.716 |
| L4 | grandes | 4 | ~4.523 |
| F2 | Keyed (mods com English) | 10 | a medir |

L1: Walls, Signs, Transport, Geysers, Hornetkeeping, HRK deathrest coffin, Medicines, Extra Signs, Space Knights, Coastal Outfits, DBH Retexture, ReGrowth Patch, Overlap Remover, Anomaly.
L2: MO Royalty, MO Barbarians, House Van Illa, House Roxmont, House Ignivar, MO Tweaks, Adaptive Storage.
L3: Gene Assembler, Backstories Patch, Dark Ages Tools, Adventures Implants/Hunts, Tasty Armory, Tailor, Fortifications Medieval (+Material), Quest Rewards, Relic Quests, Rare Resources, Trader Airships.
L4: RimTraits Medieval Talents, RimFantasy MO Edition, Medieval Prosthetics, Medieval Medicines MO Ed (completar lacunas).

Total fase 1: **9.377 strings** (~9,4k).

## Execução por lote

1. Agentes paralelos traduzem mod a mod (glossário + AGENTS.md), sem tocar arquivos fora do lote.
2. Validador roda por lote; falha bloqueia o lote.
3. Diff resumido apresentado ao humano; revisão → commit (`feat(lang): traduz <lote> (PT-BR)`) → push.

## Riscos

- **Volume/revisão**: 9,4k strings é grande; lotes pequenos mantêm a revisão viável.
- **Mods atualizam na Workshop**: defs mudam → validador acusa chaves órfãs; re-rodar extração.
- **Nomes próprios/marcas**: manter como no original quando PT-BR perder referência (guardrail do AGENTS.md).
- **Overlap com traduções instaladas** (ex.: MO PTBR): extração pula chaves já cobertas; lacunas vão pro lote correspondente.

## Critérios de sucesso

- 100% dos campos escalares dos 40 alvos com tradução PT-BR revisada.
- `xmllint` 0 erros, validador 0 falhas, 0 chave órfã.
- Um commit revisado por lote; glossário seguido em todos.
- Fase 2: Keyed dos 10 mods com English.
