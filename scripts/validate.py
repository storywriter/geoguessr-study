"""Check statistical denominators, source joins, geometry and deliverable agreement."""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,hashlib,re,itertools
from shapely.geometry import shape,box
from shapely.ops import unary_union
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';OUT=ROOT/'output'
def read(name):return json.loads((DATA/name).read_text())
def csvrows(name):return list(csv.DictReader((DATA/name).open(encoding='utf-8-sig')))

def main():
    rows=read('study_regions.json');features=read('study_regions.geojson')['features'];sources=read('sources.json')
    assert all(r['source_id'] in sources for r in read('input_manifest.json'))
    ids=[r['id'] for r in rows];assert len(ids)==len(set(ids))
    assert set(ids)=={f['id'] for f in features}
    main_csv=list(csv.DictReader((OUT/'ヒジャブの出現率.csv').open(encoding='utf-8-sig')))
    assert [r['地域ID'] for r in main_csv]==ids
    assert (OUT/'ヒジャブの出現率.csv').read_bytes().startswith(b'\xef\xbb\xbf')
    for i,(row,record,f) in enumerate(zip(main_csv,rows,features),1):
        assert row['地図番号']==str(i).zfill(3)==str(f['properties']['map_number']).zfill(3)
        assert row['ヒジャブの出現率']==record['level']==f['properties']['level']
        assert record['level'] in ['高い','やや高い']
        assert record['area_ja'] and record['un_region_ja']
        assert all(s in sources for s in record['source_ids'])
        assert all(sources[s]['url'].startswith('https://') for s in record['source_ids'])
        assert all(sources[s].get('retrieval_status')=='retrieved' for s in record['source_ids'] if s.startswith('IRF-'))
        assert all(s['source_id'] in record['source_ids'] for s in record['statistic_records'])
        assert not any(v.startswith(('=','+','@')) for v in row.values())
    # Numbers are population counts/proportions, never inferred clothing rates.
    for name in ['india_religion_2011.csv','indonesia_provinces_2010.csv']:
        for r in csvrows(name):
            pop,muslim,women,muslim_women=map(int,[r['population'],r['muslims'],r['women'],r['muslim_women']])
            assert 0<=muslim_women<=women<=pop and muslim_women<=muslim<=pop
            assert abs(100*muslim/pop-float(r['muslim_percent']))<.00006
            assert int(r['year'])>=2000
    n=csvrows('national_religion_2010_2020.csv');assert len(n)==416
    assert all(len(v)==2 and {r['year'] for r in v}=={'2010','2020'} for k,v in itertools.groupby(sorted(n,key=lambda r:r['place']),key=lambda r:r['place']) for v in [list(v)])
    assert len(csvrows('sri_lanka_districts_2024.csv'))==26
    lka={r['area']:float(r['muslim_percent']) for r in csvrows('sri_lanka_districts_2024.csv')}
    assert lka['Ampara']==45.6 and lka['Trincomalee']==46.5 and lka['Batticaloa']==27.1
    ind={r['area']:float(r['muslim_percent']) for r in csvrows('india_religion_2011.csv')}
    assert abs(ind['District - Kozhikode']-39.2423)<.0001
    assert abs(ind['District - Malappuram']-70.2384)<.0001
    # Guard the important head-cover vs hijab distinction.
    clothing=csvrows('clothing_surveys.csv')
    cm={(r['iso3'],r['survey_area'],r['metric']):float(r['percent']) for r in clothing}
    assert cm['IND','national','head_cover_practice']==89
    assert cm['IND','national','hijab']==8
    assert cm['IND','South','hijab']==23
    assert cm['IDN','national','hijab_usually']==61.9
    # Geometry remains inside its intended country; points use a small coastal tolerance.
    countries=defaultdict(list)
    for f in read('basemap_countries.geojson')['features']:countries[f['properties']['iso3']].append(shape(f['geometry']))
    countries={k:unary_union(v) for k,v in countries.items()}
    if 'MYT' not in countries:countries['MYT']=countries['FRA'].intersection(box(45,-13.1,45.4,-12.55))
    polygons=defaultdict(list);issues=[];points=0
    for f in features:
        g=shape(f['geometry']);iso=f['properties']['iso3']
        assert g.is_valid and not g.is_empty,(f['id'],'invalid geometry')
        assert box(-180,-90,180,90).covers(g)
        if g.geom_type=='Point':
            points+=1
            # Some tiny offshore enclaves are absent from 1:10m country geometry.
            tolerance=.15 if f['id'] not in ['ESP-ceuta','ESP-melilla'] else 2.0
            if g.distance(countries[iso])>tolerance:issues.append((f['id'],g.distance(countries[iso])))
        else:
            assert g.difference(countries[iso].buffer(.00003)).area<.00005,(f['id'],'outside country')
            polygons[iso].append((f['id'],g))
    assert not issues,issues
    for values in polygons.values():
        for (id1,a),(id2,b) in itertools.combinations(values,2):
            assert a.intersection(b).area<.00001,(id1,id2,'overlap')
    # M49 exceptions must survive refactoring.
    assert next(r for r in rows if r['iso3']=='IRN')['un_region_ja']=='南アジア'
    assert next(r for r in rows if r['iso3']=='RUS')['un_region_ja']=='東ヨーロッパ'
    assert next(r for r in rows if r['iso3']=='FRA')['country_ja']=='フランス'
    assert next(r for r in rows if r['iso3']=='AUS')['country_ja']=='オーストラリア'
    pdf=PdfReader(OUT/'ヒジャブの出現率_地図帳.pdf')
    assert len(pdf.pages)==10
    text='\n'.join(p.extract_text() for p in pdf.pages)
    assert 'ヒジャブ' in text and 'インド' in text
    if (DATA/'teikoku_calibration.json').exists():
        calibration=read('teikoku_calibration.json')
        assert max(p['residual_pixels'] for p in calibration['control_points'])<1
        assert {f['region_id'] for f in read('teikoku_pixel_regions.json')['features']}==set(ids)
    report=dict(status='passed',study_regions=len(rows),countries_and_areas=len({r['iso3'] for r in rows}),area_geometries=len(rows)-points,point_markers=points,pdf_pages=len(pdf.pages),national_statistic_records=len(n),india_statistic_records=len(ind),checks=['CSV/GeoJSON IDs, ratings and map numbers','Source references and survey distinctions','Population counts and denominators','Country clipping, valid geometry and non-overlap','PDF page count and Japanese text','Teikoku projection control points when available'])
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
