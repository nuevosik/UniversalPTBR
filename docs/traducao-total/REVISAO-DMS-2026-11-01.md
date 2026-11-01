# Revisão das traduções DMS — 2026-11-01

Escopo: 164 arquivos `*DeadManSSwitch*` (DMS base + Expedition, AncientCorps, MobileDragoon, Motorized, Synthetic, Taktikmagi, ControlSpi) — 6.570 entradas.
Método: checagem mecânica (XML, placeholders, chaves vazias) + revisão linguística por 10 agentes Haiku 5.5 em paralelo. Os itens críticos abaixo foram conferidos por grep no arquivo; nenhum arquivo foi editado.

## Checagem mecânica

- XML válido nos 164 arquivos.
- Nenhum placeholder `{…}`/`[…]` desbalanceado ou com nome traduzido; nenhum valor vazio.

## 1. Críticos — texto quebrado/placeholder aparecendo no jogo

| Arquivo:linha | Chave | Atual | Correção |
|---|---|---|---|
| DefInjected/DMS_Story.DialogueDef/DeadManSSwitch_DMS_Story.DialogueDef.xml:3 | FirstGreeting.title | `殖民地辦公室` (chinês) | Escritório Colonial |
| Keyed/DeadManSSwitchExpedition_Keys.xml:344 | DMSE.Letter.HuntdownThreat.Text | `(A FAZER) blablabla, de qualquer forma, {0} quer você morto.` | texto final sem "(A FAZER) blablabla" |
| DefInjected/Fortified.HuntdownDef/DeadManSSwitchAncientCor_Fortified.HuntdownDef.xml:3 | DMSAC_Huntdown.letterText | `DMSAC_Huntdown_LetterText` (nome da chave) | traduzir o texto real |
| DefInjected/RecipeDef/DeadManSSwitchControlSpi_RecipeDef.xml:17 | RKCS_ImplantControlSpine.label | `RKCS_ControlSpine` (defName) | implantar coluna de controle |
| DefInjected/RecipeDef/DeadManSSwitchExpedition_RecipeDef.xml:41 | DMSE_Make_MedicineUltratech.description | `a fazer` | Produz remédio de mundo brilhante. |
| DefInjected/ThingDef/DeadManSSwitch_ThingDef.xml:6 | DMS_AMO_Beast.description | `TODO` | conferir o original (pode vir assim do mod) |
| DefInjected/ThingDef/DeadManSSwitch_ThingDef_A.xml:164 | DMS_Gun_Kord.description | `Kord` (repete o rótulo) | conferir o original |
| DefInjected/HediffDef/DeadManSSwitch_HediffDef.xml:58 | DMS_ProstheticSpine.labelNoun | descrição inteira com `\n\n` | `coluna vertebral neuromecânica` |

## 2. Texto truncado (confirmar com o original EN)

- DefInjected/ThingDef/DeadManSSwitchControlSpi_ThingDef.xml:3 — `Polarisbloc_NibelungStandardArmor.description` termina em "é proibida para uso por..."
- DefInjected/ThingDef/DeadManSSwitchControlSpi_ThingDef.xml:11 — `RKCS_NanoBlade.description` termina em "melhorar o desempenho, ren..."
- DefInjected/GeneDef/DeadManSSwitch_GeneDef.xml:6 — `DMS_Gene_FrogmanGestation.description` termina em "a mesma sentença, uma..." (pode ser proposital)
- DefInjected/ThingDef/DeadManSSwitch_ThingDef.xml:441 — `DMS_Mech_Frogman.description` termina em "..." (pode ser proposital)

## 3. Palavras inexistentes / frases quebradas

