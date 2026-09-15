# Glossário — Campanha Medieval (PT-BR)

Mapa EN→PT canônico para os lotes L1–L4 (40 alvos, 9.353 strings). Regras:

- Um termo PT por conceito; não criar sinônimo concorrente dentro do mesmo lote.
- Só o valor é traduzido; nunca renomear chaves, `defName`, arquivos ou pastas.
- Preservar `{0}`, `{PAWN_*}`, `[TOKEN]`, `\n` e a estrutura `LanguageData` (constraint global do repo).
- Fonte do termo: **repo** = já existe em `Languages/PortugueseBrazilian` (herdar);
  **oficial** = RimWorld PT-BR oficial (`Data/Core`, `Data/Royalty`); **externo** = tradução PT-BR
  existente do Medieval Overhaul (Workshop 3033778829 / arquivos PT embutidos no MO 3219596926);
  **novo** = proposto nesta campanha, sem precedente.
- Divergências com termo já existente estão registradas em Obs. Nenhum termo herdado foi trocado.

## Termos de jogo

| EN | PT-BR | Obs |
|---|---|---|
| pawn | colono | oficial. Placeholders `[PAWN_nameDef]`, `[PAWN_possessive]` etc. permanecem intactos — nunca traduzir o token. |
| room beauty | beleza do ambiente | repo (VFEM2_ThingDef, Generated_1718190143). Oficial Core usa "quarto" em RoomStat — divergência aceita; manter "ambiente". |
| work speed / market value | velocidade de trabalho / valor de mercado | oficial (`WorkSpeedGlobal`, `MarketValue`). |
| stack / storage / stockpile / blueprint | pilha / armazenamento / estoque / projeto | oficial. "items stored" → "itens armazenados"; "5 stacks" → "5 pilhas"; blueprint sai como "(projeto)". |
| quest / reward / relic / letter | missão / recompensa / relíquia / carta | repo. "bloody letter" → "carta ensanguentada"; "undelivered letter" → "carta não entregue". |
| energy | energia | repo/oficial. "magical energy" → "energia mágica"; "energy burn" → "queimadura de energia"; "vampiric energy" → "energia vampírica"; "restorative energy" → "energia restauradora". |
| magic | magia | oficial/repo. Escolas: nature → magia da natureza; fire → do fogo; shadow → das sombras; healing → de cura; time → do tempo; lightning → de relâmpagos; battle → de batalha. |
| enchanted / lower / higher | encantado / inferior / superior | repo (11). "Enchanted with lower fire magic" → "Encantado com magia do fogo inferior". Reservar "menor/maior" para "lesser/greater". |
| unleash / release / wave / blast / bubble | desencadear / liberar / onda / explosão / bolha | RimFantasy. "unleash a wave" → "desencadear uma onda"; "on enemy contact" → "no contato com o inimigo". |
| arcane / rune | arcano / runa | repo (VRE_Archon "ciência arcana"; VFE_Pirates "segredos arcanos"). "rune-etched" → "gravado com runas". |
| mana / potion / elixir | mana / poção / elixir | repo (mana 86; poção 44). "mana potion" → "poção de mana"; "healing potion" → "poção de cura"; "elixir" permanece "elixir". |
| soul stone | pedra da alma | novo (Gene Assembler). Sem precedente no repo; minúsculas. |
| Daer / Lindwurm / Schrat / Unhold / Webknecht | manter original | Nomes próprios de criaturas. Não traduzir; manter a capitalização da fonte. |
| griffon | grifo | novo; externo mantém "griffon" (divergência registrada). "Griffon Nest" → "Ninho de Grifo"; "griffon berries" → "bagas de grifo". |
| deathstinger | vespa assassina | externo (MO PTBR, PawnKindDef). Repo não tem; criatura do MO referenciada pelo Hornetkeeping. |

## Materiais/armas

