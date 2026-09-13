"""Country and regional locators. Extents locate a search area, not a language frontier."""
from languages import LANGUAGES

# ISO | Japanese country/area name | page group | principal public languages | source
COUNTRY_TEXT='''
GBR|イギリス|英国・アイルランド|en|UK
IRL|アイルランド|英国・アイルランド|en ga|IRISH-SIGN
IMN|マン島|英国・アイルランド|en gv|MANX
JEY|ジャージー|海峡諸島|en fr nrf_JE|JERSEY
GGY|ガーンジー|海峡諸島|en fr nrf_GG|GUERNSEY
ISL|アイスランド|北大西洋|is|CLDR-T
FRO|フェロー諸島|北大西洋|fo da|FAROE
DNK|デンマーク|北欧南部|da|CLDR-T
NOR|ノルウェー|北欧南部|nb nn|NOR
SJM|スヴァールバル諸島・ヤンマイエン島|北大西洋|nb|NOR
SWE|スウェーデン|北欧南部|sv|SWE
FIN|フィンランド|フィンランド|fi sv|FIN
ALA|オーランド諸島|フィンランド|sv|FIN
EST|エストニア|バルト海東岸|et|EST
LVA|ラトビア|バルト海東岸|lv|CLDR-T
LTU|リトアニア|バルト海東岸|lt|CLDR-T
BEL|ベルギー|ベネルクス|nl fr de|BEL
NLD|オランダ|ベネルクス|nl|NLD
LUX|ルクセンブルク|ベネルクス|lb fr de|LUX-STAT
FRA|フランス|フランス|fr|FRA-MIN
DEU|ドイツ|ドイツ|de|CLDR-T
AUT|オーストリア|アルプス|de|AUT-UN
CHE|スイス|スイス|de_CH fr it rm|CHE
LIE|リヒテンシュタイン|スイス|de_CH|MICRO
ESP|スペイン|イベリア半島|es|ESP
PRT|ポルトガル|イベリア半島|pt|PRT
AND|アンドラ|イベリア半島|ca|MICRO
GIB|ジブラルタル|イベリア半島|en|CLDR-T
ITA|イタリア|イタリア|it|ITA-PCGN
SMR|サンマリノ|イタリア|it|MICRO
VAT|バチカン|イタリア|it la|MICRO
MCO|モナコ|イタリア|fr mco|MICRO
POL|ポーランド|ポーランド|pl|CLDR-T
CZE|チェコ|中央ヨーロッパ|cs|CZE
SVK|スロバキア|中央ヨーロッパ|sk|SVK
HUN|ハンガリー|中央ヨーロッパ|hu|CLDR-T
SVN|スロベニア|西バルカン|sl|SVN
HRV|クロアチア|西バルカン|hr|CHARTER
BIH|ボスニア・ヘルツェゴビナ|西バルカン|bs hr sr|BIH
SRB|セルビア|セルビア・コソボ|sr sr_Latn|SRB
XKX|コソボ|セルビア・コソボ|sq sr|XKX
MNE|モンテネグロ|バルカン南部|cnr cnr_Cyrl sr bs hr sq|MNE
ALB|アルバニア|バルカン南部|sq|CLDR-T
MKD|北マケドニア|バルカン南部|mk sq|MKD
GRC|ギリシャ|ギリシャ・キプロス|el|CLDR-T
MLT|マルタ|ギリシャ・キプロス|mt en|EU
CYP|キプロス|ギリシャ・キプロス|el tr|CYP
BGR|ブルガリア|黒海周辺|bg|CLDR-T
ROU|ルーマニア|黒海周辺|ro|ROU
MDA|モルドバ|黒海周辺|ro|MDA
UKR|ウクライナ|ウクライナ・ベラルーシ|uk|UKR
BLR|ベラルーシ|ウクライナ・ベラルーシ|be ru|CLDR-T
RUS|ロシア|ロシア全域|ru|RUS
ARM|アルメニア|南コーカサス|hy|CLDR-T
AZE|アゼルバイジャン|南コーカサス|az|AZE
GEO|ジョージア|南コーカサス|ka|GEO
'''
COUNTRIES={}
REGIONS=[]
for line in COUNTRY_TEXT.strip().splitlines():
    iso,name,group,langs,source=line.split('|')
    COUNTRIES[iso]=dict(iso3=iso,name_ja=name,group=group,languages=langs.split(),source=source)

