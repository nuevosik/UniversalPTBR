# Campanha completa — Tradução de todos os mods instalados (PT-BR)

**Data:** 31/10/2026
**Alvo:** todos os mods instalados no RimWorld (Workshop 294100), ativos e desativados.
**Resultado:** zero pendências de tradução; validação de tokens e XML sem falhas.

## Números

| Métrica | Valor |
|---|---|
| Mods ativos no `ModsConfig.xml` | 215 |
| Mods instalados com texto e pendências (ativos) | 116 |
| Strings traduzidas na campanha ativa | 18.056 |
| Strings residuais (reextração pós-limpeza) | 208 |
| Strings dos mods instalados e desativados | 1.587 |
| Entries no repositório ao final | 69.766 (48.772 DefInjected + 20.994 Keyed) |
| Arquivos XML de idioma ao final | 2.292 |
| Pendências no inventário final | 0 |

## Ferramentas

| Arquivo | Papel |
|---|---|
| `tools/coverage.py` | Inventaria os mods instalados, calcula pendências por `(DefType, chave)` e por chave Keyed, gera `tools/targets.json` e `docs/traducao-total/INVENTORY.md`. Passou a ignorar chaves que não podem ser elementos XML (nomes iniciados por dígito) e entradas cujo inglês é vazio. |
| `tools/extract_medieval.py` | Extrai os valores ingleses dos Defs e de `Languages/English/Keyed`; corrigido para ler o texto das chaves Keyed (antes gravava valor vazio). Caminhos de Steam resolvidos para Windows e Linux. |
| `tools/campaign.py` | Pipeline da campanha: `extract` (gera chunks EN por mod), `assemble` (grava os XMLs em `Languages/PortugueseBrazilian` preservando entradas existentes) e `check` (confere chave/placeholder/tag/newline e lista pendências). |
| `tools/validate_medieval.py` | Validador herdado, usado por lote para DefInjected e Keyed. |

## Fluxo executado

1. Auditoria do `ModsConfig.xml`: 215 mods ativos de 261 pastas instaladas na Workshop.
2. Extração dos valores ingleses pendentes em chunks JSON (≤ 200 chaves e ≤ 9 KB por arquivo).
3. Tradução por subagentes em paralelo, um chunk por tarefa, seguindo `work/campaign/BRIEF.md` (glossários `docs/medieval/GLOSSARY.md` e `docs/traducao-total/GLOSSARY.md`).
4. Conferência automática de: chave presente, valor não vazio, multiconjunto de `{...}` igual ao inglês, mesma quantidade de `\n` literais e de tags `<color>`.
5. Reparo em duas rodadas (grosseira e fina) e correção manual das 5 strings que ainda divergiam.
6. Montagem no repositório, limpeza de 251 chaves órfãs legadas (defs renomeadas nas atualizações 1.7) e validação por lote.
7. Reextração para cobrir o que foi removido na limpeza e tradução dos mods instalados-desativados.

## Validação final

- `python tools/validate_medieval.py --batch B1..B14` (DefInjected): **OK** em todos os lotes — 15.465 chaves.
- `python tools/validate_medieval.py --batch B1..B14 --keyed`: **OK** em todos os lotes — 11.849 chaves.
- Checagem global contra o índice inglês de todos os mods instalados: **0 divergências** de placeholder/tag/newline em 51.818 entradas com fonte inglesa.
- Well-formedness: **0 XML inválido** em 2.292 arquivos (parser `xml.etree`; `xmllint` não existe nesta máquina Windows).
- `python tools/coverage.py`: **0 alvos, 0 chaves pendentes**.

## Observações

- Mods com `Languages/PortugueseBrazilian` próprio (Combat Extended principal, Medieval Overhaul, Dubs Bad Hygiene Lite, HugsLib e outros) permanecem fora da campanha: já têm tradução embarcada.
- Chaves cujo nome começa com dígito não podem ser elementos XML válidos e ficam fora do inventário (o próprio RimWorld não as carrega).
- Entradas vazias herdadas de campanhas antigas, sem def correspondente nos mods instalados, foram mantidas; não são carregadas pelo jogo.
- Os arquivos estão no working tree para o gate humano do repositório; nenhum commit foi feito nesta sessão.
- A pasta `RimWorld/Mods/UniversalPTBR` é um clone git separado e foi sincronizada por cópia: ficou com ~800 arquivos modificados. Depois de commitar/pushar neste repositório, rode `git checkout -- .` (ou `git reset --hard origin/main`) naquela cópia antes de qualquer `git pull`, senão o pull conflita.