| Arquivo:linha | Atual | Correção |
|---|---|---|
| ThingDef/DeadManSSwitch_ThingDef.xml:233 | "estamponentes" | conferir EN (provavelmente "componentes"/"próteses") |
| ThingDef/DeadManSSwitch_ThingDef.xml:492 | "A extração para se a estela se esgotar" | "A extração para quando a estela se esgotar" |
| ThingDef/DeadManSSwitch_ThingDef.xml:195 | "pode rachadura carcaças" | "pode rachar carcaças" |
| ThingDef/DeadManSSwitchMobileDrag_ThingDef.xml:188 | "uso antifuertes" (espanhol) | "uso antifortificação" |
| ThingDef/DeadManSSwitch_ThingDef_A.xml:71 | "contrafranco" | conferir EN ("contra-atirador"?) |
| RecipeDef/DeadManSSwitch_RecipeDef.xml:244 | "pontos de banda de banda" | "pontos de banda" |
| ResearchProjectDef/DeadManSSwitch_ResearchProjectDef.xml:76 | "seu padrão padrão" | "no padrão" |
| Keyed/DeadManSSwitchControlSpi_Keys.xml:73-74 | "Sortida" | "Surtida" |
| PawnKindDef/DeadManSSwitchControlSpi_PawnKindDef.xml:35 | "perfuro do coro noturno" | "perfurador do coro noturno" |
| ThingDef/DeadManSSwitch_ThingDef_A.xml:149 | "câmara de vácuo … ambiente de alta pressão" | conferir EN |

## 4. Gramática (concordância, regência, ortografia)

- Keyed/DeadManSSwitchAncientCor_Keys.xml:48 — "Uma esquadrão" → "Um esquadrão"
- Keyed/DeadManSSwitchAncientCor_Keys.xml:31 — "Nível O {0}" (letra O) → "Nível 0 {0}"
- Keyed/DeadManSSwitchExpedition_Keys.xml:41 — "a tripulação se reagrupem e redefinam" → "se reagrupe e redefina"
- Keyed/DeadManSSwitchControlSpi_Keys.xml:57 — "no persona" → "na persona"
- ResearchProjectDef/DeadManSSwitch_ResearchProjectDef.xml:64 — "seu cápsula" → "sua cápsula"
- ResearchProjectDef/DeadManSSwitch_ResearchProjectDef.xml:83 — "mother-drones não tripuladas" → "drones-mãe não tripulados"
- ThingDef/DeadManSSwitchExpedition_ThingDef.xml:236 — "por um célula" → "por uma célula"
- ThingDef/DeadManSSwitchExpedition_ThingDef.xml:266 — "por a luz verde ser…" → "como a luz verde é…"
- ThingDef/DeadManSSwitchExpedition_ThingDef.xml:276-279, 320 — "vôo" → "voo"
- WorldObjectDef/DeadManSSwitchExpedition_WorldObjectDef.xml:5-7 — "Capsulas/capsulas" → "Cápsulas/cápsulas"
- ThingDef/DeadManSSwitch_ThingDef.xml:569 — "que conecta-se" → "que se conecta"
- AbilityDef/DeadManSSwitch_AbilityDef.xml:45 — "bioreator" → "biorreator"
- AbilityDef/DeadManSSwitch_AbilityDef.xml:28 — "para reagir seu combustível" → "para fazer seu combustível reagir"
- JobDef/DeadManSSwitchExpedition_JobDef.xml:10 — "aterro em TargetA." → "aterrando em TargetA."
- ResearchProjectDef/DeadManSSwitch_ResearchProjectDef.xml:55 — "auto-liberação" → "autoliberação"
- RoyalTitleDef/DeadManSSwitch_RoyalTitleDef.xml:6 — ".." → "."

### Placeholders de pronome (BackstoryDef)

`[PAWN_pronoun]` (ele/ela) usado onde cabe possessivo — ~11 ocorrências em DefInjected/BackstoryDef/DeadManSSwitch_BackstoryDef.xml (linhas 108, 113, 114, 117, 121, 126, 129, 130, 132, 138) e DeadManSSwitchTaktikmagi_BackstoryDef.xml:27, 33. Ex.: "usa [PAWN_pronoun] habilidades" → "usa [PAWN_possessive] habilidades"; "O trabalho de [PAWN_pronoun]" → "[PAWN_possessive] trabalho". Linha 108 também tem "recorri" → "recorreu".

## 5. Mistraduções

