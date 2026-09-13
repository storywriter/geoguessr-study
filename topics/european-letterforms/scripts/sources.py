"""Source register. Statistics are observations; geometry and cues are editorial."""
ACCESSED='2026-09-13'
# id | publisher | date | title / locator | URL
TEXT='''
UN|United Nations Statistics Division|2026|M49: Europe and Western Asia; geographic grouping, not sovereignty|https://unstats.un.org/unsd/methodology/m49/
NE|Natural Earth|5.1.2|Admin 0 / Admin 1, public domain; pinned inputs in repository data/input_manifest.json|https://www.naturalearthdata.com/about/terms-of-use/
CLDR|Unicode Consortium|2026|CLDR 48.2, exemplar characters and list conjunctions; per-language XML URLs and hashes in data/|https://cldr.unicode.org/index/downloads
CLDR-T|Unicode Consortium|2026|Territory language information; language association only, not dated population statistics|https://www.unicode.org/cldr/charts/48/supplemental/territory_language_information.html
EU|European Union|2026|EU languages; 24 official languages|https://european-union.europa.eu/principles-countries-history/languages_en
CHARTER|Council of Europe|2022|Table of protected languages; protection alone does not establish sign frequency|https://rm.coe.int/november-2022-revised-table-languages-covered-english-/1680a8fef4
UNGEGN|UNGEGN / national naming authorities|2025|National Toponymic Guidelines index; orthography and naming policies|https://unstats.un.org/unsd/ungegn/nna/toponymic/
PCGN|UK Permanent Committee on Geographical Names|2026|Country factfiles index; official languages, writing systems, place names|https://www.gov.uk/government/publications/toponymic-factfiles
UK|PCGN / Ordnance Survey|2026|UK Toponymic Guidelines, Languages; Gaelic and Scots status updated 2025|https://www.gov.uk/government/publications/toponymic-guidelines/toponymic-guidelines-for-map-and-other-editors-united-kingdom-of-great-britain-and-northern-ireland--2
WELSH|Welsh Language Commissioner|2021|Census 2021, age 3+ able to speak Welsh, local authorities|https://www.welshlanguagecommissioner.wales/policy-and-research/the-position-of-the-welsh-language/2021-census
GAELIC-SIGN|Transport Scotland|2020|Guidance on bilingual Gaelic/English traffic signs, trunk routes and local authority distinction|https://www.transport.gov.scot/media/48722/guidance-on-the-use-of-bilingual-gaelic-english-traffic-signs-in-scotland.pdf
GAELIC-STAT|Scottish Government|2022/2026|National Islands Plan, Gaelic skills from 2022 census; any skills, not speaking only|https://www.gov.scot/publications/national-islands-plan-2/pages/10/
CORNISH|Cornwall Council|2026|Street nameplates: English above Cornish on new plates|https://www.cornwall.gov.uk/planning-and-building-control/property-and-street-naming-and-numbering/street-nameplates/
IRISH-SIGN|Transport Infrastructure Ireland|2022|Third Irish language scheme, signage obligations|https://www.tii.ie/media/3pumnn4c/tii-scheme-3-english.pdf
GAELTACHT|Government of Ireland|2026|An Ghaeltacht; official regions, boundaries are more fragmented than atlas locators|https://www.gov.ie/en/department-of-rural-and-community-development-and-the-gaeltacht/policies/an-ghaeltacht/
JERSEY|Parish of St Helier|2020|Roads Committee minutes: English, French and Jerriais street-name plates|https://sthelier.je/wp-content/uploads/sites/14/2023/02/120220-A-Agenda-Minutes.pdf
GUERNSEY|Visit Guernsey / States of Guernsey|2022|Which languages are spoken in Guernsey? Historic names and present English|https://www.visitguernsey.com/articles/2020/which-languages-are-spoken-in-guernsey
MANX|Douglas City Council|2023|Council minutes 13 December pp.174-175: existing and replacement Manx/English street nameplates|https://www.douglas.gov.im/~documents/democratic-services/council-meetings-agendas-minutes/public-agenda-13-12-23/?layout=file
FAROE|Visit Faroe Islands|2016|National handbook, Language: Faroese; Danish in Danish institutions|https://vs.cdn.fo/media/1861/national-handbook-online-version.pdf
FIN|National Land Survey of Finland / UNGEGN|2025|Toponymic guidelines pp.4-13: 2024 language populations, Swedish and Sami areas, signs|https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/Toponymic_guidelines_2025.pdf
NOR|Norwegian Mapping Authority / UNGEGN|2025|Toponymic guidelines: Bokmal/Nynorsk, Sami and Kven names and alphabets|https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_12_CRP12_item7d.pdf
SWE|PCGN|2026|Sweden pp.1-3: Sami and Meankieli official names and signs|https://assets.publishing.service.gov.uk/media/69b175fc1daa1b70ca2331ae/Sweden_Toponymic_Factfile.pdf
EST|Estonian Place Names Board / UNGEGN|2025|Toponymic guidelines, official names and Estonian alphabet|https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_110_CRP110_item7d.pdf
BEL|Belgian naming authorities / UNGEGN|2009|Toponymic guidelines pp.3-5: four language areas|https://unstats.un.org/unsd/geoinfo/UNGEGN/docs/25th-gegn-docs/wp%20papers/wp93-tgl%20belgium-april%202009.pdf
NLD|Kadaster / UNGEGN|2017|Toponymic guidelines pp.6-7: Frisian alphabet and place names on signposts|https://unstats.un.org/unsd/geoinfo/UNGEGN/docs/11th-uncsgn-docs/E_Conf.105_142_CRP.142_9_toponymic%20guidelines%20Netherlands%202017_a.pdf
DEU-MIN|Council of Europe|2022|Fifth opinion Germany, topographical indications; Sorbian, Frisian, Danish, Low German|https://rm.coe.int/5th-op-germany-en/1680a6e008
FRA-MIN|French Ministry of Culture|2026|Regional languages inventory; not a measurement of street use|https://www.culture.gouv.fr/thematiques/langue-francaise-et-langues-de-france/agir-pour-les-langues/promouvoir-les-langues-de-france/langues-regionales
BRETON|Region Bretagne|2022|Convention 2022-2027, bilingual public buildings and national roads|https://www.bretagne.bzh/presse/communiques-dossiers/convention-specifique-en-faveur-des-langues-de-bretagne-2022-2027-objectif-accroitre-le-nombre-de-jeunes-locuteurs/
OCCITAN|Region Occitanie|2023|Parlem una cultura viva: existing bilingual station signs, wider public signage policy|https://www.laregion.fr/Pour-des-langues-et-cultures-regionales-bien-vivantes
BASQUE-FR|Communaute Pays Basque|2025|Municipal Basque: street-name and directional-sign translation programme|https://www.communaute-paysbasque.fr/langues-basque-et-occitan-gascon/je-developpe-leuskara-sur-ma-commune
CHE|PCGN|2023|Switzerland: four national languages and cantonal official-language areas|https://assets.publishing.service.gov.uk/media/6512a2d43d3718000d6d0b62/Switzerland_factfile.pdf
CHE-STAT|Swiss Federal Statistical Office|2020|Main languages, 2020; multiple responses, not signage share|https://www.swissstats.bfs.admin.ch/data/webviewer/appId/ch.admin.bfs.swissstat/article/issue220122032200-05/package
LUX-STAT|STATEC|2021|Recensement 2021: diversite linguistique, principal language|https://statistiques.public.lu/fr/publications/recensement/diversite-linguistique.html
ITA|Istituto Geografico Militare|2012|Toponymic Guidelines Italy, minority languages, regional maps and glossaries|https://igmi.org/%2B%2Btheme%2B%2Bigm/toponomastica/3_Toponymic%20Guidelines%20Italy.pdf
ITA-PCGN|PCGN|2026|Italy: official Italian and minority naming|https://assets.publishing.service.gov.uk/media/6a5a125f5ca06bf11ccb43c9/Italy_Toponymic_Factfile.pdf
TYROL-STAT|ASTAT, Autonomous Province Bolzano|2024|Language-group declaration 2024: valid declarations of resident Italian citizens, not all residents|https://astat.provincia.bz.it/de/publikationen/ergebnisse-sprachgruppenzahlung-2024
ESP|PCGN|2025|Spain pp.2-4: Catalan, Basque, Galician, Aranese, Asturian and Aragonese naming|https://assets.publishing.service.gov.uk/media/6941528d29501ea90654a507/Spain_Toponymic_Factfile.pdf
CAT-STAT|Idescat|2023|Knowledge of Catalan, age 15+: speaking 80.4%; not habitual-use share|https://www.idescat.cat/indicadors/?id=aec&lang=en&n=15985&t=201200
BASQUE-STAT|Basque Government|2021|Seventh sociolinguistic survey, age 16+, three territories|https://www.euskadi.eus/significant-data/web01-a3eas/en/
PRT|PCGN|2026|Portugal: Portuguese, Mirandese and regional place names|https://assets.publishing.service.gov.uk/media/6a6b12600c36759b5ccaa1f9/Portugal_Toponymic_Factfile.pdf
MICRO|PCGN|2026|Andorra, Liechtenstein, Monaco, San Marino, Vatican City; bilingual Monegasque street signs|https://assets.publishing.service.gov.uk/media/6968cbde6958e5645144b08d/European_Microstates_Toponymic_Factfile.pdf
POL-MIN|Polish Government|2019|Minority topographical names and bilingual road signs; German, Kashubian, Lemko examples|https://www.gov.pl/attachment/fb56781a-91ec-4e52-8395-1d46bb7848ca
POL-MIN2|Polish Government|2024|National-minority names including Belarusian and Lithuanian|https://www.gov.pl/attachment/20e7d747-e23c-4a23-abf7-0edcde6c6b31
CZE|Czech Office for Surveying, Mapping and Cadastre / UNGEGN|2025|Toponymic guidelines, Czech and Polish minority names|https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_152_CRP152_Item7d.pdf
SVK|PCGN|2022|Slovakia, minority languages and orthography|https://assets.publishing.service.gov.uk/media/6246f4fa8fa8f5277c0169ba/Slovakia_Toponymic_Factfile.pdf
SVN|PCGN|2023|Slovenia, Italian in southwest and Hungarian in northeast|https://assets.publishing.service.gov.uk/media/650bf4d7fbd7bc000de546ff/Slovenia_Toponymic_Factfile.pdf
BIH|PCGN|2023|Bosnia and Herzegovina: Bosnian, Croatian, Serbian and both scripts|https://assets.publishing.service.gov.uk/media/6512a00cb23dad0012e70609/Bosnia_and_Herzegovina_Toponymic_factfile.pdf
SRB|PCGN|2022|Serbia pp.1-3: Serbian and Vojvodina's five additional official languages|https://assets.publishing.service.gov.uk/media/650962d322a783001343e841/Serbia_Toponymic_Factfile.pdf
SRB-STAT|Statistical Office of Serbia|2022|Census: mother tongue, excludes Kosovo; results released June 2023|https://www.stat.gov.rs/en-US/vesti/20230616-st/?a=0&s=09
MNE|PCGN|2025|Montenegro: nationally official language and four languages in official use; Ulcinj names|https://assets.publishing.service.gov.uk/media/69285cf3b3b9afff34e9615a/Montenegro_Toponymic_factfile.pdf
MNE-STAT|MONSTAT|2023|Census mother tongue, national results|https://www.monstat.org/eng/novosti.php?id=4012
XKX|PCGN|2025|Kosovo: Albanian, Serbian and municipal Turkish/Bosnian/Romani use|https://assets.publishing.service.gov.uk/media/6941525329501ea90654a505/Kosovo_Toponymic_Factfile.pdf
MKD|PCGN|2026|North Macedonia: Macedonian, Albanian and municipal languages|https://assets.publishing.service.gov.uk/media/69b175ba24c6431b84f0e475/North_Macedonia_Toponymic_Factfile.pdf
MKD-STAT|State Statistical Office, North Macedonia|2021|Census resident population by mother tongue|https://www.stat.gov.mk/PrikaziSoopstenie_en.aspx?rbrtxt=146
ROU|PCGN|2025|Romania p.6: minority toponyms including road signs; 20% threshold|https://assets.publishing.service.gov.uk/media/694548d92f0261139350894f/Romania_Toponymic_Factfile.pdf
MDA|PCGN|2024|Moldova: Romanian; Gagauzia; separate de facto Transnistrian language situation|https://assets.publishing.service.gov.uk/media/6634e8f21834d96a0aa6d0ed/Moldova_Toponymic_Factfile.pdf
MDA-STAT|National Bureau of Statistics Moldova|2024|Final census mother tongue, territorial control exclusions; Moldovan/Romanian self-labels|https://statistica.gov.md/index.php/ro/rezultatele-finale-ale-recensamantului-populatiei-si-locuintelor-2024-caracteris-10121_62043.html
MDA-REG|National Bureau of Statistics Moldova|2024|Preliminary census regional mother tongues; explicitly preliminary|https://statistica.gov.md/en/preliminary-results-of-the-2024-population-and-housing-census-10077_61626.html
UKR|Ukraine / UNGEGN|2011|Toponymic guidelines; pre-war distribution and orthography, not current street inventory|https://unstats.un.org/unsd/geoinfo/UNGEGN/docs/Toponymic%20guidelines%20PDF/Ukraine/Verstka.pdf
GEO|PCGN|2025|Georgia: Georgian, Abkhaz and Ossetian scripts; de facto areas described separately|https://assets.publishing.service.gov.uk/media/690dd89dacbadb0fa8050f77/Georgia_Toponymic_factfile.pdf
GEO-LAW|Legislative Herald of Georgia|2015|Organic Law on Official Language: Georgian and Abkhaz in Abkhazia|https://www.matsne.gov.ge/en/document/view/2931198?fullscreen=1&impose=parallelEn
AZE|President of Azerbaijan|2026|Constitution, Article 21: Azerbaijani state language|https://president.az/en/pages/view/azerbaijan/constitution
CYP|Cyprus Office of Law Commissioner|2025|Consolidated constitution, Article 3: Greek and Turkish|https://www.olc.gov.cy/olc/olc.nsf/5CA0138A654BE102C2258D48002E723E/%24file/Constitution%2014.11.2025.pdf
CYP-PIO|Cyprus Press and Information Office|2018|Cyprus at a Glance, Languages|https://publications.gov.cy/assets/user/publications/GAAG/CAAG_EN_2018/files/assets/common/downloads/Cyprus%20at%20a%20Glance_AR.pdf
RUS|PCGN|2025|Russia pp.2-3: republic official languages; minority toponyms often limited|https://assets.publishing.service.gov.uk/media/68419a05578282a4b102c093/Russia_Toponymic_Factfile.pdf
RUS-SIGNS|Council of Europe|2018|Fourth opinion, paragraphs 109-111: Tatar, Chuvash, Udmurt, Kalmyk signage observations|https://rm.coe.int/4th-advisory-committee-opinion-on-the-russian-federation-english-langu/1680908982
OMNI|Omniglot, Simon Ager|2026|Alphabet reference index; secondary cross-check for scripts absent from CLDR, not population data|https://www.omniglot.com/writing/cyrillic.htm
CORSICA|Collectivite de Corse|2017|Lingua Corsa grants: bilingual street and public-building signs|https://www.isula.corsica/linguacorsa/attachment/2058571/
ALSACE|Eurometropole de Strasbourg|2019|Magazine April 2019 p.14: existing French/Alsatian street plates in Plobsheim|https://www.strasbourg.eu/documents/976405/4643989/201904-euromet-mag-22.pdf/533dbc8a-2da1-3677-ef26-e8d0c6b30315?t=1554210698816&version=1.0
HUN-SIGNS|Hungary / Council of Europe|2012|State report, geographical names and public-institution signs by locality|https://rm.coe.int/16806c8e14
HRV-SIGNS|Croatia / Council of Europe|2025|Implementation report: Czech and other minority signs, municipal statutes|https://rm.coe.int/croatia-ria7-en/4880282b76
HRV-OP|Council of Europe|2021|Fifth opinion Croatia, pp.27-28: actual implementation and exceptions|https://rm.coe.int/5th-op-croatia-en/1680a2cb49
ALB-SIGNS|Council of Europe|2023|Fifth opinion Albania, paragraph 119: Greek and Macedonian signs in three municipalities|https://rm.coe.int/5th-op-albania-en/1680acf90e
SAMI-NAMES|Lantmateriet|2026|Minority-language place names; North, Lule, Ume and South Sami|https://www.lantmateriet.se/sv/kartor/Ortnamn/ortnamn-pa-minoritetssprak/
AUT-UN|Austrian naming authority / UNGEGN|2012|National report: 164 Slovene, 47 Croatian and 4 Hungarian co-official settlement names|https://unstats.un.org/unsd/geoinfo/ungegn/docs/10th-uncsgn-docs/econf/E_CONF.101_60_Report%20of%20Austria.pdf
SVALBARD|Visit Svalbard / Svalbard Museum|年記載なし（2026確認）|The History of Svalbard: Barentsburg streets and mining-community heritage|https://en.visitsvalbard.com/dbimgs/THEHISTORYOFSVALBARD.pdf
'''
SOURCES={}
for line in TEXT.strip().splitlines():
    sid,publisher,date,title,url=line.split('|')
    SOURCES[sid]=dict(id=sid,publisher=publisher,date=date,title=title,url=url,accessed=ACCESSED)

