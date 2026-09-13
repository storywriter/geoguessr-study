"""Build the Japanese study table and reusable, non-overlapping region geometry."""
from pathlib import Path
from collections import defaultdict
import csv,json,unicodedata,re
from shapely.geometry import shape,mapping,box,Point,Polygon
from shapely.ops import unary_union
from shapely import make_valid,set_precision
from catalog import REGIONS
from prepare_geography import rounded
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';OUT=ROOT/'output'

REGION_JA={'Northern Africa':'北アフリカ','Western Africa':'西アフリカ','Middle Africa':'中部アフリカ','Eastern Africa':'東アフリカ','Southern Africa':'南部アフリカ','Southern Asia':'南アジア','South-eastern Asia':'東南アジア','Eastern Asia':'東アジア','Western Asia':'西アジア','Central Asia':'中央アジア','Northern Europe':'北ヨーロッパ','Southern Europe':'南ヨーロッパ','Eastern Europe':'東ヨーロッパ','Western Europe':'西ヨーロッパ','Northern America':'北アメリカ','South America':'南アメリカ','Central America':'中央アメリカ','Caribbean':'カリブ海','Australia and New Zealand':'オーストラリア・ニュージーランド','Melanesia':'メラネシア','Micronesia':'ミクロネシア','Polynesia':'ポリネシア'}
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def table(name):return list(csv.DictReader((DATA/name).open(encoding='utf-8-sig')))