- ResearchProjectDef/DeadManSSwitchExpedition_ResearchProjectDef.xml:10 — `DMSE_Carbohydrate.label` "Síntese de carbono" → "Síntese de carboidratos"
- Exosuit.CE.NPCAmmoPresetDef/DeadManSSwitchMobileDrag_…xml:3 — `ShotgunAntiAir` "antiblindagem" → "antiaérea"
- ThingDef/DeadManSSwitchExpedition_ThingDef.xml:40 — "lançador antiaéreo ombro a ombro" → "lançador antiaéreo portátil de ombro"
- BodyDef/DeadManSSwitch_BodyDef.xml:325 — "veículo quadripista" → "veículo de quatro esteiras"
- HistoryEventDef/DeadManSSwitch_HistoryEventDef.xml:9 — "tecnologia oculta" → "tecnologia lacrada" (como no resto do arquivo)
- ResearchProjectDef/DeadManSSwitchExpedition_ResearchProjectDef.xml:16 e :28 — dois projetos diferentes com o mesmo rótulo "engenharia avançada de mísseis"

## 6. Inglês que ficou no texto

- **automatroid / automatroide / automatóide / autômatoide / automatron**: ~105 ocorrências, contra o glossário (`automatroid → autômato`, aprovado). É o maior problema de consistência do DMS; dá para corrigir em lote, mas revisando caso a caso, porque "Automatroid" às vezes é nome de facção.
- Missile*: "incoming", "loiter", "homing", "pulsejet", "gantry", "retrofit" (DMSE.MissileBodyDef:11/13/23/27, MissilePartDef:143/147, ThingDef Expedition:208/230, Keyed Expedition:379)
- "hosts de registros" (ThingDef DMS:284), "emplacements" (:188), "mother-drones" (:476; ResearchProjectDef:83), "regrowth" (HediffDef:161), "mechs" (MobileDrag:204), "mechlinks" (AncientCor ThingDef:20), "pad central" (Keyed DMS:73), "biomatroid" (RecipeDef:253), "glitterworld" (Expedition RecipeDef:43)
- PawnKindDef/DeadManSSwitch_PawnKindDef.xml:95-100 — "hound", "watchdog", "verling bird" (os irmãos usam "sabujo", "pássaro Verling")
- "rimworld" nos baseDesc do BackstoryDef → "mundo da borda" (como nos .description)
- Mistura de "tarbosaurus" e "tarbossauro" (SitePartDef:6-7)

## 7. Inconsistências de termo (decidir um padrão)

- mapa-múndi × mapa-mundo × mapa mundial × "mapa grande"
- blocos × setores (tile do mundo)
- guarda-túmulos × guardião tumular × coveiro; "Sepulturero"/"Velador" (espanhol; confirmar se é nome original de variante)
- lacrado × selado (Occultech)
- aço-tungstênio × tungstênio-aço
- autocanhão × canhão automático
- psinjurador (glossário) × psicasta × conjurador
- mecanoide × mecânico × de mecha
- terra-ar × superfície-ar
- interferência × bloqueio (jamming); orientação × guia (guidance channels); ranhura × compartimento (slot)
- 76,2 × 76.2 (separador decimal)
- Dragão × Dragoon; GAU-19/A × GAU19/A; Hírax × damão; Falcon × Falcão; Ishmael × Izhmal
- jabuti × geochelone; tecelão de enxames × de aglomerados
- **Night Choir × Coro Noturno × Coral Noturno**: os três aparecem no repositório e os revisores discordaram entre si; precisa de decisão.
- **mecanitor × mecanizador**: os dois aparecem no repositório (50 × 74); vale fixar um no glossário.

## 8. Precisa conferir contra o def original

- BodyDef/DeadManSSwitch_BodyDef.xml:29 e :36 — chaves `trigger_safty`/`weapon_safty` duplicam `trigger_safety`/`weapon_safety` (linhas 308-309). Uma delas não é injetada; manter a que bate com o defName do mod (o erro de digitação pode estar no próprio mod).

## Correções aplicadas (2026-11-01)