# Deliberately separate denominator types. Missing statistics remain missing.
STATISTICS=[]
def stat(sid,iso,area,lang,year,indicator,value,denominator,source,note=''):
    STATISTICS.append(dict(id=sid,iso3=iso,area_ja=area,language_id=lang,year=year,indicator_ja=indicator,value_percent=value,denominator_ja=denominator,source_id=source,note_ja=note))
for area,value,key in [('ウェールズ全体',17.8,'all'),('北西部グウィネズ',64.4,'gwynedd'),('北西沖アングルシー島',55.8,'anglesey'),('中西部ケレディジョン',45.3,'ceredigion')]:
    stat('welsh-'+key,'GBR',area,'cy',2021,'話せる',value,'3歳以上の通常居住者','WELSH')
stat('gaelic-islands','GBR','北西沖のアウター・ヘブリディーズ','gd',2022,'何らかの言語技能',57,'島の住民（国勢調査の言語項目対象）','GAELIC-STAT','話せる割合とは異なる。公表値は整数丸め。')
for lang,val in [('fi',84.1),('sv',5.1),('se',.04)]:
    stat('fin-'+lang,'FIN','全国',lang,2024,'登録母語',val,'総人口5,635,971人','FIN','se行の0.04%はサーミ諸語の合計。個別言語の割合ではない。' if lang=='se' else '')