def main():
    OUT.mkdir(exist_ok=True)
    src=json.loads((DATA/'sources.json').read_text())
    world=json.loads((DATA/'basemap_countries.geojson').read_text())['features']
    adm=json.loads((DATA/'basemap_admin1.geojson').read_text())['features']
    m49={r['iso3']:r for r in table('un_m49.csv')}
    names={};geoms=defaultdict(list);codes={};lookup={}
    for f in world:
        p=f['properties'];iso=p['iso3']
        geoms[iso].append(shape(f['geometry']))
        # Several Natural Earth features can share ISO_A3_EH (e.g. France and
        # Clipperton). Prefer the country feature over a later overseas feature.
        if iso not in names or p['ADM0_A3']==iso:
            names[iso]=p['NAME_JA'] or p['ADMIN'];codes[iso]=p['ADM0_A3']
        lookup[norm(p['ADMIN'])]=iso
    for iso,r in m49.items():lookup[norm(r['name'])]=iso
    special={'Bosnia-Herzegovina':'BIH','D.R. Congo':'COD','Cape Verde':'CPV','Czech Republic':'CZE','Ivory Coast':'CIV','Kosovo':'XKX','Palestinian territories':'PSE','Republic of the Congo':'COG','Russia':'RUS','South Korea':'KOR','North Korea':'PRK','United States':'USA','Taiwan':'TWN','Tanzania':'TZA','Turkey':'TUR','Vietnam':'VNM','Iran':'IRN','Bolivia':'BOL','Venezuela':'VEN','Laos':'LAO','Moldova':'MDA','Syria':'SYR','United Kingdom':'GBR','Federated States of Micronesia':'FSM','St. Lucia':'LCA','St. Vincent and the Grenadines':'VCT','U.S. Virgin Islands':'VIR','Reunion':'REU','Curacao':'CUW'}
    special.update({'Hong Kong':'HKG','Macao':'MAC'})
    lookup.update({norm(k):v for k,v in special.items()})
    names.update({'SOM':'ソマリア','XKX':'コソボ','PSE':'パレスチナ','ESH':'西サハラ','MYT':'マヨット（フランス）','TUR':'トルコ','MKD':'北マケドニア','FRA':'フランス','AUS':'オーストラリア'})
    # Natural Earth stores some overseas territories under the sovereign state.
    if not geoms['MYT']:
        geoms['MYT']=[unary_union(geoms['FRA']).intersection(box(45,-13.1,45.4,-12.55))]
    countries={iso:make_valid(unary_union(gs)) for iso,gs in geoms.items()}
    national={};missing=[]
    nrows=table('national_religion_2010_2020.csv')
    aggregate={'World','Asia-Pacific','Europe','Latin America-Caribbean','Middle East-North Africa','North America','Sub-Saharan Africa'}
    for r in nrows:
        iso=lookup.get(norm(r['place']))
        r['iso3']=iso or ''
        if r['year']=='2020' and r['place'] not in aggregate:
            if iso:national[iso]=r
            else:missing.append(r['place'])
    # The two Channel Islands are grouped together in the demographic source.
    allowed_unmatched={'Channel Islands'}
    if set(missing)-allowed_unmatched:raise ValueError('Unmatched national names: '+repr(missing))
    with (DATA/'national_religion_2010_2020.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(nrows[0]));w.writeheader();w.writerows(nrows)
    datasets={
      'IND':{norm(r['area'].removeprefix('District - ')):r for r in table('india_religion_2011.csv')},
      'LKA':{norm(r['area']):r for r in table('sri_lanka_districts_2024.csv')},
      'MANUAL':{norm(r['area']):r for r in table('manual_statistics.csv')},
      'IDN':{re.sub(r'^\d+','',norm(r['area'])):r for r in table('indonesia_provinces_2010.csv')},
    }
    idn_alias={'Jakarta Raya':'DKI Jakarta','Yogyakarta':'DI Yogyakarta','Bangka-Belitung':'Kepulauan Bangka Belitung','Aceh':'Nanggroe Aceh Darussalam'}
    final=[];features=[];claimed={};geometry_types={'country':'国・地域全体','admin1':'行政区を束ねた概略','bbox':'緯度経度で囲った概略','polygon':'手描きの概略','point':'位置の目印（面積を持たない）'}
    for r in sorted(REGIONS,key=lambda r:0 if r['level']=='高い' else 1):
        r=json.loads(json.dumps(r));iso=r['iso3'];spec=r['geometry'];kind=spec['type'];land=countries[iso]
        # An inaccessible report may remain in the research bibliography, but
        # it must not masquerade as a read source supporting a study-table row.
        unread=[s for s in r['sources'] if s.startswith('IRF-') and src[s].get('retrieval_status')!='retrieved']
        r['sources']=[s for s in r['sources'] if s not in unread]
        if unread:r['unused_reference_links']=unread
        if kind=='country':g=land
        elif kind=='admin1':
            matches=[f for f in adm if f['properties']['adm0_a3']==codes.get(iso) and f['properties']['name'] in spec['names']]
            got={f['properties']['name'] for f in matches}
            if got!=set(spec['names']):raise ValueError((r['id'],'missing admin names',set(spec['names'])-got))
            g=unary_union([shape(f['geometry']) for f in matches]).intersection(land)
        elif kind=='bbox':g=box(*spec['bounds']).intersection(land)
        elif kind=='polygon':g=Polygon(spec['coordinates']).intersection(land)
        elif kind=='point':g=Point(spec['coordinates'])
        else:raise ValueError(spec)
        if kind!='point':
            g=make_valid(g.difference(claimed.get(iso,Polygon())))
            if g.geom_type=='GeometryCollection':g=unary_union([v for v in g.geoms if v.geom_type in ['Polygon','MultiPolygon']])
            claimed[iso]=unary_union([claimed.get(iso,Polygon()),g])
        if g.is_empty:raise ValueError('Empty region '+r['id'])
        stats=[]
        for family,key in r['statistics']:
            if norm(key) not in datasets[family]:raise ValueError((r['id'],'unknown statistic',family,key))
            stats.append(datasets[family][norm(key)])
        if iso=='IDN' and kind=='admin1':
            for name in spec['names']:
                key=norm(idn_alias.get(name,name));value=datasets['IDN'].get(key)
                if value is None:raise ValueError((r['id'],'BPS name not joined',name,list(datasets['IDN'])))
                stats.append(value)
        if r['id']=='GBR-london':stats.append(datasets['MANUAL'][norm('Tower Hamlets')])
        if r['id']=='GBR-blackburn':stats.append(datasets['MANUAL'][norm('Blackburn with Darwen')])
        for s in stats:
            if s['source_id'] not in r['sources']:r['sources'].append(s['source_id'])
        region=m49[iso if iso!='XKX' else 'SRB']['region']
        if region not in REGION_JA:raise ValueError(region)
        sources=list(dict.fromkeys(r['sources']+r['clothing_sources']+['PEW2025']))
        for s in sources:
            if s not in src:raise ValueError('Undefined source '+s)
        dress=[s for s in sources if any(t in src[s]['kind'] for t in ['服装','頭を覆う','ヒジャブ','衣服種別','ベール'])]
        survey=[s for s in dress if '調査' in src[s]['kind']]
        status='服装調査あり（地図の各範囲を直接測定したものではない）' if survey else ('服装の質的資料あり／地域の率は未取得' if dress else '宗教人口・地域分布からの弱い定性推定／着用率未取得')
        r.update(country_ja=names[iso],un_region_ja=REGION_JA[region],source_ids=sources,clothing_evidence=status,statistic_records=stats,national_muslim_percent=national.get(iso,{}).get('muslim_percent','未取得'),national_data_year=2020,geometry_kind_ja=geometry_types[kind],data_years='; '.join(sorted({src[s]['data_year'] for s in sources if s!='KOZHIKODE'})))
        if kind=='point':r['position_caveat']='地域選択と座標は編集上の学習用目印。引用資料がこの地点の着用率を測ったという意味ではない。'
        final.append(r)
        props={k:r[k] for k in ['id','iso3','country_ja','un_region_ja','area_ja','level','source_ids','clothing_evidence','geometry_kind_ja']}
        props['geometry_method']=spec
        # Snap before serialization: decimal rounding alone can turn a narrow
        # coastal inlet into a self-intersection or overlapping multipolygons.
        snapped=set_precision(g,grid_size=.00001,mode='valid_output')
        encoded=rounded(mapping(snapped))
        if not shape(encoded).is_valid:
            encoded=mapping(make_valid(shape(encoded)))
        features.append(dict(type='Feature',id=r['id'],properties=props,geometry=encoded))
    order={r['id']:i for i,r in enumerate(REGIONS)}
    final.sort(key=lambda r:order[r['id']]);features.sort(key=lambda f:order[f['id']])
    for r in final:r['map_number']=order[r['id']]+1
    for f in features:f['properties']['map_number']=order[f['id']]+1
    (DATA/'region_definitions.json').write_text(json.dumps(REGIONS,ensure_ascii=False,indent=2)+'\n')
    (DATA/'study_regions.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
    geo=dict(type='FeatureCollection',title='ヒジャブの出現率 — 定性推定',coordinate_reference_system='EPSG:4326; [longitude, latitude]',geometry_notice='概略学習範囲。宗教・服装の測定境界ではない。点は面積を持たない。',features=features)
    (DATA/'study_regions.geojson').write_text(json.dumps(geo,ensure_ascii=False,separators=(',',':'))+'\n')
    headers=['国連による世界地理区分','国名','地域名','ヒジャブの出現率','解説','地域ID','地図番号','地図の範囲','地域統計（宗教人口比率）','全国参考値（宗教人口比率・2020年）','服装の根拠','出典ID','出典URL']
    rows=[]
    for r in final:
        st=' / '.join(f'{s["area"]}: {float(s["muslim_percent"]):.2f}% ({s["year"]}年)' for s in r['statistic_records']) or '地域別数値は未取得'
        rows.append([r['un_region_ja'],r['country_ja'],r['area_ja'],r['level'],r['explanation'],r['id'],str(r['map_number']).zfill(3),r['geometry_kind_ja'],st,r['national_muslim_percent']+'%',r['clothing_evidence'],'; '.join(r['source_ids']),'; '.join(src[s]['url'] for s in r['source_ids'])])
    with (OUT/'ヒジャブの出現率.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)
    (DATA/'csv_matrix.json').write_text(json.dumps([headers]+rows,ensure_ascii=False,separators=(',',':'))+'\n')
    coverage=[]
    for iso,m in m49.items():
        region_count=sum(r['iso3']==iso for r in final)
        coverage.append(dict(iso3=iso,country_en=m['name'],selected_regions=region_count,national_percent=national.get(iso,{}).get('muslim_percent',''),status='掲載' if region_count else '未掲載（低頻度の証明ではない）'))
    with (DATA/'country_coverage.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(coverage[0]));w.writeheader();w.writerows(coverage)
    print(json.dumps({'regions':len(final),'countries_and_areas':len({r['iso3'] for r in final}),'polygons':sum(f['geometry']['type']!='Point' for f in features),'points':sum(f['geometry']['type']=='Point' for f in features)},ensure_ascii=False))

if __name__=='__main__':main()
