"""Cross-artifact checks: data joins, country coverage, real glyphs and PDF content."""
from pathlib import Path
import csv,hashlib,json,sys,unicodedata
from shapely.geometry import shape,box,Point
from pypdf import PdfReader
from catalog import COUNTRIES
from languages import LANGUAGES
TOPIC=Path(__file__).resolve().parents[1];ROOT=TOPIC.parents[1];DATA=TOPIC/'data';OUT=TOPIC/'output'
def read(name):return json.loads((DATA/name).read_text())
def main():
    rows=list(csv.DictReader((OUT/'ヨーロッパ周辺の特徴的な文字形.csv').open(encoding='utf-8-sig',newline='')))
    regions={r['id']:r for r in read('regions.json')};occ={o['id']:o for o in read('occurrences.json')}
    features={f['id']:f for f in read('study_regions.geojson')['features']};pages=read('page_definitions.json')
    sourceids={s['id'] for s in read('sources.json')}
    stats=list(csv.DictReader((DATA/'statistics.csv').open(encoding='utf-8-sig')));statids={s['id'] for s in stats}
    assert len(regions)==len(features) and set(regions)==set(features)
    assert len(rows)==len(occ) and len({(r['地域ID'],r['言語ID']) for r in rows})==len(rows)
    assert {r['iso3'] for r in regions.values()}==set(COUNTRIES)
    placed=[o for p in pages for o in p['occurrence_ids']]
    assert len(placed)==len(set(placed))==len(occ) and set(placed)==set(occ)
    for s in stats:
        assert 2000<=int(s['year'])<=2026 and 0<=float(s['value_percent'])<=100
        assert s['denominator_ja'] and s['source_id'] in sourceids
    for r in rows:
        assert r['地域ID'] in regions and r['言語ID'] in LANGUAGES
        assert not (set(r['統計ID'].split('; '))-{''})-statids
        assert not (set(r['参照資料ID'].split('; '))-{''})-sourceids
        assert r['特徴となる文字形'] and r['文字の出典URL'].startswith('https://')
        assert '\ufffd' not in ''.join(r.values())
    for rid,f in features.items():
        g=shape(f['geometry']);assert g.is_valid and not g.is_empty,rid
        assert g.distance(Point(*regions[rid]['anchor_lonlat']))<.0001,rid
    cs={f['id']:shape(f['geometry']) for f in read('country_shapes.geojson')['features']}
    # Prevent accidental assignment of Norway's mainland north of 70.7 N to SJM.
    assert cs['NOR'].distance(Point(25.78,71.16))<.04
    assert cs['SJM'].distance(Point(25.78,71.16))>2
    assert cs['UKR'].distance(Point(34.1,44.95))<.01 and cs['RUS'].distance(Point(34.1,44.95))>.2
    pdfpath=OUT/'ヨーロッパ周辺の特徴的な文字形_地図帳.pdf';pdf=PdfReader(pdfpath)
    assert len(pdf.pages)==len(pages)+2
    def compact(s):return ''.join(unicodedata.normalize('NFC',s).split())
    for p in pages:
        t=compact(pdf.pages[p['number']-1].extract_text())
        for oid in p['occurrence_ids']:
            l=LANGUAGES[occ[oid]['language_id']]
            assert compact(l['glyphs']) in t,(p['number'],oid,'missing PDF glyph string')
            assert compact(l['name_ja'].replace('（バレンシア語を含む）','・バレンシア語')) in t,(p['number'],oid,'missing Japanese name')
        assert (OUT/f'atlas_{p["number"]:02d}.png').exists()
    labels=read('map_label_coordinates.json')
    assert {(v['page'],v['region_id']) for v in labels}=={(p['number'],rid) for p in pages for rid in p['region_ids']}
    hashes={str(p.relative_to(TOPIC)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.is_file()}
    report=dict(countries_and_areas=len(COUNTRIES),regions=len(regions),language_profiles=len(LANGUAGES),csv_rows=len(rows),statistics=len(stats),pdf_pages=len(pdf.pages),map_labels=len(labels),all_occurrences_mapped=True,pdf_glyph_strings_present=True,geometry_valid=True,artifact_sha256=hashes)
    (DATA/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='artifact_sha256'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