| EN | PT-BR | Obs |
|---|---|---|
| armor (armour) / plate armor | armadura / armadura de placas | repo VFEM2 ("armadura de placas pesada"). Grafia britânica "armour" idem. |
| chainmail / maille / hauberk / coif | cota de malha / coifa | repo (VARME `VAE_Apparel_Chainmail` = "cota de malha"); coifa externo ("coifa de cota"). Não usar "lórica". "heraldic hauberk" → "cota de malha heráldica"; "maille coif" → "coifa de malha". |
| helm (great helm / kettle helm/hat / barbute / nasal helm) | elmo (grande elmo / chapéu-de-ferro / barbuda / elmo nasal) | repo elmo (VFEM2). "chapéu-de-ferro" e "barbuda" são novos; externo usa "capelina" para kettle — divergência registrada, adotar "chapéu-de-ferro". |
| shield (round / tall / heater / kite / buckler) | escudo (redondo / alto / triangular / romboidal / broquel) | repo escudo (113). Externo traduziu "heater shield" como "escudo aquecedor" (erro) — adotar "escudo triangular". |
| cuirass / gambeson / jerkin / brigandine | couraça / gambesão / gibão / brigantina | repo (VFEE "couraça de janízaro"; VARME "gambesão"); gibão e brigantina externos. "chestplate" → "peitoral de placas" (VARME). |
| surcoat / tabard | sobreveste / tabardo | tabardo repo VFEM2; externo usa "sobrecota/gambeson acolchoado" para surcoat — padronizar "sobreveste". |
| gauntlets / pauldrons / greaves | manoplas / ombreiras / grevas | manoplas repo VARME/oficial; ombreiras repo (42); grevas novo (sem precedente). |
| sword (longsword / shortsword / greatsword / zweihander / claymore / arming sword) | espada (espada longa / espada curta / montante / montante / claymore / espada de armas) | longa/curta oficial; claymore repo VFEM2 (mantido); greatsword e zweihander → "montante" (novo no repo); "Rusted Claymore" → "Claymore enferrujada". |
| dagger / mace / flail / warhammer | adaga / maça / mangual / martelo de guerra | adaga e maça oficiais; mangual repo VFEM2; martelo de guerra oficial (6). "parrying dagger" → "adaga de aparar". |
| axe (battle axe / greataxe / handaxe / bill) | machado (machado de batalha / machado grande / machadinha / foice de guerra) | oficial machado. "bill/billhook" → "foice de guerra" (novo). |
| spear / pike / halberd / glaive / bardiche | lança / pique / alabarda / glaive / bardiche | lança oficial; pique e alabarda repo VFEM2; glaive e bardiche mantidos (estrangeirismos consagrados). |
| bow / crossbow / bolt / arrow | arco / besta / virote / flecha | oficial. "crossbow bolt" → "virote de besta"; "light crossbow bolt" → "virote leve". |
| leather / hide / cloth / wool / bone / skull | couro / pele / tecido / lã / osso / crânio | oficial. "tanned leathers" → "couros curtidos"; "hide" = pele de animal; "Bone Armor/Helm" → "armadura/elmo de ossos"; "skulls looted" → "crânios saqueados". |
| obsidian / glimmerquartz / magicyte | obsidiana / quartzo-cintilante / magicita | obsidiana repo (9); os outros dois novos (MO Tweaks e Things: Geysers). "magicyte" é recurso, não "cristal mágico". |
| rime / rimedew / rimecrystal / aether / ashberry | geada / orvalho-de-geada / cristal-de-geada / éter / baga-de-cinza | éter repo VQE ("tubos de pressão de éter"); demais novos (House Van Illa/MO). "rimed" (adj.) → "geado"; "rimecloth" → "tecido-de-geada"; plural "bagas-de-cinza". |
| sapphire / ruby / emerald / citrine / onyx / jade / diamond / amber | safira / rubi / esmeralda / citrino / ônix / jade / diamante / âmbar | externo (MO PTBR já usa todos); gema = "gema"; "shards" → "lascas" ("lascas de rubi"). Minúsculas. |
| ore / iron / steel / gold / silver / coal | minério / ferro / aço / ouro / prata / carvão | oficial. "barrel of gold ore" → "barril de minério de ouro". |
| marble / granite / sandstone / limestone / slate / brick / timber / log / pebble / chunk | mármore / granito / arenito / calcário / ardósia / tijolo / madeira / tora / pedrisco / pedaço | oficial (blocos, "pedaço" = chunk `ChunkGranite`); "pebble" → "pedrisco" (novo; oficial não tem). |
| mead / honey / wine / beer / ale / stout / wort | hidromel / mel / vinho / cerveja / cerveja / stout / mosto | repo VFEM2 + externo. "hornet mead" → "hidromel de vespa"; "stout" mantido como estrangeirismo ("stout de roxberry"); "wort" → "mosto". |
| cheese / roast / stew / rox | queijo / assado / ensopado / rox | repo (VCE "assados"; ensopado 4). "rox" invariável ("queijo de rox", "bife rox", "leite de rox"). |

