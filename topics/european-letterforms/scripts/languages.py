"""Reviewed visual cues, not exhaustive alphabets or country-identification rules."""

# id | Japanese name | script | characteristic fragments | short words | caution/comparison
PROFILE_TEXT = '''
en|英語|Latin|th sh wh|the / of / road|基本26字だけでは他のラテン文字言語と区別しにくい。英語の案内は各国にある。
cy|ウェールズ語|Latin|ŵ ŷ ll dd ff|y / yr / a|ll・dd・ffとw/yの多い地名が手掛かり。wだけでは判定しない。
ga|アイルランド語|Latin|á é í ó ú|an / na / agus|母音の右上がりのアクセント。スコットランド・ゲール語のà・èと比較。
gd|スコットランド・ゲール語|Latin|à è ì ò ù|an / na / agus|母音の左上がりのアクセント。アイルランド語と文字列を共有する。
kw|コーンウォール語|Latin|yw dh ow|an / ha / Kernow|固有の追加文字より、Kernow・Kernow a'gas dynnerghなどを補助にする。
sco|スコッツ語|Latin|ae aa oo|aye / o / brae|英語に近い綴り。英語と同じ看板も多く、文字だけでは断定できない。
gv|マン島語|Latin|çh yn oo|yn / ny / as|çhとynが補助になる。通常の英語標識も多い。
fr|フランス語|Latin|ç œ é è ê|le / la / de / rue|çは他言語にもある。rue・du・desと合わせる。
nl|オランダ語|Latin|ij IJ aa ee|de / het / van / straat|ijと長母音の重ね書き。deだけではロマンス諸語と区別できない。
fy|西フリジア語|Latin|â ê ô û|de / it / fan|Fryslânなどの曲折アクセント。オランダ語との併記が補助。
de|ドイツ語|Latin|ä ö ü ß|der / die / und / Straße|ßが有力。大文字ではSSも使う。スイス・リヒテンシュタインでは通常ss。
de_CH|ドイツ語（スイス式）|Latin|ä ö ü ss|der / die / und / Strasse|通常ßを使わない。ssだけではスイスの証拠にはならない。
lb|ルクセンブルク語|Latin|ë ä é|d' / an / Lëtzebuerg|ëが目立つがアルバニア語にもある。ドイツ語・フランス語との混在を見る。
is|アイスランド語|Latin|þ ð æ ö|og / á / í|þとðの組合せが強い手掛かり。þの大文字はÞ。
fo|フェロー語|Latin|ð ø æ|og / í / á|ðとøの併存。アイスランド語は通常øを使わず、デンマーク語はðを使わない。
da|デンマーク語|Latin|æ ø å|og / af / vej|文字はノルウェー語とほぼ共通。vejなどを補助にする。
nb|ノルウェー語（ブークモール）|Latin|æ ø å|og / av / vei|デンマーク語と同じ追加3字。vei/vegの揺れだけで国を決めない。
nn|ノルウェー語（ニーノシュク）|Latin|æ ø å|og / ikkje / veg|ブークモールと文字集合を共有。西部の地名・公共表示の補助。
sv|スウェーデン語|Latin|å ä ö|och / av / väg|ochがデンマーク語・ノルウェー語のogとの比較に役立つ。
fi|フィンランド語|Latin|ä ö aa ii kk|ja / tie / katu|二重母音・二重子音、tie/katu。åはアルファベットにあるが借用語・スウェーデン系名中心。
se|北サーミ語|Latin|č đ ŋ š ŧ ž|ja / geaidnu|追加子音が多い。ノルウェー・スウェーデン・フィンランドにまたがる。
smj|ルレ・サーミ語|Latin|á å ń|ja / várre|北サーミ語とは字形を共有する。国境を越える言語。
sma|南サーミ語|Latin|å ä ö|jïh / vaerie|jïhやvaerieが補助。スウェーデン語と似た母音だけでは分けられない。
smn|イナリ・サーミ語|Latin|â č đ ŋ|já / Aanaar|âと追加子音の組合せ。イナリ周辺の多言語表示を確認。
sms|スコルト・サーミ語|Latin|ǩ ǧ ǥ ʒ ǯ|da / Sääʹm|k/gのカロンとʒ系が目立つ。資料・フォントによる表示差に注意。
fkv|クヴェン語|Latin|ä ö đ aa|ja / joki / järvi|フィンランド語に非常に近い。北ノルウェーでの併記が位置の手掛かり。
fit|メアンキエリ|Latin|ä ö aa|ja / Tornionlaakso|フィンランド語と字形を共有。スウェーデン北東部の併記で絞る。
et|エストニア語|Latin|õ ä ö ü|ja / tee / tänav|õとä・ö・üの組合せ。õ単独ならポルトガル語なども候補。
lv|ラトビア語|Latin|ā ē ī ū ģ ķ ļ ņ|un / iela|長音符と下付きの記号が特徴。ģの記号は小文字で上に見える。
lt|リトアニア語|Latin|ė ą ę į ų ū|ir / gatvė|点付きėと母音の下の尾。ラトビア語のā・ēとは異なる。
pl|ポーランド語|Latin|ł ą ę ś ź ż|i / w / ulica|łと鼻母音のą・ę、sz/cz/rz。ŁはLに斜線。
csb|カシューブ語|Latin|ã ë ò ô ù|ë / Kaszëbë|ポーランド語にないã・ë・òが補助。北部の併記地名に注目。
cs|チェコ語|Latin|ř ě ů|a / v / ulice|řとůが有力。スロバキア語のľ・ôと比較する。
sk|スロバキア語|Latin|ľ ĺ ŕ ô ä|a / v / ulica|ľは書体によってlの右の小さな印。チェコ語のřは通常ない。
hu|ハンガリー語|Latin|ő ű sz gy|és / az / utca|二重鋭アクセントő・űが強い手掛かり。ö・üとは別字。
ro|ルーマニア語|Latin|ă â î ș ț|și / de / strada|ș・țは下付きコンマ。旧字体・古いデータではş・ţが混在する。
sq|アルバニア語|Latin|ë ç sh xh|dhe / në / rruga|ëとq/xh/rrなどの組合せ。アルバニアのほかコソボ・北マケドニアなど。
sl|スロベニア語|Latin|č š ž|in / na / cesta|通常の固有語にć・đを使わないが、外国人名では見られる。
hr|クロアチア語|Latin|č ć đ š ž|i / u / ulica|ボスニア語・セルビア語ラテン表記と同じ字形。単独では国を分けられない。
bs|ボスニア語|Latin|č ć đ š ž|i / u / ulica|クロアチア語・セルビア語ラテン表記と共有。キリル表記もある。
sr|セルビア語|Cyrillic|ј љ њ ћ ђ џ|и / у / улица|ј・љ・њは北マケドニアとも共有。ћ・ђとќ・ѓを比較する。
sr_Latn|セルビア語（ラテン表記）|Latin|č ć đ š ž|i / u / ulica|キリル文字と併用。クロアチア語・ボスニア語と字形だけでは分けられない。
cnr|モンテネグロ語|Latin|ś ź č ć đ|i / u / ulica|ś・źは特徴だが看板で常に出るわけではない。キリル表記も使う。
mk|マケドニア語|Cyrillic|ј љ њ ќ ѓ ѕ|и / во / улица|ќ・ѓ・ѕが強い補助。セルビア語のћ・ђと形を比べる。
bg|ブルガリア語|Cyrillic|ъ щ ѝ|и / на / улица|語中のъが目立つ。ロシア語にもъはあるので単独では断定しない。
ru|ロシア語|Cyrillic|ы э ё ъ|и / в / улица|ы・эはベラルーシ語やロシア内の諸語も共有。ёの点が省かれる例もある。
uk|ウクライナ語|Cyrillic|і ї є ґ|і / та / вулиця|ї・єが有力。іだけではベラルーシ語やラテン文字と区別できない。
be|ベラルーシ語|Cyrillic|ў і ы э|і / у / вуліца|短いuのўが有力。ロシア語との併記・混在が多い。
rue|ルシン語・レムコ語|Cyrillic|і ї ы|і / на|ウクライナ語やベラルーシ語と文字を共有。地域により正書法が異なる。
el|ギリシャ語|Greek|Θ θ Λ λ Ξ ξ Ω ω|και / η / οδός|独立したギリシャ文字。キプロスでも使う。ΡはラテンPに似る。
mt|マルタ語|Latin|ċ ġ ħ ż għ|il- / tal- / triq|ħと点付きċ・ġ・żが有力。英語の併記もよく使われる。
it|イタリア語|Latin|à è é ì ò ù|il / della / via|固有の追加文字は乏しい。via・piazza・gliなどの語を補助にする。
lld|ラディン語|Latin|ë é ć|y / de|北イタリアの谷ごとに綴りが違う。ドイツ語・イタリア語との併記を見る。
fur|フリウリ語|Latin|â ê î ô û ç|e / di / cj|長母音の曲折アクセントとcj。北東イタリアの地名併記に注目。
sc|サルデーニャ語|Latin|dd tz|su / sa / de|su・saが補助。島内の地域差があり、イタリア語と共有する綴りも多い。
rm|ロマンシュ語|Latin|sch tg|il / la / e|sch・tgとロマンス系の語の組合せ。スイス南東部の一部で使う。
ca|カタルーニャ語（バレンシア語を含む）|Latin|l·l ç ny à|el / els / de / carrer|中点付きl·lが強い手掛かり。nyはスペイン語のñと比較。
es|スペイン語|Latin|ñ ¿ ¡|el / la / de / calle|ñはガリシア語などにもある。¿・¡は短い地名標識には出ないことが多い。
pt|ポルトガル語|Latin|ã õ ç nh lh|o / a / do / rua|ã・õとnh・lhの組合せ。スペイン語のñと比較する。
gl|ガリシア語|Latin|ñ nh x|o / a / e / rúa|ñとポルトガル語に似た冠詞。通常ã・õを標準正書法に使わない。
eu|バスク語|Latin|tx tz k|eta / -ko / -ak|tx・tz・kの組合せが補助。スペイン側・フランス側にまたがる。
oc|オック語（アラン語を含む）|Latin|ò è ç nh lh|lo / la / e|nh・lhはポルトガル語とも共通。フランス南部、スペインのアラン谷。
ast|アストゥリアス語|Latin|ḷ ḥ ñ|y / el / la|ḷḷ・ḥは一部方言の綴り。これらがない看板も多い。
an|アラゴン語|Latin|ch ll|o / a / y|固有の追加文字は乏しい。スペイン語・カタルーニャ語と混同しやすい。
mwl|ミランダ語|Latin|lh nh ç|l / la / i|lh・nhをポルトガル語と共有。ポルトガル北東端の地名が補助。
br|ブルトン語|Latin|c'h ñ|ar / an / ha|c'hが有力。フランス北西部のフランス語との併記を見る。
co|コルシカ語|Latin|chj ghj ù|u / a / è|chj・ghjがイタリア語との差の補助。地名だけでは似る場合が多い。
gsw|アルザス語・アレマン系地域表記|Latin|ä ö ü sch|d' / uf|ドイツ語・スイスドイツ語と文字を共有。フランス語との併記が位置の手掛かり。
hsb|上ソルブ語|Latin|ć č ě ł ń ř š ž|a / w|řとłの併存が補助。ドイツ東部のバウツェン周辺。
dsb|下ソルブ語|Latin|ć č ě ł ń ŕ ś ź ž|a / w|ŕ・ś・źとł。上ソルブ語との区別は複数の字を見る。
nds|低地ドイツ語|Latin|ä ö ü aa|de / dat / un|標準ドイツ語に近い。地名の別表記が補助で、全国的な識別字はない。
frr|北フリジア語|Latin|ä ö ü å|di / e|地域ごとに正書法が異なる。ドイツ語との併記と海岸の位置を見る。
stq|ザーターフリジア語|Latin|ä ö ü|di / dät|文字だけではドイツ語と分けにくい。Seelterloundなどの地域名が補助。
hy|アルメニア語|Armenian|ա ե մ ն ս և|և / ի|独立したアルメニア文字。日本語の山などに似て見える字が連続する。
ka|ジョージア語|Georgian|ა ბ გ დ ლ მ|და / ქუჩა|丸い輪・曲線の多い独立文字。大文字様のムタヴルリも同じ言語。
az|アゼルバイジャン語|Latin|ə ı İ ğ ş ç|və / üçün|əがトルコ語との比較に有力。ıとi、Iとİを区別する。
tr|トルコ語|Latin|ı İ ğ ş ç ö ü|ve / bir / sokak|iとı、İとIが別。アゼルバイジャン語のəは標準トルコ語にはない。
gag|ガガウズ語|Latin|ä ê ı ţ|hem / bir|トルコ語に似るがä・êが補助。モルドバ南部ではロシア語も広く使う。
ab|アブハズ語|Cyrillic|ә ҩ ҿ ҧ|Аҟәа|追加キリル字が多い。ジョージア文字とは別。ロシア語も使われる。
os|オセット語|Cyrillic|Ӕ ӕ|ӕмӕ|キリルのӕはラテンのæに似る。ロシア語と併記されることがある。
tt|タタール語|Cyrillic|ә ө ү җ ң һ|һәм / урамы|追加6字が補助。バシキール語と共通するが、ҙ・ҫは通常使わない。
ba|バシキール語|Cyrillic|ә ө ү ғ ҡ ҙ ҫ|һәм|タタール語との比較ではҙ・ҫ・ҡ・ғが補助。
cv|チュヴァシ語|Cyrillic|ӑ ӗ ҫ ӳ|тата|母音上の短音符ӑ・ӗとӳが特徴。
udm|ウドムルト語|Cyrillic|ӝ ӟ ӥ ӧ ӵ|но|子音上の2点ӝ・ӟ・ӵが特徴。
kv|コミ語|Cyrillic|ӧ і|да|ロシア語にないӧ・іが補助。単独では他のロシア内の言語とも重なる。
mhr|草原マリ語|Cyrillic|ҥ ӧ ӱ|да|ロシア語にない追加字。山地マリ語と共有する。
mrj|山地マリ語|Cyrillic|ӓ ӹ ӧ ӱ|да|ӓ・ӹが草原マリ語との比較に役立つ。
myv|エルジャ語|Cyrillic|я ё ь|ды|基本的にロシア語と同じ字。短い語とモルドヴィアの位置が必要。
mdf|モクシャ語|Cyrillic|я ё ь|ди|ロシア語・エルジャ語と同じ字形が多く、単字では分けられない。
ce|チェチェン語|Cyrillic|Ӏ гӀ кӀ|а / нохчийн|縦棒ӀはラテンIや数字1に似る。北コーカサスの他言語も使う。
inh|イングーシ語|Cyrillic|Ӏ гӀ кӀ|гӀалгӀай|縦棒をチェチェン語などと共有。字形だけで両者を分けない。
ady|アディゲ語|Cyrillic|Ӏ кӀ гъ|адыгэ|縦棒・硬音符を伴う複数字。カバルド語と似る。
kbd|カバルド語|Cyrillic|Ӏ къ гъ|къэбэрдей|アディゲ語と近い字形。単独では北コーカサスまでの絞り込みに留める。
krc|カラチャイ・バルカル語|Cyrillic|къ гъ нг|эм|基本ロシア文字の組合せを拡張。地域・綴りで表記差がある。
abq|アバザ語|Cyrillic|Ӏ гъ къ|абаза|北コーカサスの他言語と同じ複数字が多い。
nog|ノガイ語|Cyrillic|аь оь уь нъ|ногай|母音にьを続ける綴りが補助。チェチェン語などとの重複もある。
xal|カルムイク語|Cyrillic|ә ө ү җ ң һ|хальмг|タタール語と追加字を共有。カスピ海北西の位置と併せる。
sah|サハ語（ヤクート語）|Cyrillic|ҕ ҥ ө һ ү|уонна|ҕとҥが目立つ。モンゴル系のө・үだけでは分けられない。
bua|ブリヤート語|Cyrillic|ү ө һ|ба|モンゴル語に近い字形。バイカル湖東側のロシア語併記が補助。
tyv|トゥヴァ語|Cyrillic|ң ө ү|биле|追加3字を周辺の言語と共有。モンゴル国境北側が主な範囲。
alt|アルタイ語|Cyrillic|ҥ ӧ ӱ|алтай|ӧ・ӱに似たラテン文字の代用もある。コードポイントの違いは肉眼では分けにくい。
kjh|ハカス語|Cyrillic|ғ і ң ӧ ӱ|хакас|іとӧ・ӱなどの組合せ。ロシア語単独とは追加字で比較する。
av|アヴァル語|Cyrillic|Ӏ гъ къ|авар|複数字と縦棒。ダゲスタン内の他言語とも共通する。
dar|ダルギン語|Cyrillic|Ӏ гъ хӀ|дарган|地域内に言語差があり、字形だけでは他のダゲスタン諸語と分けにくい。
kum|クムク語|Cyrillic|гъ къ нг|къумукъ|追加の単字より複数字が補助。カラチャイ・バルカル語などと似る。
lez|レズギ語|Cyrillic|Ӏ гъ кь|лезги|縦棒・ъ・ьを伴う子音。ダゲスタン南部とアゼルバイジャン北部。
lak|ラク語|Cyrillic|Ӏ къ гъ|лакку|他のダゲスタン諸語と字形を共有するため、地域候補用。
tab|タバサラン語|Cyrillic|Ӏ гъ хъ|табасаран|複数字が多い。レズギ語などとの一意な識別字ではない。
agx|アグール語|Cyrillic|Ӏ гъ гь|агъул|ъ・ьを続ける複数字が補助。他のダゲスタン諸語とも共有。
rut|ルトゥル語|Cyrillic|Ӏ гъ уь||母音＋ь、縦棒など。他のダゲスタン諸語との判別力は弱い。
tkr|ツァフル語|Cyrillic|Ӏ къ уь||複数字を他のダゲスタン諸語と共有する。
jdt|タート語（ジュフリの表記）|Cyrillic|гъ гь уь||ダゲスタンのキリル表記。アゼルバイジャン側のタート語表記へ一般化しない。
rom|ロマニ語|Latin|č š ž|romani|正書法が複数ある。北マケドニアの自治体表示はマケドニア語と併せて読む。
la|ラテン語|Latin|AE QV V|et / in / de|古典的な銘文ではUの位置にVが現れる。普通の道路標識の主言語とは別。
mco|モネガスク語|Latin|ü ë œ|u / a|モナコ旧市街のフランス語との併記が補助。
frp|フランコプロヴァンス語|Latin|â ê ô|lo / la|地域ごとに正書法が異なる。フランス語・オック語と同じ字形を共有。
nrf_JE|ジャージー語（ジェリエー）|Latin|ê î û ç|la / l' / rue|フランス語と似たノルマン語の島嶼方言。道路名と英語の併用が補助。
nrf_GG|ガーンジー語（ガーンジア）|Latin|â ê î ô û|la / lé|ノルマン語の島嶼方言。地名はフランス語に似ており字形単独で島を分けない。
cnr_Cyrl|モンテネグロ語（キリル表記）|Cyrillic|ј љ њ ћ ђ|и / у / улица|セルビア語と大部分を共有。特徴字с́・з́は少なく、見えないことを除外理由にしない。
az_Cyrl|アゼルバイジャン語（キリル表記）|Cyrillic|ә ө ү ғ ҝ|вә|ダゲスタンなどのキリル表記用。アゼルバイジャン本国の現行ラテン表記と区別。
rsk|パンノニア・ルシン語|Cyrillic|ї є ґ|и / на|セルビア北部などの変種。カルパチアのルシン諸変種と区別して登録。
ro_Cyrl|モルドバ語（キリル表記）|Cyrillic|ы э ж|ши / де|ルーマニア語に対応する言語のキリル表記。沿ドニエストルの公的表示に限った補助。
sju|ウメ・サーミ語|Latin|á đ ï ŋ ü|Ubbme|他のサーミ諸語と字形を共有。スウェーデン北中部の地名に注目。
rup|アルーマニア語（ヴラフ語）|Latin|ã sh ts|shi / Crushuva|ルーマニア語に近い。ãとshは近年の正書法の補助で、綴りは地域によって異なる。
'''

