# Glossário — Tradução Total (PT-BR)

Mapa EN→PT canônico para os lotes B1–B16 (139 alvos, ~26,3 mil strings). Herda e
complementa `docs/medieval/GLOSSARY.md` — os dois glossários são entregues juntos
aos subagentes. Regras:

- Um termo PT por conceito; não criar sinônimo concorrente dentro do mesmo lote.
- Só o valor é traduzido; nunca renomear chaves, `defName`, arquivos ou pastas.
- Preservar `{0}`, `{PAWN_*}`, `[TOKEN]`, `\n` e a estrutura `LanguageData` (constraint global do repo).
- Fonte: **oficial** = RimWorld PT-BR oficial (`Core`, `Royalty`, `Ideology`, `Biotech`,
  `Anomaly`, `Odyssey`; TARs extraídos em `/tmp/opencode/oficial`); **repo** = já existe
  em `Languages/PortugueseBrazilian`; **externo** = PT de terceiros, só via termos herdados
  do medieval; **novo** = proposto nesta campanha, sem precedente.
- Toda linha `oficial`/`repo` cita arquivo + chave; termos herdados sem chave citam
  `(ver docs/medieval/GLOSSARY.md)`. Divergências entre oficial e repo estão marcadas
  com ⚠️ — **decisão humana** no gate (lista no relatório da Task 5).
- `hediff`, `tier`, `stat`, `bill`: onde oficial e repo divergem, o glossário escolhe UM
  e registra a alternativa em Obs.
- `raider`: **invasor** na campanha total; **saqueador** nos lotes medievais já traduzidos
  (divergência legada — não retraduzir).

## Termos de jogo e UI