**DMS: 59 trocas em 24 arquivos.** Cobrem todos os itens das seções 1, 3 e 4 e os itens claros da seção 5. Exceções, mantidas como estão:
- `DMSAC_Huntdown.letterText` = `DMSAC_Huntdown_LetterText` **não é erro**: o def guarda a chave e o texto vem de `Keyed/DeadManSSwitchAncientCor_Keys.xml:30`.
- `TODO` (DMS_AMO_Beast), `Kord` (DMS_Gun_Kord) e `a fazer` em `ScenarioDef/DeadManSSwitchExpedition_ScenarioDef.xml:3` (DMSE_Deviant): provavelmente vêm assim do mod original; conferir com o EN.
- "câmara de vácuo … alta pressão", "tecnologia oculta" e os textos truncados ficam até a comparação com o EN.
- `[PAWN_possessive]` foi trocado por "seu/sua" fixo (ou por `[PAWN_nameDef]` quando era objeto), porque o possessivo do LanguageWorker não concorda com o substantivo.
- Seções 6-8 (inglês remanescente, automatroid, padronização de termos, chaves `*_safty`) **não** foram tocadas: dependem de decisão de glossário.

**Alpha Mechs: 28 trocas em 8 arquivos** (revisão Haiku 5.5 em 2 lotes, 22 arquivos):
- biomicanoide → biomecanoide; "Malícia incarnada" → "encarnada"; "um centopeia canhoneiro" → "uma centopeia canhoneira"; "Se desativado… serão substituídos" → "será substituído" (3×)
- Família siege: quebra-sitios → quebra-cercos (siegebreaker) / quebra-mecas (armadura e capacete mechbreaker); funde-sitios → fundidor de cerco (como no PawnKindDef)
- "do Falangista" → "da falange"; pellet(s) → pélete(s); "Dropado pelo" → "Obtido ao derrotar o"; "Behemoth Gelado" → "beemote gelado"
- sagittarius → sagitário (ThingDef e RecipeDef, igual ao PawnKindDef); BodyDef "gutter-snipe" → "sugador de sarjeta"
- ultra-pesado → ultrapesado (7×); "pessoas não incapacitados" → "incapacitadas"; "sucumbiu à congelamento" → "ao congelamento"
- "warcasket mestre de mechas" / "Mestre-Mecha" → "carcaça de guerra mestra de mecas"

**DMS — automatroid → autômato (18 arquivos):** todas as variantes (automatroid, automatroide(s), automatóide(s), autômatoide(s), automatron(s)) foram padronizadas nos valores; as chaves não mudaram. Usos de adjetivo ou marca foram reformulados: "tecnologia de autômatos", "uso por autômatos", "arma de autômato", "facão/Machete de autômato", "Gestar autômato Armiman", "da Polarisbloc e dos autômatos", "autômato(s) ultrapesado(s)". Nenhuma ocorrência restante no DMS. Fora do DMS ainda há ocorrências em AscensionMegacorp (ThingDef/BackstoryDef) e SearchRescue_Keys, que não foram tocadas.

Pendente no Alpha Mechs (decisão ou original EN):
- `AM_Starfire.description` truncado ("só é implantado...")
- `AM_RandomItems` = "Montagem de recursos em" (provavelmente concatenado pelo código)
- Padronização de nomes: ínferno × infernus, óptio × optio, imperatriz da/de guerra × guerreira, pernalta imaculado × andarilho pristino, derrete-cerco × fundidor de cerco, mestre de cerco × destruidor de cerco, quebra-cerco × quebra-cercos
- Unidade de raio: blocos × células × quadrados
- Chaves `AM_Bullet_*` e `AMVPE_*` definidas em dois arquivos DefInjected (possível injeção duplicada)

## Segunda revisão — aplicada

**35 correções em 14 arquivos** (DMS + Alpha Mechs): todos os itens de "Correções que escaparam / erros claros" e "Possessivos restantes" listados abaixo, exceto "Sistema de proteção ativa", que está correto (é o termo padrão para *active protection system*). Também foi trocado "não-augmentado" → "sem aprimoramentos" (Taktikmagi:21). Os itens de "Inglês remanescente" e "Para conferir com o EN" continuam pendentes.