LANGUAGES={}
for line in PROFILE_TEXT.strip().splitlines():
    code,name,script,glyphs,words,contrast=line.split('|')
    LANGUAGES[code]=dict(id=code,name_ja=name,script=script,glyphs=glyphs,words=words,contrast=contrast)

ALIASES={'de_CH':'de','csb':'csb','cnr':'sr_Latn','rom':'rom','fkv':'fi','fit':'fi','gsw':'gsw'}

# Exact supplementary alphabet pages; never use the index as support for a
# language-specific claim. Primary topographic sources remain in every CSV row.
OMNI_PAGES={
 'gag':'gagauz','os':'ossetian','mco':'monegasque','frp':'francoprovencal','mwl':'mirandese',
 'csb':'kashubian','rue':'rusyn','rsk':'rusyn','cnr_Cyrl':'montenegrin','sco':'scots',
 'nrf_JE':'jerriais','nrf_GG':'guernesiais','stq':'frisian','sju':'umesami',
 'kv':'komi','udm':'udmurt','mhr':'mari','mrj':'mari','ady':'adyghe','kbd':'kabardian',
 'krc':'balkar','abq':'abaza','inh':'ingush','nog':'nogai','xal':'kalmyk',
 'alt':'altay','kjh':'khakas','av':'avar','dar':'dargwa','kum':'kumyk','lez':'lezgi',
 'lak':'lak','tab':'tabassaran','agx':'aghul','rut':'rutul','tkr':'tsakhur','jdt':'juhuri',
 'ro_Cyrl':'moldovan','rom':'romani','la':'latin','rup':'aromanian'}