| EN | PT-BR | Obs |
|---|---|---|
| pawn | colono | oficial/repo — termo herdado (ver `docs/medieval/GLOSSARY.md`); placeholders `[PAWN_*]` intactos. |
| colony | colônia | oficial — `Core/Keyed/Letters.xml` `LetterRelationsChange_HostileGoodwillDescription`. |
| settlement | assentamento | oficial — `Core/Keyed/MainTabs.xml` `GoodwillTip`. |
| world map / cell (local) / tile (mundo) | mapa-múndi / quadrado / bloco | repo — `Keyed/Outposts.xml` `Outposts_SelectDestination` (mapa-múndi); oficial — `Core/Keyed/Misc_Gameplay.xml` `SelectNextInSquareTip` (quadrado); `Core/Keyed/Dialogs_Various.xml` `ConfirmSettleNearFactionBase` ("dentro de {0} blocos"). |
| stack / storage / stockpile | pilha / armazenamento / estoque | oficial — termo herdado (ver `docs/medieval/GLOSSARY.md`). |
| quest / reward / letter | missão / recompensa / carta | repo — termo herdado (ver `docs/medieval/GLOSSARY.md`). |
| goodwill | boa vontade | oficial — `Core/Keyed/MainTabs.xml` `GoodwillTip`; repo — `Keyed/RelicQuests_Keys.xml` `LetterRelationsChange_HostileGoodwillDescription`. |
| caravan | caravana | oficial — `Core/Keyed/ITabs.xml` `TabFormingCaravan`; repo — `Keyed/Outposts.xml` `Outposts.Commands.AddPawn.Desc`. |
| outpost | posto avançado | oficial — `Core/Keyed/Letters.xml` `LetterFactionBaseDefeated`; repo — `Keyed/Outposts.xml` `Outposts_SelectDestination`; termo herdado (ver `docs/medieval/GLOSSARY.md`). |
| raid | incursão ⚠️ | repo — `DefInjected/RaidStrategyDef/VFE_Empire_RaidStrategyDef.xml` `VFEE_Deserters.letterLabelEnemy` ("Incursão (Desertores)"); divergência oficial: `Core/Keyed/Misc_Gameplay.xml` `<Raid>Invasão</Raid>`. Gate (2026-09-15): mantido `incursão` (aprovado AS-IS). |
| threat | ameaça | oficial — `Core/Keyed/Menus_Main.xml` `DifficultyThreatSection`. |
| mortar | morteiro | oficial — `Core/Keyed/Misc_Gameplay.xml` `<Mortar>morteiro</Mortar>`; repo — `DefInjected/Vehicles.VehicleTurretDef/Generated_3014906877.xml` `Toad_MainTurret.description`. |
| shell | projétil | oficial — `Core/DefInjected/ThingDef/Items_Resource_Shell.xml` `Bullet_Shell_HighExplosive.label` ("projétil de explosão grande"). |
| trap | armadilha | oficial — `Biotech/DefInjected/ThingDef/Buildings_Misc.xml` `TrapIED_ToxGas.label`; repo — `Keyed/Generated_1845154007.xml` `VFES_DesignatorRearmTraps`. |
| rearm | rearmar | repo — `DefInjected/WorkGiverDef/VFE_Security_WorkGiverDef.xml` `VFES_RearmTrap.verb`. |
| bill | tarefa ⚠️ | oficial — `Core/Keyed/ITabs.xml` `TabBills`/`AddBill`; repo divergente: Alpha Animals usa "ordem de serviço" (`Keyed/Generated_1541721856.xml` `AA_DestroyFlamingoEggsDesc`). Gate (2026-09-15): mantido `tarefa` (aprovado AS-IS). |
| queue | fila | oficial — `Core/Keyed/Misc_Gameplay.xml` `AbilityAlreadyQueued` ("já está na fila"). |
| stat | estatística ⚠️ | oficial — `Core/Keyed/ITabs.xml` `<TabStats>Estatísticas</TabStats>`; "attributes" é que é `atributos` (`Core/Keyed/Dialogs_Various.xml` `<Attributes>`). Brief sugere "atributo"; Gate (2026-09-15): mantido `estatística` (aprovado AS-IS). |
| hediff | ferimento / condição de saúde | oficial — `Core/Keyed/ITabs.xml` `UntendedInjury`; `Core/Keyed/Letters.xml` `LetterHediffFromRandomHediffGiver` ("condição de saúde"). Traduzir por contexto; nunca deixar "hediff". |
| research / project | pesquisa / projeto | oficial — `Core/Keyed/MainTabs.xml` `<Research>Pesquisar</Research>`, `ActiveProject`. |
| techprint | projeto técnico | oficial — `Core/Keyed/MainTabs.xml` `ResearchTechprintRequirement` ("Projetos técnicos"). |
| tier | nível ⚠️ | repo divergente: `Keyed/Generated_3014906877.xml` `VVE_Tier0` = "Camada 0" (descrição usa "nível 0"). Gate (2026-09-15): mantido `nível` (aprovado AS-IS). |
| upgrade | melhoria ⚠️ | repo divergente: `Keyed/VehicleFramework_Keyed.xml` `VF_Upgradeable` = "Aprimorável"; `Keyed/VFE_Insectoids_Keys.xml` `VFEI_HiveCannotBeUpgradedMore` usa "melhorar". Gate (2026-09-15): mantido `melhoria` (aprovado AS-IS). |
| wall | parede / muralha ⚠️ | oficial "parede"; medieval/repo `DefInjected/ThingDef/FortMedieval_ThingDef.xml` `FT_CastleWall.label` = "muralha de castelo". "muralha" em fortificação/medieval, "parede" em moderno. |
| perimeter | perímetro | novo — WD2 `TSA_WorldDomination.OutpostUpgradeDef` ("perimeter walls", "trap perimeter"). |
| area / zone | área / zona | oficial — `Biotech/DefInjected/ConceptDef/Tutor.xml` `PollutedTerrain.helpText` ("ZONA DE REMOÇÃO DE POLUIÇÃO"). |
| ideoligion / meme | ideologia / meme | oficial — `Ideology/Keyed/Misc_Gameplay.xml` `Ideo` = "ideologia", `MemesLower` = "memes". |

## Facções, guerras e diplomacia