def add(iso,key,area,langs,group=None,kind='regional',geometry=None,sources=None,note='',status=None,stats=None):
    c=COUNTRIES[iso]
    REGIONS.append(dict(id=iso.lower()+'-'+key,iso3=iso,country_ja=c['name_ja'],area_ja=area,
        languages=langs.split(),group=group or c['group'],kind=kind,
        geometry_spec=geometry or {'type':'country'},sources=(sources or c['source']).split(),note_ja=note,
        status_ja=status or ('全国の公用語・主要公共表示' if kind=='national' else '地域言語の地名・公共表示'),statistics=(stats or '').split()))
def admin(*names):return {'type':'admin1','names':list(names)}
def bounds(w,s,e,n):return {'type':'bbox','bounds':[w,s,e,n]}
def point(x,y):return {'type':'point','coordinates':[x,y]}

# Belgium and Switzerland are split below, so there is no misleading nationwide
# fill for every language. Other nationwide entries describe the legal/basic layer.
for iso,c in COUNTRIES.items():
    if iso in {'BEL','CHE','CYP'}:continue
    notes={
      'GBR':'英語は全国の事実上の共通語。英国全体を対象とする単一の法定公用語指定とは区別。',
      'IRL':'アイルランド語が第一公用語、英語が第二公用語。道路標識では全国的に両語を確認できる。',
      'FIN':'国の公用語は2言語。スウェーデン語の地域的集中は沿岸の拡大図を参照。',
      'FRO':'日常の主表示はフェロー語。デンマーク語はデンマーク管轄機関などで使用。',
      'JEY':'英語の案内と、フランス語・ジャージー語由来の地名。すべての標識が3言語ではない。',
      'GGY':'主表示は英語。フランス語・ガーンジー語の歴史的地名が残る。',
      'IMN':'英語にマン島語の地名・公共表示を併記する例。',
      'VAT':'日常・行政の主言語はイタリア語。ラテン語は教皇庁の公式用途や銘文を含めた補助。',
      'MCO':'フランス語が公用語。モネガスク語は旧市街などの一部街路名併記。',
      'MNE':'モンテネグロ語が国の公用語。残る4言語は憲法上「公的使用」。使用地域・名称は重なる。',
      'BIH':'3言語の綴りは非常に近く、ラテン文字とキリル文字が併存する。',
      'XKX':'国際的地位には立場の違いがあるため学習上の地域として別掲。セルビア語の実表示は自治体差。',
      'UKR':'戦争・占領・改称・撮影年により表示が変化。旧画像のロシア語だけで現在の国を判定しない。',
      'RUS':'ロシア語は全域。アジア側と地域公用語も後半の拡大図に収録。',
      'NOR':'2つのノルウェー語書記標準。地名のveg/veiだけでは境界を断定できない。',
    }.get(iso,'観光地の英語訳・ラテン文字への転写は他国でも現れる。固有の文字と短い語を組み合わせる。')
    add(iso,'base','全域（基本の表示）', ' '.join(c['languages']),kind='national',note=notes)

# British Isles
add('GBR','wales','南西部（ウェールズ）','cy',geometry=admin('Flintshire','Wrexham','Powys','Monmouthshire','Newport','Cardiff','Vale of Glamorgan','Bridgend','Neath Port Talbot','Swansea','Carmarthenshire','Pembrokeshire','Ceredigion','Gwynedd','Conwy','Denbighshire','Anglesey','Caerphilly','Rhondda, Cynon, Taff','Blaenau Gwent','Torfaen','Merthyr Tydfil'),sources='UK WELSH',note='英語との併記。ウェールズの行政区をまとめた範囲。',stats='welsh-all welsh-gwynedd welsh-anglesey welsh-ceredigion')
add('GBR','gaelic','北西部・北西沖の島々','gd',geometry=admin('Highland','Eilean Siar','Argyll and Bute'),sources='UK GAELIC-SIGN GAELIC-STAT',note='ゲール語併記の幹線・自治体表示。東・南側の一部幹線にも続く。',stats='gaelic-islands')
add('GBR','scots','北部（スコットランド）','sco',geometry=bounds(-8,54.65,-.7,61),sources='UK',status='地域の公用語／地名・文化表示',note='2025年法による公的地位。英語と同形の地名が多く、道路の主表示を一律にスコッツ語とはしない。')
add('GBR','cornwall','南西端（コーンウォール）','kw',geometry=admin('Cornwall'),sources='CORNISH UK',note='新しい街路名板などに併記。幹線道路がすべて併記とは限らない。')
add('GBR','northern-ireland','西の島の北東部（北アイルランド）','ga',geometry=bounds(-8.3,53.95,-5.3,55.5),sources='UK CHARTER',note='自治体・街路によってアイルランド語を併記。地域全域の一様な表示ではない。')
add('IRL','gaeltacht','西岸・北西岸（ゴールウェイなど）','ga',geometry=admin('Donegal','Mayo','Galway','Kerry'),sources='GAELTACHT IRISH-SIGN',note='ゲールタハトはこの中の飛び地状の地区。県全域が言語地域という意味ではない。',status='公用語が目立つ地区の位置')

