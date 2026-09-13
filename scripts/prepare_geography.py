"""Retain reusable, attributed Natural Earth geometry in EPSG:4326."""
from pathlib import Path
import json
from shapely.geometry import shape,mapping
ROOT=Path(__file__).resolve().parents[1]
COMMIT='ca96624a56bd078437bca8184e78163e5039ad19'

def rounded(o):
    if isinstance(o,float):return round(o,5)
    if isinstance(o,(tuple,list)):return [rounded(v) for v in o]
    if isinstance(o,dict):return {k:rounded(v) for k,v in o.items()}
    return o

def main():
    for src,dest in [('countries.geojson','basemap_countries.geojson'),('admin1.geojson','basemap_admin1.geojson')]:
        features=[]
        for f in json.load(open(ROOT/'.cache'/src))['features']:
            p=f['properties']
            if src.startswith('countries'):
                pr={k:p.get(k) for k in ['ADMIN','ADM0_A3','ISO_A3_EH','NAME_JA','SUBREGION']}
                iso=pr['ISO_A3_EH']
                if pr['ADM0_A3']=='SOL':iso='SOM'
                if pr['ADM0_A3']=='KOS':iso='XKX'
                pr['iso3']=iso
            else:
                pr={k:p.get(k) for k in ['name','adm0_a3','iso_3166_2']}
            g=shape(f['geometry']).simplify(0.012,preserve_topology=True)
            features.append(dict(type='Feature',properties=pr,geometry=rounded(mapping(g))))
        out=dict(type='FeatureCollection',source='Natural Earth 1:10m; public domain',upstream_commit=COMMIT,simplification_degrees=0.012,coordinate_reference_system='EPSG:4326; longitude, latitude',features=features)
        (ROOT/'data'/dest).write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n')
        print(dest,len(features))

if __name__=='__main__':main()