| EN | PT-BR | Obs |
|---|---|---|
| faction | facção | oficial — `Core/Keyed/MainTabs.xml` `GoodwillTip`. |
| empire | império | oficial — `Royalty/DefInjected/FactionDef/Faction_Empire.xml` `Empire.description`. |
| royal title | título real | oficial — `Royalty/Keyed/MainTabs.xml` `WorkDisabledByRoyalTitle`. |
| noble | nobre | repo — termo herdado (ver `docs/medieval/GLOSSARY.md`). |
| lord (sistema Lord/LordJob do CQF) | lorde | oficial usa "lorde" em backstories (Solid_Adult) e "senhor" como título; no CQF adota-se "lorde" para o sistema e "senhor" permanece o título do glossário medieval. Divergência de contexto, não retraduzir. |
| vassal | vassalo | repo — `Keyed/VFE_Empire_Keyed.xml` `VFEE.ReleaseAllVassals`. |
| allegiance | lealdade | novo — WD2 `TSA_WD_AllegianceLock_Title`; sem precedente. |
| diplomacy | diplomacia | oficial — `Core/DefInjected/BackstoryDef/Offworld_Nonspecific_Adult.xml` `Bartender62.description`; repo — `BackstoriesPatch_BackstoryDef.xml` `GTF_CommonerLord45`. |
| coalition | coalizão | novo — WD2 `TSA_WD_Diplo_Block_Coalition`. |
| conquest | conquista | oficial — `Core/DefInjected/BackstoryDef/Solid_Adult.xml` `ImperialGeneral27.description`; repo — `VFE_Medieval2_BackstoryDef.xml` `VFEM_Knight51`. |
| attrition | atrito | novo — WD2 `TSA_WD_Diplo_AttritionMult`. |
| garrison | guarnição | oficial — `Odyssey/DefInjected/LandmarkDef/Landmarks.xml` `AncientGarrison.label`; repo — `VFE_Medieval2_BackstoryDef.xml` `VFEM_Castellan56`. |
| reinforcement | reforço | oficial — `Biotech/DefInjected/QuestScriptDef/Script_SanguophageShip.xml`; repo — `DefInjected/IncidentDef/Generated_2023507013.xml` `VSE_Reinforcements.label`. |
| raider | invasor | oficial — `Core/Keyed/Menus_Main.xml` `Difficulty_RaidLootPointsFactor_Info` ("pelos invasores"). Divergência legada: "saqueador" nos lotes medievais já traduzidos — não retraduzir (ver regra no topo). |
| deserter | desertor | oficial — `Core/DefInjected/BackstoryDef/Offworld_Nonspecific_Adult.xml` `Defector78.title`; repo — `DefInjected/FactionDef/VFE_Empire_FactionDef.xml` `VFEE_Deserters.label`. |
| mercenary | mercenário | repo — termo herdado (ver `docs/medieval/GLOSSARY.md`). |
| spy ops | operações de espionagem | novo — WD2 `TSA_WD_GoodwillMsg_SpyOpFailure`; sem precedente. |
| supply line | linha de suprimentos | novo — WD2 ("supply lines"); sem precedente. |
| siege | cerco | repo — `DefInjected/Vehicles.VehicleDef/Generated_3014906877.xml` `VVE_Udar_Blueprint.description` ("arma de cerco"). |
| artillery | artilharia | repo — `DefInjected/Vehicles.VehicleDef/Generated_3014906877.xml` `VVE_Udar_Blueprint.description` ("unidade de artilharia"). |
| bombardment | bombardeio | oficial — `Core/DefInjected/ThingDef/RangedSpecial.xml` `OrbitalTargeterBombardment.description` ("bombardeiam a área"). |
| anti-air | antiaéreo | novo — WD2 `TSA_WD_Upgrade_AntiAirGun`. |
| flak | flak / antiaéreo ⚠️ | oficial traduz "flak jacket" como "jaqueta de artilharia" (`Core/DefInjected/ThingDef/Apparel_Various.xml` `Apparel_FlakJacket.label`); para "flak fire" da WD2 preferir "fogo antiaéreo". Gate (2026-09-15): mantido `flak / antiaéreo` (aprovado AS-IS). |
| IED | IED (manter) | oficial — `Biotech/DefInjected/ThingDef/Buildings_Misc.xml` `TrapIED_ToxGas.label` ("Armadilha IED tóxica"). |
| palisade | paliçada | repo — `DefInjected/ThingDef/VFE_Medieval2_ThingDef.xml` `VFEM2_Palisade.label`; WD2 `Upgrade_PalisadeWalls`. |
| watchtower | torre de vigia | novo — WD2 `TSA_WD_Upgrade_WoodenWatchTower`. |
| embassy | embaixada | novo — WD2 `TSA_WD_Outpost_Embassy`; sem precedente. |
| intel | informações | novo — WD2 ("intel"); não usar "inteligência" (colide com a habilidade). |
| world domination | domínio mundial | novo — nome/jargão da WD2. |

## Mechas, robótica e próteses