# Nordic regional layers
add('DNK','german','南端・ドイツ国境近く','de',group='北欧南部',geometry=point(9.42,55.04),sources='CHARTER',status='少数言語の学校・文化施設表示',note='ドイツ系施設などの局所的手掛かり。国の道路標識の主言語ではない。')
add('NOR','nynorsk-west','西岸・南西部','nn',geometry=bounds(4.5,58,9,63),sources='NOR',note='ニーノシュク採用自治体が多い地域の概略。内部にはブークモール自治体もある。')
for key,area,lang,geo in [
 ('sami-north','北端・北東部（フィンマルク）','se',bounds(20,68.2,31.5,71.5)),
 ('sami-lule','北部（ボードーの北東）','smj',point(16.1,68.05)),
 ('sami-south','中部（トロンハイムの北東・山地）','sma',bounds(11,62,15.5,65.5)),
 ('kven','北東部（フィンランド国境近く）','fkv',bounds(23,69,30.5,71))]:
    add('NOR',key,area,lang,group='北欧の地域言語',geometry=geo,sources='NOR',note='法定の多言語地名・標識。塗色内の自治体や道路で表示の有無が異なる。')
for key,area,lang,geo in [
 ('sami-north','北端（キルナ周辺）','se',bounds(17,66.7,23,69.1)),
 ('sami-lule','北部（ヨックモック周辺）','smj',point(19.84,66.61)),
 ('sami-south','中北部の西側山地','sma',bounds(12,61.5,16,65.4)),
 ('meankieli','北東端・フィンランド国境近く','fit',bounds(22,65.6,24.3,68.3))]:
    add('SWE',key,area,lang,group='北欧の地域言語',geometry=geo,sources='SWE',note='伝統的な地名とスウェーデン語の併記が手掛かり。実際の表示地点は範囲内の一部。')
add('FIN','swedish-west','西岸（ヴァーサ周辺）','sv',geometry=admin('Ostrobothnia','Central Ostrobothnia'),sources='FIN',note='海岸寄りのスウェーデン語・二言語自治体。内陸全域の使用を意味しない。',stats='fin-sv')
add('FIN','swedish-south','南岸・南西の島々','sv',geometry=bounds(21,59.7,27,60.5),sources='FIN',note='ヘルシンキ周辺を含む沿岸の二言語表示。',stats='fin-sv')
for key,area,lang,geo in [('sami-north','北端（ウツヨキなど）','se',bounds(20.5,68.3,28.5,70.2)),('sami-inari','北部イナリ湖周辺','smn',point(27.02,68.91)),('sami-skolt','北東端（セヴェッティヤルヴィ周辺）','sms',point(28.60,69.51))]:
    add('FIN',key,area,lang,group='北欧の地域言語',geometry=geo,sources='FIN',note='サーミ語地域内でも言語ごとに使用地が異なる。',stats='fin-se')

# Benelux / France / Germany
add('BEL','north','北部（フランデレン）','nl',geometry=admin('West Flanders','East Flanders','Antwerp','Limburg','Flemish Brabant'),sources='BEL')
add('BEL','south','南部（ワロン）','fr',geometry=admin('Hainaut','Namur','Luxembourg','Liege','Walloon Brabant'),sources='BEL',note='東端のドイツ語地域と境界の便宜言語自治体は別に扱う。')
add('BEL','brussels','中央付近（ブリュッセル）','fr nl',geometry=point(4.35,50.85),sources='BEL',note='フランス語・オランダ語の二言語地域。')
add('BEL','german','東端・ドイツ国境（オイペンなど）','de',geometry=point(6.03,50.63),sources='BEL',note='ドイツ語地域は細い非連続の範囲。点はオイペン、南側のザンクト・フィートも候補。')
add('NLD','friesland','北部（フリースラント）','fy',geometry=admin('Friesland'),sources='NLD',note='フリジア語地名・街路名。自治体によりオランダ語と単独・併記が異なる。')
for key,area,lang,geo,src in [
 ('breton','北西の半島（ブルターニュ）','br',admin('Finistère','Morbihan',"Côtes-d'Armor",'Ille-et-Vilaine'),'BRETON'),
 ('basque','南西端・スペイン国境の大西洋側','eu',bounds(-1.85,43,-.8,43.65),'BASQUE-FR'),
 ('catalan','南端・スペイン国境の地中海側','ca',admin('Pyrénées-Orientales'),'OCCITAN'),
 ('occitan','南部内陸（トゥールーズ・モンペリエなど）','oc',bounds(-.2,42.8,4.8,45.1),'OCCITAN'),
 ('corsica','南東沖（コルシカ島）','co',admin('Haute-Corse','Corse-du-Sud'),'CORSICA FRA-MIN'),
 ('alsace','北東部・ドイツ国境（ストラスブール周辺）','gsw',admin('Bas-Rhin','Haute-Rhin'),'ALSACE FRA-MIN')]:
    add('FRA',key,area,lang,geometry=geo,sources=src,status='地域言語の地名・公共表示（自治体差）',note='フランス語が基本。塗色は併記を探す地域の概略で、全道路での使用を示さない。',stats='basque-fr' if lang=='eu' else None)