## AscensionMegacorp (40 arquivos, 1.216 entradas) — revisado e corrigido

Já estava 100% traduzido (nenhuma entrada inteira em inglês, placeholders íntegros). Revisão Haiku 5.5 (2 agentes) + checagem mecânica; **23 correções em 7 arquivos**:
- automatroides → autômatos (4×); [PAWN_possessive] → "seu corpo", "da mesma idade", "os pais"; "ultra-pesado" → "ultrapesado"
- mechlink/mechalink → meca-conexão (glossário); "Canhão autocannon Bushmaster" → "Autocanhão Bushmaster"
- "Um rifle de precisão reformado" (metralhadora leve) → "Uma metralhadora leve reformada"; "Um ligação" → "Uma ligação"; "linha falha" → "linha defeituosa"
- Keyed: "A Rising Giant" → "Um Gigante em Ascensão"; "Você são" → "Vocês são"; "Incidenciais" → "Incidentais"; "Sacolas de cadáver" → "Sacos para cadáveres"; "sinalizador" → "farol" (como no resto do arquivo)

Mantidos de propósito: rótulos `TERMINAL_FINANCEIRO`/`ARMADURA_CORTANTE` etc. (estilo de terminal da UI, já em PT); "um ala autônomo" (ala = parceiro de voo, masculino); "M88 Rocky saqueado" (pode significar "capturado"; conferir EN).

Pendente no AscensionMegacorp: chaves `UASC_Radiotoxicity.*` (DamageDef) — prefixo difere de `USAC_`; conferir o defName no mod, senão a injeção falha; "deputado" (USAC_Military03.titleShort); "neuro-reforçador" × "neuro-potenciador"; "mecanitor" × "mecanizador"; "mecha" × "mecanoide"; debugLabels em inglês no PawnRenderTreeDef.

## Pendentes resolvidos (Haiku 5.5, 10 agentes) — aplicado

Os agentes propuseram trocas em JSON (sem editar arquivos); revisei as ~383 propostas, descartei 7 e corrigi 3, e apliquei **376 trocas em 65 arquivos** com verificação por entrada (texto exato, tags e placeholders idênticos). Comparação com o backup: 372 valores alterados, nenhuma chave perdida, nenhum placeholder alterado, XML válido nos 259 arquivos.

Decisões aplicadas (glossário ou forma majoritária):
- mecanitor → **mecanizador**; mapa-mundo / mapa mundial / "mapa grande" → **mapa-múndi**; setores → **blocos**; saqueador → **invasor**; gantry → **pórtico**; psilink → **psylink**; psicasta/conjurador (psycaster) → **psinjurador**; mechlink(s) → **meca-conexão(ões)**
- Night Choir / Coral Noturno → **Coro Noturno**; Occultech selado → **lacrado**; tungstênio-aço → **aço-tungstênio**; canhão automático → **autocanhão**; superfície-ar → **terra-ar**; Dragoon → **Dragão**; 76.2 → **76,2**; GAU19/A → **GAU-19/A**
- Inglês traduzido: Hound/watchdog/Verling bird, Rimworld, antistealth, inbound, airburst, loiter, homing, pulsejet, retrofit, gantry, pod, host, emplacements, regrowth, mechs, Synths, psicocasts, splicers, voidlink, beamcaster, neurolink, Dominion, Apoptosis, guttersnipe, legate, optio, polychoron, scriptomaton, sanguinarius, Vanilla, debugLabels
- Nomes unificados com o PawnKindDef: tarbossauro, guarda-túmulos, tecelão de enxames, jabuti, damão, dogue, tartaruga-careta, dama, cão de combate, cão infernal, homem-rã, pássaro açougueiro, Falcão, Izhmal; Alpha Mechs: ínferno, óptio, sanguinário, imperatriz da guerra, quebra-cercos, mestre de cerco, fundidor de cerco, oceanus, geneticor, scriptômato, (…) imaculado; Cinders: Lápide, artilheiro de guerra, turbilhão blindado, flechete, "estilo original"; Ascension: neuro-potenciador