| EN | PT-BR | Obs |
|---|---|---|
| mech / mechanoid | mecanoide | oficial — `Core/DefInjected/ThingDef/Races_Mechanoid.xml` `Mech_Lancer.description`; repo "mecanoide" (117). |
| mechanitor | mecanizador | oficial — `Biotech/Keyed/MainTabs.xml` `MissingRequiredMechanitor` ("colono mecanizador"). |
| mechlink | meca-conexão | oficial — `Biotech/DefInjected/ConceptDef/Tutor.xml` `Mechanitors.helpText`. |
| mech gestator | gestador mecanoide | oficial — `Biotech/DefInjected/WorkGiverDef/WorkGivers.xml` `DoBillsMechGestator.label`. |
| bandwidth / control group | banda-larga / grupo de controle | oficial — `Biotech/DefInjected/ConceptDef/Tutor.xml` `Mechanitors.helpText`. |
| automatroid | autômato ⚠️ | novo — DMS `DMS_Legacy.description` (esqueleto B3); alternativa: manter "automatroid" como nome de facção. Gate (2026-09-15): mantido `autômato` (aprovado AS-IS). |
| bionic | biônico | oficial — `Core/DefInjected/HediffDef/Hediffs_BodyParts_Bionic.xml` `BionicArm.label`. |
| prosthetic | prótese | oficial — `Core/DefInjected/HediffDef/Hediffs_BodyParts_Prosthetic.xml` `CochlearImplant.label`. |
| implant | implante | oficial — `Core/DefInjected/HediffDef/Hediffs_Global_Misc.xml` `BrainShock.description` ("implantes cerebrais"). |
| archotech | arquotecnológico | oficial — `Core/DefInjected/BackstoryDef/Offworld_Glitterworld_Adult.xml` `NavyScientist52.description`; repo — `VRE_Archon_XenotypeDef.xml` ("arquotecnologia"). |
| drone | drone | novo — manter estrangeirismo; sem precedente no repo. |
| turret | torreta | oficial — `Core/DefInjected/ThingDef/Buildings_Mech.xml` `Turret_AutoMiniTurret.label`. |
| sensor | sensor | oficial — `Anomaly/DefInjected/ResearchProjectDef/ResearchProjects_Anomaly.xml`; repo — `VQE_Ancients_BackstoryDef.xml` `VQE_IsolationChamber14`. |
| reactor | reator | oficial — `Anomaly/DefInjected/MutantDef/Mutants.xml`; repo — `VQE_Generator_BackstoryDef.xml` `VQE_ControlSystemsEngineer03`. |
| radiation | radiação | oficial — `Biotech/DefInjected/GeneDef/GeneDefs_Spectrum.xml` `UVSensitivity_Intense.description`. |
| uranium | urânio | oficial — `Biotech/DefInjected/ThingDef/Buildings_Misc.xml` `ShuttleCrashed_Exitable.description`. |
| plutonium | plutônio | novo — Dubs Rimatomics (sem precedente no jogo base). |
| turbine | turbina | novo — Dubs Rimatomics `DubsRimatomics_ThingDef.xml` `Turbine.description`. |
| cooling tower | torre de resfriamento | novo — Dubs Rimatomics. |
| spent fuel | combustível nuclear gasto | novo — Dubs Rimatomics; "combustível" já é oficial (repo `VEE_RadioactiveBarrel`). |
| tesla coil | bobina de Tesla | novo — Dubs Rimatomics. |
| gantry | pórtico (ou manter "gantry") ⚠️ | novo (pendente) — brief manda manter o original; **nenhuma ocorrência** nos esqueletos B1–B16 (defs). Gate (2026-09-15): mantido `pórtico (ou manter "gantry")` AS-IS; se aparecer em Keyed, aplicar a decisão. |

## Ciência, pesquisa e energia

| EN | PT-BR | Obs |
|---|---|---|
| tech level | nível tecnológico | oficial — `Core/Keyed/Enums.xml` `TechLevel_Neolithic` = "Neolítico"; repo — `DefInjected/VEF.Planet.HireableFactionDef/VFE_Pirates_HireableFactionDef.xml` `Pirate.description` ("nível tecnológico"). |
| industrial / medieval / neolithic / spacer | industrial / medieval / neolítico / espacial | oficial — `Core/Keyed/Enums.xml` `TechLevel_*`; `Core/DefInjected/BackstoryDef/Solid_Child.xml` `MidworldCadet83.description` ("classe espacial"). |
| glitterworld / glitter-tech | mundo brilhante / tecnobrilho ⚠️ | oficial para glitterworld — `Core/DefInjected/BackstoryDef/Offworld_Glitterworld_Adult.xml` `Architect28.description`; "glitter-tech" é novo. Gate (2026-09-15): mantido `tecnobrilho` (aprovado AS-IS). |
| ultratech | ultratecnologia | oficial — `Royalty/DefInjected/FactionDef/Faction_Empire.xml` `Empire.description` ("sociedade ultratecnológica"). |
| geothermal | geotérmico | oficial — `Core/DefInjected/ThingDef/Buildings_Natural.xml` `SteamGeyser.description`. |
| hydroponics | hidroponia | oficial — `Core/DefInjected/ResearchProjectDef/ResearchProjects_2_Electricity.xml` `Hydroponics.label`. |
| solar | solar | oficial — `Core/DefInjected/ResearchProjectDef/ResearchProjects_2_Electricity.xml` `SolarPanels.label` ("painéis solares"). |
| photovoltaic | fotovoltaico | novo — WD2 "photovoltaic arrays". |
| pollution | poluição | oficial — `Biotech/DefInjected/ConceptDef/Tutor.xml` `PollutedTerrain.helpText`. |
| decontamination | descontaminação | novo — WD2 `TSA_WD_Traveler_Outpost_Decontamination`. |
| quantum | quântico | novo — WD2/USE; sem precedente. |