for key,area,lang,geo in [
 ('sorbian-upper','東部・チェコとポーランドに近い内陸','hsb',bounds(13.95,51.05,14.7,51.65)),
 ('sorbian-lower','東部（コトブス周辺）','dsb',bounds(13.8,51.5,14.65,52.05)),
 ('frisian-north','北西岸・デンマーク国境近く','frr',bounds(8.1,54.4,9.15,55.1)),
 ('danish','北端（フレンスブルク周辺）','da',point(9.43,54.78)),
 ('saterland','北西部（オルデンブルクの西）','stq',point(7.68,53.09)),
 ('low-german','北部平野（ニーダーザクセンなど）','nds',bounds(6.7,52.5,10.8,53.8))]:
    add('DEU',key,area,lang,geometry=geo,sources='DEU-MIN CHARTER',note='地名や自治体・文化表示の併記。ドイツ語が併用され、設置の程度には差がある。')

# Alps and Italy
add('CHE','german','北部・中部・東部','de_CH',geometry=admin('Zürich','Aargau','Bern','Lucerne','Uri','Schwyz','Glarus','Sankt Gallen','Thurgau','Solothurn','Basel-Stadt','Basel-Landschaft','Schaffhausen','Zug','Obwalden','Nidwalden','Appenzell Ausserrhoden','Appenzell Innerrhoden'),sources='CHE',note='ベルンなどにはフランス語地区もあり、このまとめは主な位置を示す。',stats='che-de_CH')
add('CHE','french','西部（ジュネーブ・ローザンヌなど）','fr',geometry=admin('Genève','Vaud','Neuchâtel','Jura','Fribourg','Valais'),sources='CHE',note='フリブール・ヴァレーは二言語州。州内のドイツ語地区までフランス語一色とはしない。',stats='che-fr')
add('CHE','italian','南部（ティチーノと東隣の谷）','it',geometry=admin('Ticino'),sources='CHE',note='東隣のグラウビュンデン州南側の谷にもイタリア語地区。',stats='che-it')
add('CHE','romansh','南東部の山地（グラウビュンデンの一部）','rm',geometry=admin('Graubünden'),sources='CHE',note='州内はロマンシュ語・ドイツ語・イタリア語のモザイク。塗色は州の位置のみ。',stats='che-romansh-area che-rm')
add('AUT','slovene','南端・スロベニア国境近く','sl',geometry=bounds(13.6,46.4,15.1,46.85),sources='AUT-UN CHARTER',note='ケルンテン南部などの二言語地名。')
add('AUT','croatian','東端・ハンガリー国境近く','hr',geometry=admin('Burgenland'),sources='AUT-UN CHARTER',note='ブルゲンラント内の一部集落。県全域の主表示ではない。')
add('AUT','hungarian','東端（オーバーヴァルト周辺）','hu',geometry=point(16.20,47.29),sources='AUT-UN CHARTER',note='ハンガリー語の公的地名を持つ一部集落。')
for key,area,lang,geo in [
 ('german','北端・オーストリア国境（ボルツァーノ）','de',admin('Bozen')),
 ('ladin','北東の山地（ドロミテの谷）','lld',point(11.67,46.55)),
 ('french','北西端・フランス国境（アオスタ）','fr',admin('Aoste')),
 ('francoprov','北西端のアオスタ谷','frp',admin('Aoste')),
 ('friulian','北東部（ウーディネ周辺）','fur',admin('Udine','Pordenone','Gorizia')),
 ('slovene','北東端・スロベニア国境','sl',admin('Trieste','Gorizia')),
 ('sardinian','西の大きな島（サルデーニャ）','sc',bounds(8,38.8,10,41.4)),
 ('catalan','サルデーニャ島北西岸（アルゲーロ）','ca',point(8.32,40.56))]:
    add('ITA',key,area,lang,geometry=geo,sources='ITA ITA-PCGN',note='イタリア語との地域的な併記。谷・集落によって言語が異なる。',stats='tyrol-de tyrol-it tyrol-lld' if key in ('german','ladin') else None)

