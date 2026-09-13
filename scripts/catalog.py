"""Editorial source of the study regions. All geometry is coarse, never a rate raster.

Edit this file to add or refine regions. Numeric facts belong in data/*statistics* or
the original extracted tables; ratings remain explicit editorial judgements.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REGIONS=[]

def add(iso,slug,area,level,geometry,note,stats=None,sources=None,clothing=None):
    REGIONS.append(dict(id=f'{iso}-{slug}',iso3=iso,area_ja=area,level=level,
        geometry=geometry,explanation=note,statistics=stats or [],
        sources=sources or ['PEW2025'],clothing_sources=clothing or [],
        rating_status='学習用の定性推定（街頭出現率の実測値ではない）'))
def country(iso,level,note,**kwargs):add(iso,'all','全域（住民の生活圏）',level,{'type':'country'},note,**kwargs)
def admin(iso,slug,area,level,names,note,**kwargs):add(iso,slug,area,level,{'type':'admin1','names':names.split('|')},note,**kwargs)
def box(iso,slug,area,level,bounds,note,**kwargs):add(iso,slug,area,level,{'type':'bbox','bounds':bounds},note,**kwargs)
def polygon(iso,slug,area,level,coordinates,note,**kwargs):add(iso,slug,area,level,{'type':'polygon','coordinates':coordinates},note,**kwargs)
def city(iso,slug,area,lon,lat,note='',**kwargs):add(iso,slug,area,'やや高い',{'type':'point','coordinates':[lon,lat]},note or '都市内のムスリム居住地区で見られる可能性がある。点は位置の目印で、市全域の着用率や居住範囲を表さない。',**kwargs)

# North Africa. Liberal cities and tourist sites are not uniform clothing samples.
country('EGY','高い','ナイル川沿い・デルタの生活圏が中心。全国のムスリム女性への2010年調査で、いつも62%、大抵21%が頭を覆うと回答。',clothing=['PEW_DRESS2010'])
country('DZA','やや高い','北部の地中海沿岸に人口が集中。宗教人口は多いが、着用率を同じ数字とはみなさない。')
country('MAR','やや高い','北部・西部の都市や農村が主な生活圏。頭を覆わない女性も多く、都市・観光地と集落で差がある。')
country('TUN','やや高い','北部・東部沿岸の生活圏。ムスリム人口の多さだけで「高い」とは判定しない。')
country('LBY','高い','北部の地中海沿岸の生活圏を主に想定。広大な南部砂漠の塗色は人口密度を表さない。',sources=['PEW2025','IRF-LBY'])
country('SDN','高い','ナイル川沿い、北部・東部・西部のムスリム生活圏。避難・人口移動が大きく、資料年と撮影年に注意。',sources=['PEW2025','IRF-SDN'])
country('ESH','やや高い','西サハラの住民生活圏。頭を覆うメルハファ等との混同があるため、ヒジャブ単独については保守的な評価。帰属係争があり地図は境界を確定するものではない。')

# West and Central Africa: headwraps are not automatically hijab.
country('MRT','やや高い','北西アフリカの大西洋岸から内陸。メルハファなど地域衣装との混同があるため、ヒジャブ単独については保守的な評価。',sources=['PEW2025','IRF-MRT'])
country('SEN','やや高い','西端のダカールを含む広い生活圏。首を覆わない頭巻きや未着用もあり、宗教人口比率から着用率を決めない。')
country('GMB','やや高い','セネガルに囲まれた細長い国の全域。頭巻きとの見分けが必要。')
country('NER','やや高い','住民の多い南部、ナイジェリア国境沿いが中心。北部砂漠の面積と遭遇機会は比例しない。')
country('MLI','やや高い','南西部のバマコ周辺からニジェール川沿い、北部の町。地域衣装の頭布も多く、一律の着用率はない。')
country('BFA','やや高い','特に北部・東部、首都のムスリム生活圏。伝統的な頭巻きを含めて判定しない。')
box('GIN','north','北部・中部・西部（南東部の森林地帯を除く）','やや高い',[-15.2,9.1,-8.0,12.8],'北部・中部・海岸部のムスリム生活圏。南東部の森林地域は宗教構成が異なる。',sources=['PEW2025','IRF-GIN'])
box('GNB','interior','北東部・東部（セネガル／ギニア国境寄り）','やや高い',[-15.25,11.1,-13.5,12.75],'内陸のムスリム居住地域を学習用に大きく囲った範囲。沿岸全体の着用率を示さない。',sources=['PEW2025','IRF-GNB'])
country('SLE','やや高い','北部・東部を含むムスリム生活圏。宗教が混在し、一般的な頭巻きも見られる。')
box('CIV','north','北部（マリ・ブルキナファソ国境寄り）','やや高い',[-8.7,8.0,-2.4,10.8],'北部にムスリム人口が多い。南部にも居住しているので北部に限定できる手掛かりではない。',sources=['PEW2025','IRF-CIV'])
city('CIV','abidjan','南部アビジャンの一部',-4.03,5.35,sources=['PEW2025','IRF-CIV'])
box('GHA','north','北部（タマレ周辺とその北）','やや高い',[-2.9,8.55,0.6,11.2],'北部のムスリム生活圏。北部全域が同じ宗教・服装ではない。',sources=['PEW2025','IRF-GHA'])
city('GHA','accra','南部アクラのゾンゴ地区など',-0.21,5.57,sources=['PEW2025','IRF-GHA'])
box('TGO','north','北部（ブルキナファソ国境寄り）','やや高い',[-0.2,9.1,1.5,11.2],'北部のムスリム生活圏を大まかに示す。宗教の混在と一般の頭巻きに注意。',sources=['PEW2025','IRF-TGO'])
admin('BEN','north','北部・北東部（ニジェール／ナイジェリア国境寄り）','やや高い','Alibori|Borgou|Donga','ムスリム人口の多い北部・北東部をまとめたもの。各県内にも宗教の混在がある。',sources=['PEW2025','IRF-BEN'])
admin('NGA','north','北部（北西部と北東部の中心域）','高い','Sokoto|Zamfara|Kebbi|Katsina|Kano|Jigawa|Yobe|Borno|Bauchi|Gombe','北西部・北東部ではイスラム教が優勢。2010年の全国ムスリム女性調査では、いつも53%、大抵16%が頭を覆う。北部全住民がムスリムという意味ではない。',sources=['PEW2025','IRF-NGA'],clothing=['PEW_DRESS2010'])
admin('NGA','transition','中北部・北東部南縁（アブジャ周辺など）','やや高い','Kaduna|Niger|Kwara|Nassarawa|Federal Capital Territory|Adamawa|Taraba','キリスト教・イスラム教が混在する移行帯。カドゥナ州の北部と南部にも差がある。',sources=['PEW2025','IRF-NGA'],clothing=['PEW_DRESS2010'])
admin('NGA','southwest','南西部（ラゴス・イバダン周辺）','やや高い','Lagos|Ogun|Oyo|Osun','南西部にもムスリムが多く住む。ヒジャブを見て直ちに北部と決めない。',sources=['PEW2025','IRF-NGA'],clothing=['PEW_DRESS2010'])
box('TCD','north','北部・中部（首都ンジャメナを含む）','やや高い',[13.4,11.6,24.1,23.5],'イスラム教人口が多い北部・中部。南部にはキリスト教・伝統宗教の人口が多い。',sources=['PEW2025','IRF-TCD'])
box('CMR','north','北部の細長い部分（ナイジェリア／チャド寄り）','やや高い',[12.0,7.0,16.3,13.1],'北部にムスリム人口が集中するが一様ではない。南部の熱帯都市も完全な除外はできない。',sources=['PEW2025','IRF-CMR'])

# Eastern and Southern Africa.
country('SOM','高い','東アフリカの角の住民生活圏。ソマリランドを含めた地理的表示。長い覆い・ジルバブ・顔の覆いを伴うこともある。',sources=['PEW2025','SOM_DRESS'])
country('DJI','高い','紅海入口の小国。ソマリ系・アファル系の生活圏で頭を覆う服装が見られる。数値は宗教人口で、着用率の全国実測値は未取得。',sources=['PEW2025','IRF-DJI'])
admin('ERI','lowlands','西部の低地と紅海沿岸','やや高い','Gash Barka|Anseba|Semenawi Keyih Bahri|Debubawi Keyih Bahri','ムスリム人口は低地・沿岸に多い。中央のアスマラ周辺の高地を除いた大まかな行政地域。県内にも高地や宗教の混在がある。',sources=['PEW2025','IRF-ERI'])
admin('ETH','east','東部（ソマリア国境寄り）','高い','Somali','ソマリ州のムスリム生活圏。全国平均をこの地域の率として使わない。',sources=['PEW2025','IRF-ETH'])
admin('ETH','northeast','北東部（ジブチ・エリトリア国境寄りの低地）','やや高い','Afar','アファル低地のムスリム生活圏。高原側のキリスト教徒の頭布との混同に注意。',sources=['PEW2025','IRF-ETH'])
box('ETH','southeast','東中部・南東部（ハラール周辺から南へ）','やや高い',[39,6,43,10],'ハラール周辺とオロミア州東部・南東部の一部。長方形を国境で切った概略で、宗教境界ではない。',sources=['PEW2025','IRF-ETH'])
admin('KEN','northeast','北東部（ソマリア国境沿い）','高い','North-Eastern','ムスリムが多いソマリア国境側。旧州境を使った大まかな表示。',sources=['PEW2025','IRF-KEN'])
box('KEN','coast','南東部の海岸（モンバサ～ラム）','やや高い',[39.2,-4.9,41.9,-1.6],'スワヒリ海岸のムスリム生活圏。海岸州の内陸すべてに同じ傾向があるとは限らない。',sources=['PEW2025','IRF-KEN'])
city('KEN','nairobi','中南部ナイロビ東部の一部',36.86,-1.28,sources=['PEW2025','IRF-KEN'])
admin('TZA','zanzibar','東部沖の島々（ザンジバル・ペンバ）','高い','Zanzibar South and Central|Kaskazini-Unguja|Zanzibar West|Kusini-Pemba|Kaskazini-Pemba','ザンジバルはムスリム約99%との推計。沿岸本土と区別して覚える。',stats=[['MANUAL','Zanzibar']],sources=['IRF-TZA'])
admin('TZA','coast','東部の海岸（ダルエスサラーム周辺）','やや高い','Tanga|Pwani|Dar-Es-Salaam|Lindi|Mtwara','本土のインド洋沿岸にムスリム生活圏が続く。州の内陸は混在する。',sources=['PEW2025','IRF-TZA'])
admin('MOZ','north','北部（タンザニア国境・北東海岸）','やや高い','Cabo Delgado|Niassa|Nampula','北部のムスリム人口が多い地域。宗教分布と一般的な頭巻きは分ける。',sources=['PEW2025','IRF-MOZ'])
box('MWI','south','南部（マラウイ湖の南端周辺）','やや高い',[34.6,-15.6,35.8,-13.5],'マンゴチ・マチンガなど南部のムスリム生活圏。湖全周や国全域を意味しない。',sources=['PEW2025','IRF-MWI'])
city('UGA','kampala','南部カンパラの一部',32.58,0.32,sources=['PEW2025','IRF-UGA'])
country('COM','やや高い','インド洋のコモロ諸島。頭を覆うシロマニなど地域衣装もあり、一般のヒジャブと形が異なる。')
box('MYT','island','マヨット島（アフリカ東岸沖）','やや高い',[45.0,-13.1,45.4,-12.55],'国連M49では東アフリカの独立した統計地域。フランス本土の傾向と混同しない。頭布の形に注意。')
city('MUS','port-louis','北西部ポートルイスの一部',57.50,-20.16)
city('MDG','mahajanga','北西部マハジャンガの一部',46.32,-15.72,sources=['PEW2025','IRF-MDG'])
city('ZAF','cape-town','南西端ケープタウンのボーカープ周辺',18.41,-33.92,'西ケープ州のムスリム人口は2022年に5.2%。州全体を塗らず、歴史的なムスリム地区の位置を点で示す。',stats=[['MANUAL','Western Cape']],sources=['ZAF2022'])
city('ZAF','durban','東岸ダーバンの一部',31.02,-29.86,sources=['PEW2025','IRF-ZAF'])
city('ZAF','johannesburg','北東部ヨハネスブルクの一部',28.00,-26.21,sources=['PEW2025','IRF-ZAF'])

# Southern Asia (UN M49 puts Iran here).
country('IRN','高い','国連M49では南アジア。頭を覆う法的要件がある一方、実際の着用や取り締まりには時期・都市差がある。法律だけを着用率とはみなさない。',sources=['PEW2025','FCDO-IRN'])
country('AFG','やや高い','頭髪・身体を覆う服装が広く想定されるが、ブルカや顔の覆いをヒジャブと同一の着用率にしない。2021年以降と過去画像で環境が異なる。',sources=['PEW2025','FCDO-AFG'])
country('PAK','高い','全国のムスリム女性調査（2010年）で、いつも32%、大抵29%が頭を覆う。ドゥパッタなど緩い頭布もあり、頭布一枚で判定しない。',clothing=['PEW_DRESS2010'])
country('BGD','やや高い','低地の住民生活圏に広く候補がある。サリーの布などヒジャブ以外の覆いもあるため、一律の高率とはしない。')
country('MDV','やや高い','住民島とマレを想定。観光リゾート島の服装を住民島に一般化しない。',sources=['PEW2025','FCDO-MDV'])

# India: distant regions remain distinct. Bboxes are intentionally approximate.
box('IND','kashmir','最北部（スリナガル周辺のカシミール盆地）','やや高い',[73.9,33.4,75.7,34.8],'ムスリム人口が非常に多い盆地。地区別のヒジャブ着用率は未取得なので保守的に「やや高い」。旧州全域やラダックまで同色にしない。',stats=[['IND','Srinagar']],sources=['IND_C01','PEW_IND_DRESS'])
box('IND','upper-ganges','北部（デリーの北東～東、ガンジス川上流の平野）','やや高い',[77.15,28.2,79.6,30.1],'ウッタル・プラデーシュ州西部のムスリムが多い地区。州全体の比率を個別地区の比率に置き換えない。',stats=[['IND','State - UTTAR PRADESH']],sources=['IND_C01','PEW_IND_DRESS'])
city('IND','delhi','北部デリー周辺（旧市街・北東部など）',77.23,28.66,'デリー全体とムスリムが多い地区には差がある。北東地区の統計をデリー全域に広げない。',stats=[['IND','North East']],sources=['IND_C01','PEW_IND_DRESS'])
city('IND','lucknow','北部ラクナウ周辺',80.95,26.85,'都市内にムスリム生活圏がある。過去のイスラム王朝の首都という歴史だけで周辺全域を「高い」にしない。',stats=[['IND','State - UTTAR PRADESH']],sources=['IND_C01','PEW_IND_DRESS'])
box('IND','bihar-east','東部（バングラデシュの北西側、ビハール州東端）','やや高い',[87.1,25.3,88.3,26.7],'キシャンガンジなどの人口集積。北東部全体ではなく、バングラデシュの北西側を覚える。',stats=[['MANUAL','Kishanganj district']],sources=['CENSUS2011_KISHANGANJ','PEW_IND_DRESS'])
box('IND','bengal','東部（バングラデシュ国境の西側）','やや高い',[87.6,21.6,89.2,25.65],'西ベンガル州の東寄りの地区。国境全線がムスリム多数という意味ではなく、コルカタなどにも混在する。',stats=[['IND','Murshidabad'],['IND','Maldah'],['IND','Nadia'],['IND','South Twenty Four Parganas']],sources=['IND_C01','PEW_IND_DRESS'])
box('IND','assam','北東部（バングラデシュ北側の低地）','やや高い',[89.6,25.2,92.2,26.6],'アッサム州の西部低地・バングラデシュに近い側。北東インドの山地全体へ広げない。',stats=[['IND','Dhubri'],['IND','Goalpara'],['IND','Barpeta']],sources=['IND_C01','PEW_IND_DRESS'])
box('IND','malabar','南西部（コジコード周辺～その北・南の海岸）','やや高い',[74.85,10.7,76.5,12.8],'北ケララのマラバール海岸。コジコードの英語旧称はカリカットで、東部のコルカタ（カルカッタ）とは別都市。マラップラムなど地区差がある。',stats=[['IND','Kozhikode'],['IND','Malappuram'],['IND','Kannur'],['IND','Kasaragod']],sources=['IND_C01','KOZHIKODE','PEW_IND_DRESS'])
admin('IND','lakshadweep','南西沖の小島群（ラクシャドウィープ）','やや高い','Lakshadweep','ケララ州沖の島々。人口構成はムスリム多数だが島別のヒジャブ着用率は未取得なので保守的に「やや高い」。',stats=[['IND','State - LAKSHADWEEP']],sources=['IND_C01','PEW_IND_DRESS'])
city('IND','hyderabad','南中部ハイデラバード旧市街周辺',78.47,17.36,'デカン高原内陸の独立した候補。南西海岸のコジコードとは離れている。',stats=[['IND','State - ANDHRA PRADESH']],sources=['IND_C01','PEW_IND_DRESS'])
city('IND','mumbai','西岸ムンバイの一部',72.84,18.98,stats=[['IND','Mumbai'],['IND','Mumbai Suburban']],sources=['IND_C01','PEW_IND_DRESS'])
city('IND','bhopal','中部ボパールの一部',77.40,23.26,stats=[['IND','State - MADHYA PRADESH']],sources=['IND_C01','PEW_IND_DRESS'])
city('IND','bengaluru','南部ベンガルールの一部',77.59,12.97,stats=[['IND','Bangalore']],sources=['IND_C01','PEW_IND_DRESS'])
polygon('NPL','terai','南部の低地（インド国境沿いの中西部・東部）','やや高い',[[80.8,28.5],[81.4,28.25],[82.2,28.05],[83.5,27.85],[84.5,27.65],[85.5,27.1],[86.5,26.95],[87.6,26.8],[87.6,26.25],[83.0,26.4],[80.8,27.0],[80.8,28.5]],'タライ低地のムスリム居住集落。地形に沿って手描きした概略で、集落の正確な境界ではない。',sources=['PEW2025','IRF-NPL'])
admin('LKA','east','東部海岸（トリンコマリー～アンパラ）','やや高い','Trikuṇāmalaya|Maḍakalapuva|Ampāra','2024年の宗教別人口はトリンコマリー46.5%、アンパラ45.6%、バッティカロア27.1%。東部全域で女性の多数が着用するとの実測値ではない。',stats=[['LKA','Trincomalee'],['LKA','Ampara'],['LKA','Batticaloa']],sources=['LKA2024'])
admin('LKA','northwest','北西部海岸（プッタラム～マンナール）','やや高い','Puttalama|Mannārama','離れた東海岸と別に覚える。2024年のムスリム人口はプッタラム21.6%、マンナール27.4%。',stats=[['LKA','Puttalam'],['LKA','Mannar']],sources=['LKA2024'])
city('LKA','colombo','西部コロンボの一部',79.86,6.93,stats=[['LKA','Colombo']],sources=['LKA2024'])
city('LKA','kandy','中部キャンディ周辺の一部',80.63,7.29,stats=[['LKA','Kandy']],sources=['LKA2024'])

# Southeast Asia.
admin('IDN','sumatra','西部スマトラ島（北端アチェ・西部・南部など）','高い','Aceh|Sumatera Barat|Riau|Jambi|Sumatera Selatan|Bengkulu|Lampung|Bangka-Belitung|Kepulauan Riau','ムスリム多数の州をまとめる。北スマトラ州のバタク高地などを一括で同色にしない。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','north-sumatra','スマトラ島北部（メダン周辺を含む北スマトラ州）','やや高い','Sumatera Utara','州全体は宗教が混在する。トバ湖周辺・西沖の島々と東岸の都市で差が大きい。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','java','南西部ジャワ島（ジャカルタを含む）','高い','Jawa Barat|Jawa Tengah|Jawa Timur|Jakarta Raya|Banten|Yogyakarta','インドネシアの人口集積の中心。全国ムスリム女性調査の通常着用61.9%（2022年）を参照するが、各州の実測率ではない。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','lombok','南部のロンボク島・スンバワ島（バリの東隣）','高い','Nusa Tenggara Barat','バリ島と、さらに東のフローレス島・ティモール島を同一視しない。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','borneo-se','ボルネオ島の南部・東部','高い','Kalimantan Selatan|Kalimantan Timur','南部・東部の州。州内の森林集落や少数宗教地域には差がある。旧東カリマンタン州の範囲には現在の北カリマンタン州を含む。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','borneo-wc','ボルネオ島の西部・中部','やや高い','Kalimantan Barat|Kalimantan Tengah','ムスリム・キリスト教徒などが混在。海岸都市と内陸で差がある。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','sulawesi','中央東部スラウェシ島（北東端を除く）','やや高い','Sulawesi Selatan|Sulawesi Barat|Sulawesi Tenggara|Sulawesi Tengah|Gorontalo','ムスリム多数の州だが、トラジャ高地など州内の宗教差が大きいため保守的に「やや高い」。北東端のマナド周辺を除く。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('IDN','maluku','東部マルク諸島','やや高い','Maluku|Maluku Utara','島ごとの宗教差が大きい。パプア全体をムスリム地域として塗らない。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
city('IDN','bali-denpasar','南部バリ島デンパサールの一部',115.22,-8.66,'バリ島はヒンドゥー教徒が多数。ムスリム居住地区の補足候補を点で示し、島全体は無着色とする。',sources=['BPS2010','ISEAS2022'],clothing=['ISEAS2022'])
admin('MYS','peninsula-east','マレー半島の北部・東岸','高い','Kelantan|Terengganu|Kedah|Perlis|Pahang','クランタン州では2020年にムスリム95.5%。半島の北東部を特に覚える。数値は宗教人口。',stats=[['MANUAL','Kelantan']],sources=['DOSM2020','MYS_DRESS'])
admin('MYS','peninsula-west','マレー半島の西岸・南部（クアラルンプール周辺など）','やや高い','Perak|Pulau Pinang|Selangor|Kuala Lumpur|Putrajaya|Negeri Sembilan|Melaka|Johor','都市ごとにムスリム・仏教徒・ヒンドゥー教徒などが混在。北東部と同率にしない。',sources=['PEW2025','MYS_DRESS'])
admin('MYS','sabah','ボルネオ島北東部（サバ州）','やや高い','Sabah|Labuan','海岸部のムスリム生活圏と内陸の宗教構成には差がある。',sources=['PEW2025','IRF-MYS','MYS_DRESS'])
city('MYS','kuching','ボルネオ島北西部クチンの一部',110.34,1.56,'サラワク州全域は塗らず、都市のムスリム生活圏を補足する。',sources=['PEW2025','IRF-MYS','MYS_DRESS'])
country('BRN','高い','ボルネオ島北岸の小国。頭を覆うトゥドゥンが見られる生活圏。外国人や宗教少数派まで一律ではない。',sources=['PEW2025','IRF-BRN'])
admin('THA','deep-south','最南部（マレーシア国境近く）','高い','Pattani|Yala|Narathiwat|Satun','マレー系ムスリムが多い南端。半島南部全域が同じ宗教構成ではない。',sources=['PEW2025','IRF-THA'])
admin('THA','andaman','南部の西海岸（クラビー・パンガー・プーケット周辺）','やや高い','Krabi|Phangnga|Phuket|Trang','ムスリムの生活圏と観光地・仏教徒の集落が混在する。',sources=['PEW2025','IRF-THA'])
city('THA','bangkok','中部バンコク東部などの一部',100.62,13.76,sources=['PEW2025','IRF-THA'])
admin('PHL','mindanao','南部ミンダナオ島の西寄り（コタバト・マラウィ周辺）','高い','Lanao del Sur|Maguindanao','旧BARMM集計のムスリム人口は90.9%（2020年、世帯人口）。ミンダナオ島全体を塗らない。',stats=[['MANUAL','BARMM2020']],sources=['PSA2020'])
admin('PHL','sulu','南西端の島列（バシラン・スールー・タウィタウィ）','高い','Basilan|Sulu|Tawi-Tawi','ミンダナオからボルネオへ伸びる島々。2020年の地域集計と現在の行政区分には差がある。',stats=[['MANUAL','BARMM2020']],sources=['PSA2020'])
country('SGP','やや高い','小さな都市国家のマレー系・ムスリム生活圏。ヒジャブは国全体がムスリム多数である証拠ではない。')
box('KHM','mekong','中部（プノンペン北方、メコン川沿い）','やや高い',[104.5,11.5,106.2,13.0],'チャム系ムスリムの集落が点在。四角形は集落の位置を探す概略で、範囲内が一様という意味ではない。',sources=['PEW2025','IRF-KHM'])
box('MMR','rakhine','西端（バングラデシュ国境寄り）','やや高い',[92.1,20.2,93.3,21.6],'北ラカインのムスリム生活圏。迫害・避難で人口分布が大きく変わっており、過去の人口値を現在へ外挿しない。',sources=['PEW2025','IRF-MMR'])
city('MMR','yangon','南部ヤンゴンの一部',96.16,16.78,sources=['PEW2025','IRF-MMR'])

# Western Asia and Central Asia.
box('TUR','interior','中央部・東部の内陸（アンカラ以東）','高い',[31,35.8,44.9,42.2],'全国2010年調査ではムスリム女性の56%がいつも、6%が大抵頭を覆う。内陸の服装傾向は定性推定で、東西の実測率差は未取得。',clothing=['PEW_DRESS2010','GALLUP_TUR'])
box('TUR','west','西部（イスタンブール・エーゲ海岸周辺）','やや高い',[25.5,35.8,31,42.2],'大都市・海岸部には未着用女性も多い。全国値を西部固有の率とはしない。',clothing=['PEW_DRESS2010','GALLUP_TUR'])
country('IRQ','高い','メソポタミアの都市・集落が主な生活圏。北部クルディスタン、都市、少数宗教地区の差を含む定性推定。',sources=['PEW2025','IRF-IRQ'])
country('SYR','やや高い','内陸のムスリム生活圏を含む。沿岸部・都市・宗教少数派、避難による人口分布の変化が大きい。',sources=['PEW2025','IRF-SYR'])
box('LBN','north','北部（トリポリ周辺）','やや高い',[35.65,34.15,36.6,34.7],'宗教構成は非常に細かく分かれる。全国ムスリム女性の調査を地域全女性の着用率には使わない。',sources=['PEW2025','IRF-LBN'],clothing=['PEW_DRESS2010'])
box('LBN','south-east','南部と東部内陸（ベカー高原）','やや高い',[35.1,33.05,36.7,34.15],'南部・東部のムスリム生活圏の概略。キリスト教徒・ドゥルーズ派などの地区が混在する。',sources=['PEW2025','IRF-LBN'],clothing=['PEW_DRESS2010'])
country('JOR','高い','アンマンなど住民の生活圏。2010年のムスリム女性調査で、いつも59%、大抵24%が頭を覆う。',clothing=['PEW_DRESS2010'])
country('SAU','高い','都市・集落の住民女性を想定する定性推定。女性旅行者に髪を覆う義務がある、という説明はしない。',sources=['PEW2025','FCDO-SAU'])
country('YEM','高い','住民女性の頭・身体を覆う服装を想定。ニカブなど顔の覆いとヒジャブを区別する。',sources=['PEW2025','IRF-YEM'])
country('OMN','高い','北東部のマスカット周辺や南部サラーラなどの生活圏。砂漠を含む国の面積は出題頻度ではない。',sources=['PEW2025','IRF-OMN'])
country('ARE','やや高い','湾岸のアブダビ・ドバイ・シャルジャなど。外国人住民や旅行者が多く、イスラム教国でも街頭の服装は多様。')
country('QAT','やや高い','東岸のドーハ周辺に人口が集中。国籍人口と全居住人口を混同しない。')
country('BHR','やや高い','マナーマ周辺など住民生活圏。外国人住民の存在も考慮する。')
country('KWT','やや高い','湾岸のクウェート市周辺。外国人住民を含む人口と自国籍住民の服装は同じではない。')
country('PSE','高い','ヨルダン川西岸・ガザのムスリム生活圏。両地域は離れている。人口移動と撮影時期の違いに注意。',sources=['PEW2025','IRF-PSE'])
box('ISR','galilee','北部（ガリラヤのアラブ系住民の町）','やや高い',[34.95,32.2,35.65,33.2],'町・宗教ごとの差が大きい。頭布だけでイスラム教・国籍・民族を判断しない。',sources=['PEW2025','IRF-ISR'])
city('ISR','negev','南部（ベエルシェバ北方のラハト周辺）',34.76,31.4,sources=['PEW2025','IRF-ISR'])
city('AZE','baku','東部バクー周辺の一部',49.87,40.40,'宗教人口は多いが未着用も多い。ムスリム多数を根拠に国全体を濃い赤にしない。',sources=['PEW2025','IRF-AZE'])
city('GEO','batumi','南西部（黒海沿岸バトゥミ周辺）',41.64,41.65,sources=['PEW2025','IRF-GEO'])
box('UZB','ferghana','東端（フェルガナ盆地）','やや高い',[70.2,40.0,73.3,41.4],'中央アジアではムスリム人口とヒジャブ着用が一致しない。東部の生活圏に限った弱い補助候補。',sources=['PEW2025','IRF-UZB'])
box('KGZ','osh','南西部（オシ周辺、フェルガナ盆地の縁）','やや高い',[71.7,39.3,74.0,41.2],'山地全域へ広げず、南西部の生活圏を候補とする。全国着用率の実測値は未取得。',sources=['PEW2025','IRF-KGZ'])

# Europe: explicit localities, light red only, and no entire diaspora countries filled.
city('ALB','tirana','中西部ティラナの一部',19.82,41.33,'ムスリム人口が多くても未着用女性が多い。市内の一部の生活圏を補助候補とする。')
city('XKX','prizren','南部プリズレン周辺',20.74,42.21,'コソボはM49の独立した国コードではないため、国連区分はセルビアの南ヨーロッパを参照。服装は多様。')
city('BIH','sarajevo','中東部サラエボ周辺',18.42,43.86,'ボシュニャク系ムスリムの生活圏。ムスリムの多さを一律の着用率とみなさない。')
city('MKD','tetovo','北西部（テトヴォ周辺）',20.97,42.01,sources=['PEW2025','IRF-MKD'])
city('SRB','novi-pazar','南西部（ノヴィ・パザル周辺）',20.52,43.14,sources=['PEW2025','IRF-SRB'])
city('MNE','ulcinj','南東部（アルバニア国境沿いのウルツィニ周辺）',19.20,41.93,sources=['PEW2025','IRF-MNE'])
box('BGR','south','南部（ギリシャ国境近くの山地・町）','やや高い',[23.4,41.35,26.0,42.1],'ロドピ山地などのムスリム生活圏。高齢女性の一般的な頭布とは区別する。',sources=['PEW2025','IRF-BGR'])
box('GRC','thrace','北東端（トルコ・ブルガリア国境寄り）','やや高い',[24.3,40.8,26.55,41.75],'西トラキアのムスリム生活圏。ギリシャ本土の他地域とは分けて覚える。',sources=['PEW2025','IRF-GRC'])
admin('RUS','caucasus','南西部（カスピ海西岸～北コーカサス東部）','高い','Chechnya|Ingush|Dagestan','チェチェン・イングーシ・ダゲスタンの生活圏。国連M49ではロシア全体が東ヨーロッパ。地域ごとに服装差がある。',sources=['PEW2025','IRF-RUS','PEW_ATTIRE'])
city('RUS','kazan','西部内陸（カザン周辺、ボルガ川中流）',49.11,55.79,'ムスリム生活圏のある別の候補。北コーカサスと同じ高い着用率は想定しない。',sources=['PEW2025','IRF-RUS'])

for iso,slug,area,lon,lat,src in [
 ('GBR','london','南東部ロンドン東部（タワーハムレッツなど）',-0.03,51.52,'ONS2021'),
 ('GBR','birmingham','中部バーミンガムの一部',-1.89,52.48,'ONS2021'),
 ('GBR','bradford','北部ブラッドフォード周辺',-1.75,53.79,'ONS2021'),
 ('GBR','blackburn','北西部ブラックバーン周辺',-2.48,53.75,'ONS2021'),
 ('FRA','paris','北部パリと周辺の一部',2.35,48.88,'INSEE2020'),
 ('FRA','marseille','南東岸マルセイユの一部',5.38,43.31,'INSEE2020'),
 ('DEU','ruhr','西部（ルール地方の都市部の一部）',7.01,51.46,'BAMF2020'),
 ('DEU','berlin','北東部ベルリンの一部',13.41,52.49,'BAMF2020'),
 ('NLD','rotterdam','西部ロッテルダムの一部',4.48,51.92,'FRA2024'),
 ('NLD','amsterdam','西部アムステルダムの一部',4.90,52.37,'FRA2024'),
 ('BEL','brussels','中部ブリュッセルの一部',4.35,50.85,'FRA2024'),
 ('SWE','malmo','最南部マルメの一部',13.00,55.61,'FRA2024'),
 ('SWE','stockholm','東岸ストックホルムの一部',18.06,59.33,'FRA2024'),
 ('DNK','copenhagen','東部コペンハーゲンの一部',12.55,55.69,'FRA2024'),
 ('AUT','vienna','東部ウィーンの一部',16.37,48.21,'FRA2024'),
 ('ITA','milan','北部ミラノの一部',9.19,45.47,'FRA2024'),
 ('ESP','barcelona','北東部バルセロナの一部',2.17,41.39,'FRA2024'),
]:
    clothing={'FRA':['INSEE2020'],'DEU':['BAMF2020']}.get(iso,[])
    city(iso,slug,area,lon,lat,sources=['PEW2025',src],clothing=clothing)
city('ESP','ceuta','アフリカ側の飛び地セウタ',-5.32,35.89,sources=['PEW2025','IRF-ESP'])
city('ESP','melilla','アフリカ側の飛び地メリリャ',-2.94,35.29,sources=['PEW2025','IRF-ESP'])

# The Americas and Oceania: symbols are local community candidates, not city rates.
city('CAN','toronto','南東部トロントの一部',-79.38,43.65,'トロント市の私的世帯人口でムスリム9.6%（2021年）。カナダの2016年調査ではムスリム女性48%がヒジャブを着用と回答。',stats=[['MANUAL','Toronto city']],sources=['STATCAN2021'],clothing=['ENVIRONICS2016'])
city('CAN','montreal','南東部モントリオールの一部',-73.57,45.50,sources=['PEW2025','STATCAN2021'],clothing=['ENVIRONICS2016'])
city('USA','detroit','北東寄りの五大湖周辺（デトロイト西郊など）',-83.18,42.32,sources=['PEW2025','PEW_US2017'],clothing=['PEW_US2017'])
city('USA','minneapolis','北部内陸ミネアポリスの一部',-93.24,44.97,sources=['PEW2025','PEW_US2017'],clothing=['PEW_US2017'])
city('USA','new-york','北東岸ニューヨークの一部',-73.95,40.72,sources=['PEW2025','PEW_US2017'],clothing=['PEW_US2017'])
city('SUR','paramaribo','北部海岸（パラマリボ周辺）',-55.20,5.83,'ムスリム生活圏のある南米の候補。国の大部分を占める内陸森林を同色にしない。')
city('GUY','georgetown','北東部海岸（ジョージタウン周辺）',-58.16,6.81)
city('TTO','chaguanas','トリニダード島の中西部（チャグアナス周辺）',-61.41,10.52)
city('AUS','sydney','南東岸シドニーの西部・南西部の一部',150.99,-33.92,'グレーター・シドニーのムスリム人口6.3%（2021年）は都市圏全体の値。着用率ではない。',stats=[['MANUAL','Greater Sydney']],sources=['ABS2021'])
city('AUS','melbourne','南東部メルボルン北部などの一部',144.96,-37.72,sources=['PEW2025','ABS2021'])
city('NZL','auckland','北島北部オークランドの一部',174.76,-36.85)
city('FJI','lautoka','ビティレブ島西部（ラウトカ周辺）',177.45,-17.61)

if __name__=='__main__':
    (ROOT/'data').mkdir(exist_ok=True)
    (ROOT/'data'/'region_definitions.json').write_text(json.dumps(REGIONS,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(REGIONS)} regions; {len({r["iso3"] for r in REGIONS})} countries/areas')
