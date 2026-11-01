# Brief de tradução — chunks JSON (EN→PT-BR)

Instruções aplicadas por subagente em cada chunk da campanha de 31/10/2026. Um chunk é um JSON com `defs` (por DefType) e `keyed`, no formato:

```json
{"defs": {"<DefType>": {"<chave>": "<texto EN>"}}, "keyed": {"<chave>": "<texto EN>"}}
```

## Contrato de saída

- Mesmo JSON, mesma estrutura e mesmas chaves, com valores em português do Brasil.
- Toda chave do chunk presente, com valor não vazio.
- Nunca alterar, renomear, reordenar ou remover chaves.
- UTF-8, JSON válido.

## Regras invioláveis

- Preservar verbatim: `{0}`, `{1}`, `{PAWN_name}`, `{PAWN_possessive}`, `[TOKEN]`, `\n` (barra invertida + n), tags `<color=...>`/`</color>`, entidades XML.
- Não traduzir `defName`, nomes de classe, ids nem conteúdo entre chaves de código.
- Nomes próprios de facções, casas, pessoas e criaturas ficam no original (Aoba, Ignivar, Dead Man's Switch, Alpha Animals, Vanilla Expanded).
- Termos canônicos do RimWorld: pawn=colono, colony=colônia, settlement=assentamento, raid=incursão, quest=missão, research=pesquisa, hediff=ferimento/condição de saúde, mechanoid=mecanoide, mech=mecha, turret=torreta, plasteel=plastiaço, chemfuel=combustível químico, neutroamine=neutroamina, hyperweave=hiper tecido, synthread=fibra sintética, stuff=material, stack=pilha, storage=armazenamento, bill=tarefa, stat=estatística, tier=nível, upgrade=melhoria, caravan=caravana, outpost=posto avançado, goodwill=boa vontade, faction=facção, empire=império, vassal=vassalo.
- Vanilla Expanded/Aoba: gene=gene, xenotype=xenótipo, hemogen=hemogênio, gravship=gravinave, psycast=psicocast, psycaster=psinjurador, archotech=arquiotecnológico, android=androide, exosuit=exotraje.
- Descrições: prosa natural e direta, conteúdo inteiro, sem resumo.
- Labels e títulos: curtos, capitalização de título em PT.
- Concordância de gênero/número e acentuação corretas.
- Nada fora do JSON.

## Glossário completo

`docs/traducao-total/GLOSSARY.md` e `docs/medieval/GLOSSARY.md`.