## Facções/títulos

| EN | PT-BR | Obs |
|---|---|---|
| house / estate / manor | Casa / propriedade / mansão | repo (propriedade 35; mansão 11). "Casa Ignivar", "Casa Van Illa", "Casa Roxmont"; "Alp Estate" → "Propriedade Alp". |
| castle / fortress / outpost | castelo / fortaleza / posto avançado | repo (VFEM2 castelo 43 + "muralha de castelo"; "posto avançado" já em cSpell). |
| knight / squire | cavaleiro / escudeiro | repo VFEM2 (cavaleiro 36; escudeiro 9). |
| noble / nobility | nobre / nobreza | repo (82/30). "Spurned Illan Noble" → "Nobre Illan Desprezado". |
| lord / lady / king / queen / majesty | senhor / senhora / rei / rainha / majestade | repo/oficial. "lady" como título → "senhora" (alt. "dama" só em vestuário/peça). |
| baron(ess) / count(ess) / duke / duchess | barão(esa) / conde(ssa) / duque / duquesa | repo (VFE Empire). Divergência: oficial Royalty traduz Count→"Arconte" e Duke→"Dominus"; adotar títulos históricos do repo para a campanha medieval. |
| warlord / barbarian | senhor da guerra / bárbaro | warlord repo (4; VVE Core). "bárbaro" novo (sem precedente no repo). "Barbarian tribe" → "tribo bárbara". |
| infantry / footman / levy / archer / mercenary / raider / bandit / cavalry | infantaria / infante / recruta / arqueiro / mercenário / saqueador / bandido / cavalaria | repo/oficial: infantaria 255, infante (VFEM2), arqueiro, mercenário, saqueador 20. "levies" → "recrutas". |
| fey (Illan Fey / Frost Fey) | fada (Fada Illan / Fada do Gelo) | novo; repo não tem "fada" (ocorrências eram falsos positivos). "Illan" é adjetivo invariável do xenótipo. |
| simulacrum / simulacra / Awakened Simulacrum | simulacro / simulacros / Simulacro Desperto | novo (House Van Illa). Sem precedente em repo/oficial/externo. |
| flamesmith / steward / apothecary / alchemy | forjador de chamas / mordomo / boticário / alquimia | mordomo oficial Royalty ("mordomo chefe"); alquimia repo (2); "flamesmith" (House Ignivar) e "boticário" novos. "flamesmiths" → "forjadores de chamas". |
| heraldry / banner / heraldic | heráldica / estandarte / heráldico | repo (VFEM2 "heráldica", "estandarte heráldico"; banner 17). "heraldic standard" → "estandarte heráldico". |
| tavern / market / guild | taverna / mercado / guilda | repo (guilda 17; "mestre da guilda" em cSpell). "market stall" → "barraca de mercado". |

## Verbos de receita/Job