for lang,val in [('de_CH',62),('fr',23),('it',8),('rm',.5)]:
    stat('che-'+lang,'CHE','全国',lang,2020,'主要言語',val,'永住人口の全年齢（家族についての補足回答を含む・最大3言語）','CHE-STAT','ドイツ語にはスイスドイツ語、イタリア語には方言も含む。調査範囲・丸めが異なるため他国と単純比較しない。')
stat('che-romansh-area','CHE','南東部ロマンシュ語地域','rm',2020,'主要言語',65,'ロマンシュ語地域の永住人口・全年齢（複数回答）','CHE-STAT')
stat('lux-main','LUX','全国','lb',2021,'主要言語',48.9,'2021国勢調査の主要言語回答者','LUX-STAT')
for lang,val in [('de',68.61),('it',26.98),('lld',4.41)]:
    stat('tyrol-'+lang,'ITA','北端・ボルツァーノ周辺','%s'%lang,2024,'言語集団への所属宣言',val,'対象イタリア国民の有効宣言450,373件','TYROL-STAT','2023-09-30時点の居住等を要件とする2024調査。外国籍住民を含む全人口の母語割合ではない。')
stat('catalan-speak','ESP','北東部カタルーニャ','ca',2023,'話せる',80.4,'15歳以上','CAT-STAT')
for iso,area,val,key in [('ESP','北部バスク自治州',36.2,'bac'),('ESP','北部ナバラ',14.1,'nav'),('FRA','南西端フランス領バスク',20.1,'fr')]:
    stat('basque-'+key,iso,area,'eu',2021,'話せる',val,'16歳以上','BASQUE-STAT')