# Iberia
for key,area,lang,geo,st in [
 ('catalan','北東部（バルセロナ周辺）','ca',admin('Lérida','Gerona','Barcelona','Tarragona'),'catalan-speak'),
 ('valencian','東岸（バレンシア周辺）','ca',admin('Castellón','Valencia','Alicante'),''),
 ('balearic','東の沖合（バレアレス諸島）','ca',admin('Baleares'),''),
 ('basque','北部・フランス国境の大西洋側','eu',admin('Gipuzkoa','Bizkaia','Álava'),'basque-bac'),
 ('navarre','北部（ナバラの北寄り）','eu',bounds(-2.5,42.7,-.7,43.4),'basque-nav'),
 ('galician','北西端（ガリシア）','gl',admin('La Coruña','Lugo','Orense','Pontevedra'),''),
 ('asturian','北岸（オビエド・ヒホン周辺）','ast',admin('Asturias'),''),
 ('aranese','北東の山中（アラン谷）','oc',point(.80,42.70),''),
 ('aragonese','北東部内陸（ウエスカ北側の一部）','an',point(-.3,42.6),'')]:
    add('ESP',key,area,lang,geometry=geo,sources='ESP',note='スペイン語との関係は地域差。地名が地域言語のみで公式の場合もある。',stats=st)
add('PRT','mirandese','北東端（ミランダ・ド・ドウロ）','mwl',geometry=point(-6.27,41.5),sources='PRT',note='ミランダ語が地域的に公認され、ポルトガル語と併記される地名もある。')

# Central and eastern Europe
for key,area,lang,geo,src in [
 ('kashubian','北部（グダニスクの西）','csb',bounds(17.3,53.7,18.7,54.9),'POL-MIN'),
 ('german','南西部（オポーレ周辺）','de',admin('Opole'),'POL-MIN'),
 ('belarusian','東端・ベラルーシ国境','be',bounds(22.8,52.4,24,53.5),'POL-MIN2'),
 ('lithuanian','北東端・リトアニア国境','lt',point(23.18,54.25),'POL-MIN2'),
 ('lemko','南東の山地・スロバキア国境','rue',bounds(20.7,49.2,22,49.75),'POL-MIN')]:
    add('POL',key,area,lang,geometry=geo,sources=src,note='公認の追加地名がある自治体の位置。塗色内の全自治体に設置されるわけではない。')
add('CZE','polish','東端（チェスキー・チェシーン周辺）','pl',geometry=point(18.63,49.75),sources='CZE CHARTER',note='ポーランド語との二言語地名。')
add('SVK','hungarian','南部・ハンガリー国境沿い','hu',geometry=bounds(17,47.65,22.2,48.6),sources='SVK CHARTER',note='南部のハンガリー語使用自治体。北寄りにかかる塗色は概略。')
add('SVK','rusyn','北東端（ポーランド・ウクライナ近く）','rue',geometry=bounds(21,48.85,22.65,49.5),sources='SVK CHARTER',note='一部自治体の少数言語地名。')
add('HUN','german','南西部（ペーチ周辺の集落）','de',geometry=point(18.23,46.08),sources='CHARTER',status='少数言語の自治体・文化表示',note='ドイツ語は他地方の集落にもある。点は代表的な地域を示す。')
add('HUN','slovak','南東部（ベーケーシュチャバ周辺）','sk',geometry=point(21.09,46.68),sources='CHARTER',status='少数言語の自治体・文化表示')
add('ROU','hungarian-east','中央の東寄り（セーケイ地方）','hu',geometry=admin('Harghita','Covasna','Mures'),sources='ROU',note='地域の中でも市町村差。ルーマニア語とハンガリー語の併記が補助。')
add('ROU','hungarian-west','北西部・ハンガリー国境近く','hu',geometry=admin('Satu Mare','Bihor','Salaj'),sources='ROU',note='自治体ごとに併記。中央東寄りの集住地とは分けて覚える。')
add('ROU','german','中央南部（シビウ・ブラショヴ周辺）','de',geometry=point(24.15,45.8),sources='ROU CHARTER',status='少数言語・歴史的地名の表示',note='ドイツ語の旧地名・文化案内など。現住民の多数言語ではない。')
add('MDA','gagauz','南部（コムラト周辺）','gag ru',geometry=bounds(28.4,45.7,29.1,46.6),sources='MDA MDA-REG',note='ガガウズ自治地域は飛び地を含む。地図は南部の概略でロシア語表示も多い。',stats='mda-gag-reg')
add('MDA','bulgarian','南端（タラクリア周辺）','bg',geometry=point(28.66,45.9),sources='MDA CHARTER',status='少数言語の自治体・文化表示')
add('MDA','transnistria','東端・ドニエストル川東岸など','ru uk',geometry=bounds(29,46.6,30.2,48.2),sources='MDA',status='事実上の行政・地域表示',note='沿ドニエストルの統治・表示は別事情。ロシア語が目立ち、ウクライナ語にも公的地位。キリル表記のモルドバ語は別行。')
add('UKR','hungarian','西端（ハンガリー国境近く）','hu',geometry=point(22.64,48.21),sources='UKR CHARTER',note='ザカルパッチャ南西側の一部。資料は戦前の地域状況を含む。')
add('UKR','romanian','南西部（チェルニウツィの南など）','ro',geometry=point(25.92,48.15),sources='UKR CHARTER',note='ルーマニア国境近くの一部。資料・画像の撮影年を確認。')
add('UKR','russian','東部・南部・クリミアなどの旧画像','ru',geometry=bounds(33,44.3,40.3,50.4),sources='UKR RUS',status='歴史的・事実上の表示（撮影年依存）',note='ロシア語は旧画像や現在の一部表示にもある。言語と国境を結び付けない。地図の範囲は便宜的。')

