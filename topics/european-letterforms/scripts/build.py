"""Build attributed CSV, clipped WGS84 geometry and reproducible page assignments."""
from pathlib import Path
import copy,csv,hashlib,json,math,sys,unicodedata
from shapely.geometry import shape,mapping,box,Point
from shapely.ops import unary_union
from shapely import make_valid,set_precision
from catalog import COUNTRIES,REGIONS,VIEWS
from languages import LANGUAGES,ALIASES,OMNI_PAGES
from sources import SOURCES,STATISTICS

TOPIC=Path(__file__).resolve().parents[1];ROOT=TOPIC.parents[1];DATA=TOPIC/'data';OUT=TOPIC/'output'
REGION_JA={'Northern Europe':'北ヨーロッパ','Western Europe':'西ヨーロッパ','Eastern Europe':'東ヨーロッパ','Southern Europe':'南ヨーロッパ','Western Asia':'西アジア'}
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def csvwrite(path,headers,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,lineterminator='\r\n');w.writerow(headers);w.writerows(rows)

def country_geometries(world,admin1):
    result={}
    for iso in COUNTRIES:
        selected=[shape(f['geometry']) for f in world if f['properties']['ISO_A3_EH']==iso and f['properties']['ADM0_A3']==iso]
        if not selected:selected=[shape(f['geometry']) for f in world if f['properties']['iso3']==iso]
        # NE stores Svalbard and Jan Mayen under Norway. A statistical-area split
        # here leaves the shared Natural Earth files untouched.
        islands=unary_union([box(10,74,40,84),box(-10,70.7,-7,72)])
        if iso=='SJM':selected=[shape(f['geometry']).intersection(islands) for f in world if f['properties']['ADM0_A3']=='NOR']
        if not selected:raise ValueError(f'Missing country geometry: {iso}')
        g=make_valid(unary_union(selected))
        if iso=='NOR':g=g.difference(islands)
        if iso in ('FRA','NLD','DNK','GBR'):g=g.intersection(box(-26,34,36,72))
        if iso in ('ESP','PRT'):g=g.intersection(box(-32,27,6,45))
        result[iso]=g
    crimea=unary_union([shape(f['geometry']) for f in admin1 if f['properties']['adm0_a3']=='RUS' and f['properties']['name'] in ('Crimea','Sevastopol')])
    result['UKR']=make_valid(result['UKR'].union(crimea))
    result['RUS']=make_valid(result['RUS'].difference(crimea))
    north=unary_union([shape(f['geometry']) for f in world if f['properties']['ADM0_A3']=='CYN'])
    result['CYP']=result['CYP'].union(north)
    return result

def geometry(r,countries,world,admin1):
    spec=r['geometry_spec'];country=countries[r['iso3']];typ=spec['type']
    if typ=='point':
        g=Point(*spec['coordinates'])
        if g.distance(country)>.12:raise ValueError(f'Point outside country: {r["id"]} {g}')
        return g
    if typ=='country':
        if 'adm0' in spec:g=unary_union([shape(f['geometry']) for f in world if f['properties']['ADM0_A3'] in spec['adm0']])
        else:g=country
    elif typ=='bbox':g=country.intersection(box(*spec['bounds']))
    elif typ=='admin1':
        candidates=[f for f in admin1 if f['properties']['adm0_a3']==r['iso3'] and f['properties']['name'] in spec['names']]
        missing=set(spec['names'])-{f['properties']['name'] for f in candidates}
        if missing:raise ValueError(f'Unknown admin1 for {r["id"]}: {missing}')
        g=unary_union([make_valid(shape(f['geometry'])) for f in candidates]).intersection(country)
    else:raise ValueError(spec)
    g=set_precision(make_valid(g),.00001,mode='valid_output')
    if g.is_empty or not g.is_valid:raise ValueError(f'Invalid geometry: {r["id"]}')
    return g

STATUS_OVERRIDES={
 ('GBR','en'):'全国の事実上の共通語・主要公共表示',('FRO','da'):'デンマーク管轄機関などの行政用語',
 ('MCO','mco'):'旧市街などの一部街路名併記',('VAT','la'):'教皇庁の公式用途・銘文',
 ('JEY','fr'):'歴史的地名・街路名',('JEY','nrf_JE'):'地域言語の街路名・公共表示',
 ('GGY','fr'):'歴史的地名・街路名',('GGY','nrf_GG'):'地域言語の地名・文化表示',
 ('IMN','gv'):'地域言語の地名・公共表示',('LUX','lb'):'国語・行政での使用',
 ('LUX','fr'):'立法・行政での使用',('LUX','de'):'行政での使用',
 ('GBR','cy'):'ウェールズの公用語・英語との併記',
 ('GBR','gd'):'スコットランドの公用語・一部道路等に併記',
 ('NLD','fy'):'フリースラント州の公用語・地名併記',
 **{('BEL',l):'言語地域に応じた公用語・公共表示' for l in ['nl','fr','de']},
 **{('CHE',l):'地域・州に応じた公用語・公共表示' for l in ['de_CH','fr','it','rm']},
 **{('ESP',l):'指定地域の共同公用語・地名表記' for l in ['ca','eu','gl','oc']},
 **{('ITA',l):'指定地域の共同公用語・地名併記' for l in ['de','fr']},
 **{('SVN',l):'指定地域の共同公用語・地名併記' for l in ['it','hu']},
 **{('MKD',l):'自治体公用語・地域の公共表示' for l in ['tr','rom']},
 **{('MNE',l):'憲法上の公的使用（自治体・住民集落による）' for l in ['sr','bs','hr','sq']}}