Descartados de propósito: "biomatróide" (fica "biomatroide"), tradução de "Gatekeeper" (nome próprio), "Sistema de proteção ativo", troca de "neuro-reativador".

**Ainda pendente** (precisa do texto original em inglês): textos truncados (Polarisbloc armor, NanoBlade, FrogmanGestation, Starfire, Alien_Cinder), TODO/"A FAZER"/"Kord"/"/" (provavelmente originais), chaves `trigger_safty`/`weapon_safty` (DMS BodyDef) e `UASC_Radiotoxicity` (Ascension), "lenha", "deputado", "talabardas", "flabelo", "M88 Rocky saqueado", `DMS_LandCrab.label`, `DMSAC_StructuralDamage.labelNoun`, `AM_RandomItems`; 

**mecha/meca → mecanoide (decisão do usuário, 2026-11-01):** 166 valores em 39 arquivos dos quatro mods (DMS, Alpha Mechs, Ascension, Cinders); "mecha(s)"/"meca(s)" → "mecanoide(s)" (mesmo gênero, sem ajuste de concordância). Compostos: "meca-conexão" mantido (mechlink, glossário); "um meca-imperatriz da guerra ultrapesado" → "um mecanoide ultrapesado imperatriz da guerra"; "Gestar um meca-irmã mais velha" → "Gestar uma mecanoide irmã mais velha". Backup: scratchpad `backup_mecanoide.zip`.

## Cinders of the Embergarden (33 arquivos, 949 entradas) — revisado e corrigido

Já estava 100% traduzido; placeholders íntegros. Revisão Haiku 5.5 (2 agentes) + checagem mecânica; **34 correções em 8 arquivos**:
- BackstoryDef: 20 usos de `[PAWN_possessive]` reescritos ("seus pais", "sua perna", "Em seus longos sonhos", "sua história"…); "metade do corpo queimada" → "queimado"; "Conselho Nacional de Defesa"/"de Defesa Nacional" → "Conselho de Defesa" (como no resto); "naves-terrestre" → "navios de assalto terrestre"
- ThingDef: "Um antigo submetralhadora" → "Uma antiga submetralhadora"; "saqueadores" → "invasores"; "ultra-pesados" → "ultrapesados"
- WeaponTraitDef: "telémetro" → "telêmetro"; "auto-carregamento" → "autocarregamento"
- AlienRace: removida a nota do tradutor "(nota: a ser verificado)"
- Keyed: "Fumée Misericordioso" → "Misericordiosa" (a narradora é uma garota)
- HediffDef: "Hediff oculto" → "Condição oculta"; AbilityDef: "Lançar míssil" → "Lança um míssil." (2×)

Mantidos de propósito: 8 descrições "TODO"/"A FAZER" de armas montadas (vêm assim do mod); `Cinder_TentacleTrap.description` = "/" (provavelmente original); nomes "Tombstone", "Needle PDW", "flechette".

Pendente (conferir com o original): `Alien_Cinder.description` parece truncada (descreve só a primeira de duas reações); `Cinder_Culture.label` = "lenha"; "torrente blindada" × "turbilhão blindado"; "guerreiro de guerra" × "artilheiro de guerra"; "estilo Vanilla" (Keyed:10, 18).

## Segunda revisão (Haiku 5.5, 12 agentes, 186 arquivos) — achados

As correções anteriores foram confirmadas no lugar; não foi encontrado nenhum erro de concordância introduzido pela troca automatroid → autômato. Os apontamentos novos abaixo foram conferidos por grep.

