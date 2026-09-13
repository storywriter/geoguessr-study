"""Cache primary USDOS reports from ACCORD's publicly accessible mirror.

Original prose is not distributed with the project. Discovery metadata is saved.
"""
import concurrent.futures,json,re,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from catalog import REGIONS
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'.cache'
SLUGS=dict(x.split(':') for x in '''AZE:azerbaijan BEN:benin BGR:bulgaria BRN:brunei CIV:cote-d-ivoire CMR:cameroon DJI:djibouti ERI:eritrea ESP:spain ETH:ethiopia GEO:georgia GHA:ghana GIN:guinea GNB:guinea-bissau GRC:greece IRQ:iraq ISR:israel KEN:kenya KGZ:kyrgyzstan KHM:cambodia LBN:lebanon LBY:libya MDG:madagascar MKD:north-macedonia MMR:myanmar MNE:montenegro MOZ:mozambique MRT:mauritania MWI:malawi MYS:malaysia NGA:nigeria NPL:nepal OMN:oman PSE:palestine RUS:russian-federation SDN:sudan SRB:serbia SYR:syria TCD:chad TGO:togo THA:thailand TZA:tanzania UGA:uganda UZB:uzbekistan YEM:yemen ZAF:south-africa'''.split())

def get(url,path):
    if not path.exists():
        cmd=['/usr/bin/curl','--fail','--location','--silent','--show-error','--max-time','25']
        r=subprocess.run(cmd+[url,'--output',str(path)+'.partial'],capture_output=True)
        if r.returncode:raise RuntimeError(r.stderr.decode()[:100])
        Path(str(path)+'.partial').replace(path)
    return BeautifulSoup(path.read_text(),'html.parser')

def one(code):
    try:
        s=get('https://www.ecoi.net/en/countries/'+SLUGS[code]+'/',CACHE/f'irf-index-{code}.html')
        links=[a for a in s.find_all('a',href=True) if '2023 Report on International Religious Freedom' in a.get_text(' ',strip=True)]
        if not links:return code,{'status':'not_found'}
        url=links[0]['href'];url='https://www.ecoi.net'+url if url.startswith('/') else url
        s=get(url,CACHE/f'irf-{code}.html')
        t=s.get_text(' ',strip=True)
        m=re.search(r'Section I\. Religious Demography(.*?)(?:Section II\.|LEGAL FRAMEWORK)',t)
        return code,{'status':'retrieved' if m else 'section_missing','mirror_url':url,'title':links[0].get_text(' ',strip=True),'demography':m[1].strip() if m else ''}
    except Exception as e:return code,{'status':'error','error':str(e)}

if __name__=='__main__':
    codes=sorted({s[4:] for r in REGIONS for s in r['sources'] if s.startswith('IRF-')})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        rows={}
        for code,r in ex.map(one,codes):
            rows[code]=r;print(code,r['status'],flush=True)
    (CACHE/'irf-discovery.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