for lang,val in [('sr',84.4),('hu',2.6),('bs',2.2),('rom',1.2),('sq',1.0)]:
    stat('srb-'+lang,'SRB','全国（コソボを除く）',lang,2022,'母語',val,'国勢調査人口','SRB-STAT')
for lang,val in [('sr',43.18),('cnr',34.52),('bs',6.97),('sq',5.25),('ru',2.36)]:
    stat('mne-'+lang,'MNE','全国',lang,2023,'母語',val,'国勢調査人口','MNE-STAT')
for lang,val in [('mk',61.38),('sq',24.34),('tr',3.41),('rom',1.73),('sr',.61),('bs',.85)]:
    stat('mkd-'+lang,'MKD','全国',lang,2021,'母語',val,'総居住人口（行政資料による不詳者を含む）','MKD-STAT')
for lang,val in [('ru',11.6),('gag',3.6),('uk',3),('bg',1.2)]:
    stat('mda-'+lang,'MDA','国勢調査対象地域',lang,2024,'母語',val,'国勢調査回答人口','MDA-STAT','沿ドニエストルなど調査非実施地域は対象外。')
stat('mda-gag-reg','MDA','南部ガガウズ自治地域','gag',2024,'母語（暫定集計）',77.7,'自治地域の国勢調査回答人口','MDA-REG','全国最終値と地域暫定値を混同しない。')