# Adriatic and southern Balkans
add('SVN','italian','南西端の海岸（コペル・ピラン）','it',geometry=admin('Koper','Piran','Izola'),sources='SVN')
add('SVN','hungarian','北東端・ハンガリー国境','hu',geometry=admin('Lendava','Dobrovnik','Hodoš','Šalovci','Moravske Toplice'),sources='SVN',note='自治体の中の混住地域。')
add('HRV','italian','北西の半島（イストラ）','it',geometry=admin('Istarska'),sources='CHARTER ITA',note='二言語自治体ではクロアチア語とイタリア語を併記。')
add('HRV','serbian','東端（ドナウ川近くの一部自治体）','sr',geometry=point(18.95,45.42),sources='CHARTER',note='キリル文字の地名・公共施設表示がある自治体。設置状況に地域差。')
add('SRB','vojvodina','北部（ヴォイヴォディナ）','hu sk ro rsk hr',geometry=admin('Severno-Backi','Zapadno-Backi','Severno-Banatski','Južno-Backi','Srednje-Banatski','Južno-Banatski','Sremski'),sources='SRB',note='州の5つの追加公用語。実際の併記は言語集落・自治体ごとに異なる。')
add('SRB','bosnian','南西部（ノヴィ・パザル周辺）','bs',geometry=point(20.52,43.14),sources='SRB CHARTER',note='サンジャク地方の自治体で公的使用。')
add('SRB','albanian','南端（プレシェヴォ周辺）','sq',geometry=point(21.65,42.31),sources='SRB CHARTER',note='北マケドニア・コソボに近い一部自治体。')
add('XKX','turkish','南部（プリズレンなど）','tr bs',geometry=point(20.74,42.21),sources='XKX',note='トルコ語などの自治体公用語。地域全体の主表示ではない。')
add('MNE','albanian','南東端（ウルツィニ・トゥジ）','sq',geometry=bounds(19.1,41.8,19.6,42.5),sources='MNE',note='アルバニア国境近く。Ulcinj / Ulqinなどの地名。')
add('ALB','greek','南端・ギリシャ国境近く','el',geometry=point(20.26,39.88),sources='CHARTER PCGN',note='ギリシャ語少数言語地域の一部表示。')
add('MKD','albanian','西部・北西部（テトヴォなど）','sq',geometry=bounds(20.45,40.85,21.45,42.4),sources='MKD',note='アルバニア語の併記が位置の補助。国の公的使用の範囲はこれより広い。',stats='mkd-sq')
add('MKD','turkish','中西部の一部自治体','tr',geometry=point(21,41.51),sources='MKD CHARTER',note='自治体公用語の一つ。マケドニア語との併記。')
add('MKD','romani','北部・首都スコピエの一地区','rom',geometry=point(21.42,42.04),sources='MKD CHARTER',note='シュト・オリザリ地区の地域公用語。全国の道路標識の言語ではない。')
add('MKD','serbian','北端（首都スコピエの北側）','sr',geometry=point(21.3844,42.1019),sources='MKD',status='自治体公用語（表示の量は未測定）',note='チュチェル・サンデヴォの自治体公用語。セルビア語の字形があっても国境の北側とは限らない。')
add('MKD','aromanian','中西部内陸（クルシェヴォ周辺）','rup',geometry=point(21.2483,41.3694),sources='MKD',status='自治体公用語（表示の量は未測定）',note='クルシェヴォの自治体公用語。Crushuvaはアルーマニア語の地名形。地図の点は自治体の代表位置。')