**Correções que escaparam / erros claros**
- AlphaMechs_ThingDef.xml:215 — "sua torre funde-sitios" (sobrou da troca) → "sua torre de fundidor de cerco"
- AlphaMechs_ThingDef.xml:62 — "por um canhoneiro centopeia" → "por uma centopeia canhoneira"; :292/:298 "centopeia artilheira" → "centopeia canhoneira"
- AlphaMechs_ThingDef.xml:189 — "O turbocompressor paira" → "O turbolimpo paira" (o label é turbolimpo)
- AlphaMechs_VFEPirates.WarcasketDef.xml:8 — "ombrageiras" → "ombreiras"
- ResearchProjectDef/DeadManSSwitch_ResearchProjectDef.xml:59 — "A fornecimento" → "O fornecimento"; :30 "unidades autômato menores" → "unidades autômatas menores"
- ThingDef/DeadManSSwitchExpedition_ThingDef.xml:296 — "um camuflagem" → "uma camuflagem"
- ThingDef/DeadManSSwitch_ThingDef.xml:618-619 — "Invasione(-o)" → "Hackeie(-o)"; :280 "em salvos" → "em salvas"; :244/247/250 "ocutécnica" → "ocultécnica"
- ThingDef/DeadManSSwitch_ThingDef_A.xml:215 — "Os amigos de batalha" → "Os camaradas de batalha"; :8 "não-conscriptos" → "não conscritos"
- ThingDef/DeadManSSwitchControlSpi_ThingDef.xml:7 — "Ao contrário dos trajes táticos, como os Óculos…" → sem "como"
- ThingDef/DeadManSSwitchMobileDrag_ThingDef.xml:167 — "Sistema de proteção ativa" → "ativo"
- Keyed/DeadManSSwitchExpedition_Keys.xml:749 — chave `DMSE.Transfer.UI.Eta` traduzida como "Fator de consumo de combustível" → "Tempo estimado de chegada"
- Keyed/DeadManSSwitch_Keys.xml:350 — "sinais comerciais" → "faróis comerciais" (como em :172-173)
- "ultra-pesado(s)" restantes (RecipeDef DMS:256/259/263, SitePartDef:7, ThingDef DMS:476) → "ultrapesado(s)"; "ultra-classe" → "ultraclasse"; "contra-tecnologia" → "contratecnologia"
- AlphaMechs "mecanitas" → "mecanitos"

**Possessivos restantes (`[PAWN_possessive]` / `{X_possessive}`)** — mesma falha já corrigida na 1ª rodada: o possessivo segue o gênero do colono, não do substantivo, e às vezes aparece como objeto.
- DeadManSSwitch_BackstoryDef.xml:112 ("da vida de [PAWN_possessive]"), :131 ("pai biológico de [PAWN_possessive]"), :139 ("apoiar [PAWN_possessive]")
- DeadManSSwitchTaktikmagi_BackstoryDef.xml:3, 6, 15, 21, 30, 39 ("[PAWN_possessive] serviço/pelotão/própria mente/infância/educação")
- Keyed/DeadManSSwitch_Keys.xml:163-164 ("{DEVIANT_possessive} palavra"); Keyed/DeadManSSwitchTaktikmagi_Keys.xml:19 ("{PAWN_possessive} corpo")

**Inglês remanescente (somar à seção 6)**
- DMS: Hound / watchdog / Verling bird / Verlingbird nas estações e máquinas (ThingDef DMS:670-687, 733-734); "Rimworld" (MobileDrag ThingDef:168, 194); "antistealth" (Keyed Expedition:35, 92); "inbound", "airburst" (Expedition ThingDef:320, 322); "pod de gestação" (RecipeDef:253); "host de comando" (SitePartDef:33); "Synths" (XenotypeDef:5); "psicocasts" (HediffDef:175); debugLabels do Synthetic PawnRenderTreeDef
- Alpha Mechs: guttersnipe (ThingDef:147-148), legate, polychoron, slurrypede, scriptomaton, Dominion, Apoptosis, voidlink/voidlinks, beamcaster, neurolink, sanguinarius, splicers

**Para conferir com o EN**: `DMSAC_StructuralDamage.labelNoun` (frase inteira, como era o ProstheticSpine); `DMS_LandCrab.label` = "terrestre"; "flabelo" (Wildfowl); "talabardas" (FT2 Fibre Mill); "Arrowhead"; `{PAWN}` em ControlSpi_Keys:113-114.

## Apontamentos dos revisores que descartei

- "lenta e uniformemente iteradas" está correto (só o último advérbio leva -mente).
- "psicocastes" e "Coral Noturno" como correções obrigatórias: são preferências, não erros.