| EN | PT-BR | Obs |
|---|---|---|
| make / craft / forge (smith) | fazer / fabricar / forjar | oficial (Crafting.verb "Fabricar em"). Receitas estilo MO: "Make a Warlord helm" → "Fazer um elmo de senhor da guerra". WorkGiver "craft at" → "fabricando em"; "smithing at" → "forjando em". |
| mine / drill | minerar / perfurar | oficial (Mining.verb "Minerar"; jobString "cavando em"; OperateDeepDrill "perfurando"). Receitas "Mining 1 obsidian." → "Minerar 1 obsidiana". |
| polish / cut / crush | polir / cortar / triturar | oficial (CutPlant "cortando"; SmoothFloor "alisando"). "crush rock chunks" → "triturar pedaços de rocha". |
| gather / harvest / sow / plant | coletar / colher / semear / plantar | oficial (Harvest "colhendo"; PlantSeed "plantando"). "gather pebble" → "coletar pedrisco". |
| cook / roast / bake | cozinhar / assar / assar | oficial (Cooking.verb "Cozinhar"). "bake" e "roast" ambos "assar" (VCE já usa "assados"). |
| brew / ferment / distill | preparar / fermentar / destilar | oficial (FermentingBarrel "barril de fermentação"; fermentar 10). "brew liquors" → "preparar destilados"; "wort" → "mosto". |
| extract / refine / smelt | extrair / refinar / fundir | oficial (refinar 12; fundir 9). "extracting magicyte from" → "extraindo magicita de"; "extract soul" → "extrair alma". |
| install / implant / remove | instalar / implantar / remover | oficial (Jobs "implantar braço protético"; remove "removendo"). Próteses → "instalar" (jobString do mod: "Installs X"); órgãos/implantes → "implantar". |
| tame / train / slaughter / butcher / hunt | domar / treinar / abater / esquartejar / caçar | oficial (Slaughter "abatendo"; Hunt "caçando"; Cooking desc "esquarteje animais"; "mesa de açougueiro"). "butcher" (receita) → "esquartejar"; "butcher sign" → "placa de açougue". |
| build / deconstruct / repair / haul / clean | construir / desconstruir / reparar / carregar / limpar | oficial (Construction.verb "Construir"; Deconstruct "desconstruindo"; Repair "reparando"; Haul "carregando"; Clean "limpando"). |
| research / study / meditate | pesquisar / estudar / meditar | oficial. "researching." → "pesquisando." |
| enchant / invoke / pacify / recruit / heal / tend | encantar / invocar / pacificar / recrutar / curar / cuidar de | repo/oficial ("Invoque dríades"; "tentando recrutar"; TendPatient "Cuidando de"; Doctor.verb "Tratar de"). "pacify" novo ("pacificar"); "tend" → "cuidar de". |

## Moedas da campanha (registro retroativo — Task 17)

Termos cunhados nos lotes L1–L4 e já em uso no repo; este quadro só documenta (nenhum valor foi alterado).

| EN | PT-BR | Obs |
|---|---|---|
| javelin | azagaia | novo (MOBarbarians `pphhyy_Barbarian_RustedJavalin` + receitas). Não confundir com lança (spear) nem pique (pike). |
| antler | galhada | novo (MOBarbarians "elmo de galhada do escolhido", `pphhyy_Barbarian_MakeChosenAntler`). |
| entosomnia / entosomnic | entossonia / entossônico | novos (MedMedsMO `Entosomnia`; "caixão entossônico"). |
| Ambroisen (material) | paresiano | novo (MedMedsMO/MOTweaks "braço paresiano", `AmbroisenMedArm`). |
| eyepatch / earpatch | tapa-olho / tapa-orelha | novos (Prosthetics `EyePatch`, `InstallEarPatch`); hifenizados, plurais "tapa-olhos"/"tapa-orelhas". |
| pebble | pedrisco | já na linha pedra/mármore (FortMaterial); registrado aqui como moeda da campanha. |
| kettle helm (capelina) | capelina | obs: termo do externo (MO) para kettle helm — não adotado; a campanha usa "chapéu-de-ferro" (linha de elmos). |
| rox / roxberry | rox / roxberry | já na linha cheese/roast/stew/rox; "rox" invariável em compostos ("queijo de rox", "stout de roxberry"). Task 17 normalizou "roxwood" → "rox". |
| kettle helm | chapéu-de-ferro | já na linha de elmos; moeda da campanha (Ignivar `Ignivar_Kettle_Face`), alternativa a "capelina". |