## Comida, animais e produção

| EN | PT-BR | Obs |
|---|---|---|
| chemfuel | combustível químico | oficial — `Core/DefInjected/ThingDef/Buildings_Special.xml` `InfiniteChemreactor.description`. |
| neutroamine | neutroamina | oficial — `Core/DefInjected/ThingDef/Items_Resource_Manufactured.xml` `Neutroamine.label`. |
| plasteel | plastiaço | oficial — `Core/DefInjected/ThingDef/Items_Resource_Stuff.xml` `Plasteel.label`. |
| synthread | fibra sintética | oficial — `Core/DefInjected/ThingDef/Items_Resource_Stuff.xml` `Synthread.label`. |
| hyperweave | hiper tecido | oficial — `Core/DefInjected/ThingDef/Items_Resource_Stuff.xml` `Hyperweave.label` (grafia oficial com espaço). |
| hay bale | fardo de feno | novo — WD2 `TSA_WD_Hayball_2a.label` (esqueleto B1). |
| livestock / herd | criação / rebanho | herd "rebanho" oficial — `Anomaly/DefInjected/PsychicRitualDef/PsychicRituals.xml` `SummonAnimals.description`; "livestock" → "criação" novo (WD2). |
| pasture | pasto | novo — WD2 (upgrade de pasto). |
| tame / train / slaughter / butcher / hunt | domar / treinar / abater / esquartejar / caçar | oficial — termo herdado (ver `docs/medieval/GLOSSARY.md`). |
| mining wagon | carroça de mineração | repo — "carroça" em `DefInjected/ThingDef/AdaptiveStorage_ThingDef.xml` `DankPyon_CartEmptyA.label`; WD2 `TSA_WD_Wagon_*`. |
| crate | caixote | oficial — `Core/DefInjected/ThingDef/Buildings_Ancient_Active.xml` `AncientHermeticCrate.description`; WD2 "wooden crate". |
| irrigation | irrigação | novo — WD2 `TSA_WD_Upgrade_IrrigationCanals`. |
| fishing / pier / trawler | pesca / píer / arrastão | novo — WD2 `Upgrade_FishingNets`, `Upgrade_CoastalPier`, `Upgrade_TrawlerGear`. |
| sunsteel / sunweave / solarite / quasar alloy | aço-solar / tecido-solar / solarita / liga de quasar | novo — WD2 (`BOR_TSA_WD_Upgrade_SunsteelWall`, `SunweaveTraps`, "Solarite starships", `QuasarAlloyWall`). |
| kwazaari | kwazaari (manter) | novo — WD2 (`Kwazaari Hospital`, `Kwazaari Mining Lift`); nome próprio, não traduzir. |

## Medieval herdado (referência)

Termos fechados em `docs/medieval/GLOSSARY.md`; usar verbatim. Os que reaparecem
nos lotes B12 (VFE Medieval 2), B13 (House Doyle, Faction Elves) e utilitários:

