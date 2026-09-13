"""Extract numeric facts only. Population religion is not a clothing measure."""
from pathlib import Path
import csv,json,re,logging
from bs4 import BeautifulSoup
from pypdf import PdfReader
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'.cache'
DATA=ROOT/'data'
logging.getLogger('pypdf').setLevel(logging.ERROR)

def write_csv(name,rows):
    DATA.mkdir(exist_ok=True)
    with (DATA/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    # PDF layout preserves multiword and wrapped country names.
    rows=[]
    for page in PdfReader(CACHE/'pew-national.pdf').pages:
        lines=page.extract_text(extraction_mode='layout').splitlines()
        pending=''
        for i,line in enumerate(lines):
            m=re.match(r'^\s*(.*?)\s+(2010|2020)\s+([\d,]+)\s+(.+)$',line)
            if not m: continue
            name,year,pop,values=m.groups();v=values.split()
            def name_only(s):
                return bool(s.strip()) and not re.search(r'\d|%|www\.|PEW|Place|religion|Appendix',s) and len(s.rstrip())<24
            if i>0 and name_only(lines[i-1]) and not (i>1 and re.search(r'\b(?:2010|2020)\b',lines[i-2])): name=lines[i-1].strip()+' '+name
            if i+1<len(lines) and name_only(lines[i+1]): name=name+' '+lines[i+1].strip()
            name=name.replace('- ','-')
            if len(v)!=7: raise ValueError(line)
            rows.append(dict(place=name.strip(),year=int(year),population=int(pop.replace(',','')),muslim_percent=v[1].replace('%',''),source_id='PEW2025',source_page=page.page_number+1))
    write_csv('national_religion_2010_2020.csv',rows)
    # M49 includes intermediate African subdivisions; use the finest region.
    soup=BeautifulSoup((CACHE/'m49.html').read_text(),'html.parser')
    records=[];region=''
    for tr in soup.find('table',id='GeoGroupsENG').find_all('tr'):
        cells=[c.get_text(' ',strip=True) for c in tr.find_all('td')]
        if len(cells)>=3 and re.fullmatch('[A-Z]{3}',cells[2]):
            records.append(dict(name=cells[0],m49=cells[1],iso3=cells[2],region=region))
        elif cells and any(x in cells[0] for x in ['Africa','Asia','Europe','America','Caribbean','Melanesia','Micronesia','Polynesia','Australia and New Zealand']):region=cells[0]
    write_csv('un_m49.csv',records)
    # Indonesia 2010: each religion has urban/rural/total x male/female/both.
    soup=BeautifulSoup((CACHE/'idn-religion.html').read_text(),'html.parser')
    records=[]
    for tr in soup.find('table').find_all('tr')[3:]:
        c=[x.get_text(' ',strip=True) for x in tr.find_all('td')]
        if len(c)!=91: continue
        n=lambda s:int(s.replace('.','').replace('-','0'))
        records.append(dict(area=c[0],year=2010,muslims=n(c[9]),population=n(c[90]),muslim_percent=round(100*n(c[9])/n(c[90]),4),muslim_women=n(c[8]),women=n(c[89]),source_id='BPS2010'))
    write_csv('indonesia_provinces_2010.csv',records)
    records=[]
    page=PdfReader(CACHE/'lka-2024.pdf').pages[95]
    for line in page.extract_text(extraction_mode='layout').splitlines():
        m=re.match(r'^\s*([A-Za-z ]+?)\s+(\d+\.\d.*?)\s*$',line)
        if not m:continue
        v=m[2].split()
        if len(v)==12:
            records.append(dict(area=m[1].strip(),year=2024,muslim_percent=float(v[5]),source_id='LKA2024',source_page=96))
    write_csv('sri_lanka_districts_2024.csv',records)
    records=[]
    for p in sorted(CACHE.glob('india-c01*.xls')):
        d=pd.read_excel(p,header=None,dtype=object)
        for _,r in d.iterrows():
            if r[6]!='Total' or not isinstance(r[7],(int,float)):continue
            # Keep country/state/district; discard towns and tehsils.
            if str(r[3]).strip() not in ['0','00000'] or str(r[4]).strip() not in ['0','000000']:continue
            records.append(dict(area=str(r[5]).strip(),state_code=str(r[1]).zfill(2),district_code=str(r[2]).zfill(3),year=2011,population=int(r[7]),muslims=int(r[13]),muslim_percent=round(100*r[13]/r[7],4),women=int(r[9]),muslim_women=int(r[15]),source_id='IND_C01',input_file=p.name))
    # State files repeat state totals, use unique census codes.
    records=list({(r['state_code'],r['district_code']):r for r in records}.values())
    write_csv('india_religion_2011.csv',records)
    print(json.dumps({'national_records':len(rows),'india_records':len(records),'m49_records':len(list(csv.DictReader((DATA/'un_m49.csv').open())))}))

if __name__=='__main__':main()