# Cyprus and Caucasus
add('CYP','south','島の南部（共和国政府管理地域）','el',geometry={'type':'country','adm0':['CYP']},sources='CYP CYP-PIO',note='ギリシャ語が主表示。英語やラテン文字への転写も併用される。')
add('CYP','north','島の北部（事実上別の行政下）','tr',geometry={'type':'country','adm0':['CYN']},sources='CYP CYP-PIO',note='トルコ語が主表示。キプロスの憲法上の公用語はギリシャ語とトルコ語。境界はNatural Earthの表示区分。')
add('GEO','abkhazia','北西部・黒海沿岸（アブハジア）','ab ru',geometry=admin('Abkhazia'),sources='GEO GEO-LAW',note='アブハズ語の法的位置と、事実上の行政・表示状況を分ける。ジョージア文字だけではない。')
add('GEO','ossetia','北寄りの中央山地（南オセチア）','os ru',geometry=bounds(43.7,42,44.7,42.8),sources='GEO',status='事実上の地域公用語・表示',note='塗色は位置の概略。行政上・国際的な地位の主張ではない。')

# Russia: official republic languages; no assertion that they dominate street signs.
RUSSIA=[
 ('tatar','西部内陸（カザン周辺）','Tatarstan','tt','ロシア・ヴォルガ川周辺'),
 ('bashkir','西部内陸（ウファ周辺）','Bashkortostan','ba','ロシア・ヴォルガ川周辺'),
 ('chuvash','西部内陸（カザンの西）','Chuvash','cv','ロシア・ヴォルガ川周辺'),
 ('mari','西部内陸（カザンの北西）','Mariy-El','mhr mrj','ロシア・ヴォルガ川周辺'),
 ('udmurt','西部内陸（カザンの北東）','Udmurt','udm','ロシア・ヴォルガ川周辺'),
 ('mordovia','西部内陸（モスクワの東南東）','Mordovia','myv mdf','ロシア・ヴォルガ川周辺'),
 ('komi','北西部内陸（ウラル山脈の西）','Komi','kv','ロシア・北西部とカスピ海'),
 ('kalmyk','南西部（カスピ海北西）','Kalmyk','xal','ロシア・北西部とカスピ海'),
 ('adyghe','南西端（黒海の北東側）','Adygey','ady','ロシア・北コーカサス'),
 ('karachay','南西端（黒海とカスピ海の間・西寄り）','Karachay-Cherkess','krc kbd abq nog','ロシア・北コーカサス'),
 ('kabardin','南西端（コーカサス山脈の中央）','Kabardin-Balkar','kbd krc','ロシア・北コーカサス'),
 ('ossetian','南西端（ジョージア北隣）','North Ossetia','os','ロシア・北コーカサス'),
 ('ingush','南西端（北オセチアの東隣）','Ingush','inh','ロシア・北コーカサス'),
 ('chechen','南西端（イングーシの東隣）','Chechnya','ce','ロシア・北コーカサス'),
 ('dagestan','南西端（カスピ海西岸・ダゲスタン）','Dagestan','av dar kum lez lak tab nog ce az_Cyrl agx rut jdt tkr','ロシア・ダゲスタン'),
 ('altai','南部（カザフスタン・モンゴルの間）','Gorno-Altay','alt','ロシア・南シベリア'),
 ('khakas','南部（クラスノヤルスクの南）','Khakass','kjh','ロシア・南シベリア'),
 ('tuva','南部・モンゴル北隣（キジル周辺）','Tuva','tyv','ロシア・南シベリア'),
 ('buryat','南東部（バイカル湖東側）','Buryat','bua','ロシア・南シベリア'),
 ('sakha','東部の広い内陸（ヤクーツク周辺）','Sakha (Yakutia)','sah','ロシア・極東')]