| EN | PT-BR | Obs |
|---|---|---|
| castle / knight | castelo / cavaleiro | repo — `DefInjected/ThingDef/VFE_Medieval2_ThingDef.xml` (castelo); `VFE_Medieval2_BackstoryDef.xml` `VFEM_Knight51`. |
| plate armor / chainmail | armadura de placas / cota de malha | repo — `VFEM2_ThingDef.xml` ("armadura de placas pesada"); `VAE_Apparel_Chainmail` (VARME). |
| helm / shield | elmo / escudo | repo — `DefInjected/ThingDef/VFE_Medieval2_ThingDef.xml` `VFEM2_Apparel_HeavyLeatherHelmet.label` ("elmo de couro pesado"); "escudo" herdado do medieval (ver `docs/medieval/GLOSSARY.md`). |
| tavern / guild / heraldry | taverna / guilda / heráldica | repo — `VFE_Medieval2_BackstoryDef.xml` `VFEM_Guildmaster59` (guilda); `VFEM2_ThingDef.xml` ("estandarte heráldico"). |
| fey | fada | novo — herdado do medieval (`HouseVanIlla_XenotypeDef.xml` "Fadas Illan"). |

## Utilitários, logística e QoL

| EN | PT-BR | Obs |
|---|---|---|
| warehouse | armazém | oficial — `Core/DefInjected/BackstoryDef/Solid_Child.xml` `AbandonedChild30.description`; WD2 `TSA_WD_Outpost_Warehouse`. |
| forklift | empilhadeira | oficial — `Odyssey/DefInjected/QuestScriptDef/Script_AncientStructures.xml` `Opportunity_AncientStructureWarehouse.questSubjectRules.rulesStrings` ("esboço de uma empilhadeira"). |
| logistics | logística | repo — `DefInjected/BackstoryDef/VQE_Deadlife_BackstoryDef.xml` `VQE_EternalLogisticsOfficer38.description`. |
| delivery spot | ponto de entrega | novo — WD2 `TSA_WD_OutpostDeliverySpot`. |
| remote power | energia remota | novo — WD2 `TSA_WD_RemotePowerTabSource`. |
| mining lift | elevador de mineração | novo — WD2 `Upgrade_MiningLift` + variantes. |
| ruins | ruínas | oficial — `Anomaly/DefInjected/CreepJoinerBaseDef/Downsides.xml` `CrumblingMind.label`; WD2 "settlement ruins". |

## Registro de cunhagens por mod (WD2/DMS)

Termos novos cunhados nos maiores alvos; nenhum substitui termo herdado.

| EN | PT-BR | Obs |
|---|---|---|
| outpost upgrade | melhoria de posto avançado | novo — WD2 `OutpostUpgradeDef`; "upgrade" segue o gate de "melhoria". |
| deepchem | química profunda | novo — WD2 `TSA_WD_Outpost_DeepchemDrill`; não confundir com "deep drill" oficial ("perfurar"). |
| raw shaping | modelagem de recursos brutos | novo — WD2 `TSA_WD_Outpost_RawShaping`. |
| academy / acolyte | academia / acólito | "acólito" oficial — `Core/DefInjected/BackstoryDef/Solid_Adult.xml` `AcolyteOfStars6`; "academia" novo (WD2 `TSA_WD_Outpost_Academy`). |
| cowanoid / chickenoid | cowanoide / galinhenoide | novo — DMS; trocadilhos com "mecanoide", preservar o radical "-noide". |

## Registro de cunhagens — B9 (VPE e bibliotecas)

| EN | PT-BR | Obs |
|---|---|---|
| psycaster (pessoa) | psinjurador | herdado do oficial (VME `PreceptDef` "psinjurador", VRE Archon) — unificado no B9 em 69b173a; "psicocaster" era divergente. |
| psycast (habilidade) | psicocast | convenção do repo B9; "psi-talento" oficial não adotado para não reterraduzir 56 ocorrências. |
| psyessence | psiessência | novo — VPE. |
| skipgate / skipdoor / skipbarrier / skipshield | portal de salto / porta de salto / barreira de salto / escudo de salto | novo — VPE B9; radical "salto" do `VPE_Skipdoor` ("porta de salto") já existente. |
| archotechist | arqueotecista | novo — VPE; stem segue "arqueotecnológicos" (Core archist). |
| skipmaster / staticlord | mestre do salto / senhor da estática | novo — VPE rótulos de caminho. |
| psyring | anel psíquico | novo — VPE `VPE_Psyring` + receita; antes ficava "psiring" em EN. |
| path | caminho | VPE rótulos de caminho ("O caminho do X"). |
| pawn | colono | unificação repo (a112677): "peões" removidos de VQE, VVE, RimCuisine/Cooking, VFE Architect, Classical e Alpha Animals; `wildpawn` mantém EN como nome de criatura. Citação de nome de configuração do VehicleFramework segue o rótulo real "Trabalhos de Multi-Colonos". |