def main():
    DATA.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
    world=json.loads((ROOT/'data/basemap_countries.geojson').read_text())['features']
    admin1=json.loads((ROOT/'data/basemap_admin1.geojson').read_text())['features']
    m49={r['iso3']:r for r in csv.DictReader((ROOT/'data/un_m49.csv').open())}
    expected={r['iso3'] for r in m49.values() if 'Europe' in r['region']}|{'ARM','AZE','GEO','CYP','XKX'}
    assert set(COUNTRIES)==expected,(set(COUNTRIES)^expected)
    countries=country_geometries(world,admin1)
    regions=copy.deepcopy(REGIONS);features=[];occurrences=[]
    # Page order is geographic, independent of dictionary/alphabetical sorting.
    ordered=[r for group in VIEWS for r in regions if r['group']==group]
    for number,r in enumerate(ordered,1):
        r['number']=number
        r['un_region_ja']=REGION_JA[m49[r['iso3']]['region']] if r['iso3'] in m49 else '南ヨーロッパ（学習用の別掲）'
        g=geometry(r,countries,world,admin1);anchor=g if g.geom_type=='Point' else g.representative_point()
        r['anchor_lonlat']=[round(anchor.x,5),round(anchor.y,5)]
        r['bbox']=list(g.bounds);r['geometry_note_ja']={'country':'国・地域の外形','admin1':'行政区を使った位置の概略','bbox':'国の外形で切り取った概略範囲','point':'代表地点。周辺全体を意味しない'}[r['geometry_spec']['type']]
        assert set(r['sources'])<=SOURCES.keys(),r
        features.append(dict(type='Feature',id=r['id'],properties={k:v for k,v in r.items() if k!='geometry_spec'},geometry=mapping(g)))
        for lang in r['languages']:
            occurrences.append(dict(id=r['id']+':'+lang,region_id=r['id'],language_id=lang))
    pages=[]
    for group,extent in VIEWS.items():
        rs=[r for r in ordered if r['group']==group];entries=[o for r in rs for o in occurrences if o['region_id']==r['id']]
        count=math.ceil(len(entries)/7)
        for part in range(count):
            # Balanced chunks avoid an almost empty last page (e.g. 7+7+1).
            batch=entries[(part*len(entries))//count:((part+1)*len(entries))//count]
            p=dict(number=len(pages)+3,title=group+(f' {part+1}/{count}' if count>1 else ''),group=group,extent=list(extent),occurrence_ids=[o['id'] for o in batch],region_ids=list(dict.fromkeys(o['region_id'] for o in batch)))
            for o in batch:o['page']=p['number']
            pages.append(p)
    lookup={r['id']:r for r in ordered}
    cldr=json.loads((DATA/'cldr_characters.json').read_text())['locales']
    headers=['国連による世界地理区分','国・地域名','国内の大まかな地域','言語の日本語名','文字体系','特徴となる文字形','冠詞・前置詞等／短い看板語','見分け方・混同注意','公的地位・看板での扱い','地域の解説','地図番号','地図帳ページ','地域ID','言語ID','経度','緯度','範囲の性質','統計ID','参照資料ID','地域・制度の出典URL','文字の出典URL','大文字形（機械的な対応・例外は解説）']
    rows=[]
    for o in occurrences:
        r=lookup[o['region_id']];l=LANGUAGES[o['language_id']];loc=ALIASES.get(l['id'],l['id'])
        if loc in ('nb','nn'):loc='no' if not cldr.get(loc,{}).get('main') or cldr.get(loc,{}).get('main')=='↑↑↑' else loc
        charurl=cldr[loc]['source_url'] if loc in cldr and cldr[loc].get('main') not in (None,'↑↑↑') else ('https://www.omniglot.com/writing/'+OMNI_PAGES[l['id']]+'.htm' if l['id'] in OMNI_PAGES else SOURCES[r['sources'][0]]['url'])
        if l['id']=='kum':charurl='https://www.omniglot.com/writing/kumyk.php'
        if l['id']=='fkv':charurl=SOURCES['NOR']['url']
        if l['id']=='fit':charurl=SOURCES['SWE']['url']
        if l['id']=='cnr':charurl=SOURCES['MNE']['url']
        # Country statistics attach to the basic entry only. A country-wide value
        # must never silently become a percentage for a small regional locator.
        stats=[s['id'] for s in STATISTICS if (s['id'] in r['statistics'] or (r['kind']=='national' and s['iso3']==r['iso3'] and ('全国' in s['area_ja'] or s['area_ja']=='国勢調査対象地域'))) and (s['language_id']==l['id'] or (s['id']=='fin-se' and l['id'] in ('se','smn','sms')))]
        row=[r['un_region_ja'],r['country_ja'],r['area_ja'],l['name_ja'],l['script'],l['glyphs'],l['words'],l['contrast'],STATUS_OVERRIDES.get((r['iso3'],l['id']),r['status_ja']),r['note_ja'],str(r['number']),str(o['page']),r['id'],l['id'],str(r['anchor_lonlat'][0]),str(r['anchor_lonlat'][1]),r['geometry_note_ja'],'; '.join(stats),'; '.join(r['sources']),'; '.join(SOURCES[s]['url'] for s in r['sources']),charurl]
        row.append(l['glyphs'].upper())
        rows.append(row);o['statistic_ids']=stats;o['orthography_url']=charurl
    csvwrite(OUT/'ヨーロッパ周辺の特徴的な文字形.csv',headers,rows)
    dump(DATA/'csv_matrix.json',[headers,*rows]);dump(DATA/'regions.json',ordered)
    dump(DATA/'language_profiles.json',list(LANGUAGES.values()));dump(DATA/'occurrences.json',occurrences)
    dump(DATA/'study_regions.geojson',dict(type='FeatureCollection',name='European letterforms study locators',features=features))
    dump(DATA/'page_definitions.json',pages);dump(DATA/'sources.json',list(SOURCES.values()))
    chars=sorted({c for l in LANGUAGES.values() for c in l['glyphs']+l['glyphs'].upper() if c.isalpha()},key=ord)
    dump(DATA/'unicode_characters.json',[dict(character=c,codepoint=f'U+{ord(c):04X}',name=unicodedata.name(c),uppercase=c.upper(),lowercase=c.lower()) for c in chars])
    dump(DATA/'country_shapes.geojson',dict(type='FeatureCollection',features=[dict(type='Feature',id=iso,properties=COUNTRIES[iso],geometry=mapping(set_precision(g,.00001))) for iso,g in countries.items()]))
    sh=list(STATISTICS[0]);csvwrite(DATA/'statistics.csv',sh,[[s[h] for h in sh] for s in STATISTICS])
    csvwrite(DATA/'country_coverage.csv',['iso3','国・地域名','地域数','言語表記数','統計値数'],[[iso,c['name_ja'],sum(r['iso3']==iso for r in regions),len({l for r in regions if r['iso3']==iso for l in r['languages']}),sum(s['iso3']==iso for s in STATISTICS)] for iso,c in COUNTRIES.items()])
    docs=TOPIC/'docs';docs.mkdir(exist_ok=True)
    text=['# 出典台帳','',f'確認日：2026-09-13。制度・地名資料と人口統計は用途を分けています。全{len(SOURCES)}資料。','', '各行の出典はCSVの資料IDと対応します。生データの転載ではなく、必要な事実と数値の転記・学習用の再構成です。','']
    for sid,s in SOURCES.items():text.extend([f'## {sid}',f"{s['publisher']} / {s['date']}。[{s['title']}]({s['url']})。確認：{s['accessed']}。",''])
    text.extend(['## 言語ごとの文字資料','', 'Unicodeは文字集合・接続表現の根拠。地域の表記差や短い道路語は、各行の地名資料・解説も併用しています。Omniglotは補助的な二次資料です。','', '| 言語・表記 | 文字資料 |','|---|---|'])
    for lang in LANGUAGES:
        urls=sorted({o['orthography_url'] for o in occurrences if o['language_id']==lang})
        text.append('| '+LANGUAGES[lang]['name_ja']+' | '+ ' / '.join(f'[資料{i+1}]({url})' for i,url in enumerate(urls))+' |')
    text.extend(['## 文字データと原資料の保存','', 'Unicode CLDR 48.2 の取得先・commit・SHA-256は `data/reference_manifest.json`、実際の文字集合は `data/cldr_characters.json`。未収録言語の404も記録しています。CLDRの継承記号を実際の文字集合として扱いません。', '', '人口統計は `data/statistics.csv` に指標・対象年・分母・出典ID付きで転記。未取得の数値は0ではなく欠測です。看板の使用率やGeoGuessrの出題率へ換算していません。',''])
    (docs/'SOURCES.md').write_text('\n'.join(text))
    print(f'{len(COUNTRIES)} countries/areas; {len(regions)} locators; {len(rows)} CSV rows; {len(pages)+2} planned pages; {len(STATISTICS)} statistics.')

if __name__=='__main__':main()