for key,area,aname,langs,group in RUSSIA:
    note='共和国の公用語を収録。塗色は共和国の外形で、話者の密度・看板の頻度・言語の排他的境界を示さない。'
    if key=='tatar':note+=' 2018年調査で街路名・公共施設への併記を確認。'
    if key=='chuvash':note+=' 2018年調査ではチェボクサルの街路名併記。'
    if key=='udmurt':note+=' 2018年調査では一部道路・公共表示に使用。'
    if key=='kalmyk':note+=' 2018年調査では街路名より民間の表示が中心。'
    if key=='dagestan':note+=' 言語ごとの使用集落は異なる。全13言語が同じ看板に並ぶという意味ではない。'
    add('RUS',key,area,langs,group=group,geometry=admin(aname),sources='RUS RUS-SIGNS' if key in ('tatar','chuvash','udmurt','kalmyk') else 'RUS',status='共和国公用語（実際の表示は局所・地域差）',note=note)

# Page windows: (west,south,east,north). They are saved in the output manifest.
VIEWS={
 '英国・アイルランド':(-11,49,2.5,61),'海峡諸島':(-3.1,48.9,-1.65,49.85),
 '北大西洋':(-26,54,33,81.5),'北欧南部':(4.5,54,25,69),'フィンランド':(18,59,32,71),
 '北欧の地域言語':(8.5,61,32,72),'バルト海東岸':(20,53,29,60),
 'ベネルクス':(2.2,49.3,7.5,54),'フランス':(-5.5,41,10,51.5),'ドイツ':(5.5,47,15.5,55.5),
 'アルプス':(9,45.6,17.4,49.2),'スイス':(5.8,45.7,10.8,47.95),
 'イベリア半島':(-10.5,35.5,5,44.3),'イタリア':(6,35,19,47.3),
 'ポーランド':(13.7,48.8,24.3,55),'中央ヨーロッパ':(11.8,45.5,23,51.3),
 '西バルカン':(12.7,41.8,20.5,47.1),'セルビア・コソボ':(18.5,41.5,23.2,46.5),
 'バルカン南部':(18.3,39.4,23.3,43.7),'ギリシャ・キプロス':(13,33.5,35,42.3),
 '黒海周辺':(19.8,41,31,48.6),'ウクライナ・ベラルーシ':(21.5,44,41,57),
 '南コーカサス':(39.5,38.5,51,44),'ロシア全域':(19,41,180,79),
 'ロシア・ヴォルガ川周辺':(40,52.5,61,59.9),'ロシア・北西部とカスピ海':(35,43,69,70),
 'ロシア・北コーカサス':(38.5,41.8,48.4,46),'ロシア・ダゲスタン':(45.4,41.1,48.7,45.3),
 'ロシア・南シベリア':(82,48,117,59),'ロシア・極東':(105,53,165,75)}

for r in REGIONS:
    assert set(r['languages']) <= LANGUAGES.keys(), r
    assert r['group'] in VIEWS, r

add('MDA','moldovan-cyrillic','東端（沿ドニエストル）','ro_Cyrl',geometry=point(29.64,46.84),sources='MDA',status='事実上の地域公用語の表記',note='キリル文字のモルドバ語。共和国政府側のルーマニア語ラテン表記と分ける。')
add('SWE','sami-ume','北中部（ウメオの北西側）','sju',group='北欧の地域言語',geometry=point(18.15,65.53),sources='SAMI-NAMES',note='ウメ・サーミ語地名。道路上では他のサーミ語とも文字を共有する。')
add('ALB','macedonian','南東端（プレスパ湖畔）','mk',geometry=point(20.91,40.79),sources='ALB-SIGNS',note='プステツなどのマケドニア語との二言語表示。')
add('HRV','czech','北部内陸（ダルヴァル周辺）','cs',geometry=point(17.23,45.55),sources='HRV-SIGNS',note='周辺の一部集落・自治体。2024年の規定を含む2025年報告に基づく。')
add('SJM','russian','西側の鉱山集落（バレンツブルクなど）','ru',geometry=point(14.23,78.06),sources='SVALBARD',status='鉱山集落・施設の地域表示',note='ノルウェー主権下でもロシア語の集落がある。ピラミデンなどの歴史的表示も候補。島全体の公用語ではない。')
for r in REGIONS:
    if r['id'].startswith('hun-') and r['kind']!='national':r['sources']=['HUN-SIGNS','CHARTER']
    if r['iso3']=='AUT':r['sources']=['AUT-UN','CHARTER']
    if r['id']=='hrv-italian' or r['id']=='hrv-serbian':r['sources']=['HRV-SIGNS','HRV-OP']
    if r['id']=='alb-greek':r['sources']=['ALB-SIGNS']
