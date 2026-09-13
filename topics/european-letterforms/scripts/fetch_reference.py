"""Fetch pinned Unicode character data and fonts; keep complete inputs in cache."""
from pathlib import Path
import base64, concurrent.futures, hashlib, json, shutil, subprocess, xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

TOPIC = Path(__file__).resolve().parents[1]
ROOT = TOPIC.parents[1]
CACHE = ROOT / '.cache/european-letterforms'
CLDR = 'fc1fd058cc6f50544a450a3b15a4bba0e0c1e653'
FONTS = '809e4d8b8d7e9364a914909bb777679606c178b8'
GH_USABLE = bool(shutil.which('gh')) and subprocess.run(['gh','auth','status'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
LOCALES = '''en cy ga gd kw gv fo is da nb nn sv fi se smj sma smn sms et lv lt de fr nl fy lb br co oc ca eu gl ast an pt it rm fur lld sc el mt sq bs hr sr sr_Latn sl mk bg ro hu cs sk pl be uk ru hy az ka tr gag hsb dsb nds wa tt ba cv ce os av lez kbd ady krc ab kum nog xal kv udm mhr mrj myv mdf sah bua tyv alt kjh krl vep frr lij vec nap scn sco crh'''.split()
LOCALES += ['es', 'no', 'gsw', 'csb', 'rue', 'az_Cyrl']

def get(item):
    name,url = item
    dest = CACHE/name
    if not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True)
        # gh uses the host's configured trust store and also works when curl's
        # CA bundle does not include the organisation's certificate chain.
        if GH_USABLE and urlsplit(url).hostname=='raw.githubusercontent.com':
            owner,repo,ref,relative=unquote(urlsplit(url).path).lstrip('/').split('/',3)
            if name.endswith('.ttf'):
                # Decode binary through the documented blob API. gh's raw-text
                # response path can reject arbitrary font byte sequences.
                meta=json.loads(subprocess.check_output(['gh','api',f'repos/{owner}/{repo}/contents/{relative}?ref={ref}'],text=True))
                blob=json.loads(subprocess.check_output(['gh','api',f'repos/{owner}/{repo}/git/blobs/{meta["sha"]}'],text=True))
                dest.write_bytes(base64.b64decode(blob['content']))
                return {'filename':name,'url':url,'retrieved':True,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size}
            command=['gh','api',f'repos/{owner}/{repo}/contents/{relative}?ref={ref}','--header','Accept: application/vnd.github.raw+json']
            with open(str(dest)+'.partial','wb') as output:
                result=subprocess.run(command,stdout=output,stderr=subprocess.PIPE,text=True)
        else:
            result = subprocess.run(['curl','--globoff','--fail','--location','--silent','--show-error','--retry','2','--connect-timeout','15','--max-time','60',url,'--output',str(dest)+'.partial'],capture_output=True,text=True)
        if result.returncode:
            Path(str(dest)+'.partial').unlink(missing_ok=True)
            return {'filename':name,'url':url,'retrieved':False,'error':result.stderr.strip()}
        Path(str(dest)+'.partial').replace(dest)
    return {'filename':name,'url':url,'retrieved':True,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size}

def main():
    inputs = [(f'cldr/{loc}.xml',f'https://raw.githubusercontent.com/unicode-org/cldr/{CLDR}/common/main/{loc}.xml') for loc in LOCALES]
    for family in ['NotoSans','NotoSansArmenian','NotoSansGeorgian']:
        folder=family.lower()
        inputs += [(f'{family}.ttf',f'https://raw.githubusercontent.com/google/fonts/{FONTS}/ofl/{folder}/{family}%5Bwdth,wght%5D.ttf'),(f'{family}-OFL.txt',f'https://raw.githubusercontent.com/google/fonts/{FONTS}/ofl/{folder}/OFL.txt')]
    inputs += [('Unicode-LICENSE.txt',f'https://raw.githubusercontent.com/unicode-org/cldr/{CLDR}/LICENSE')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: records=list(pool.map(get,inputs))
    (TOPIC/'data').mkdir(parents=True,exist_ok=True)
    (TOPIC/'data/reference_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    data={}
    for r in records:
        if not r['retrieved'] or not r['filename'].endswith('.xml'): continue
        loc=Path(r['filename']).stem
        xml=ET.parse(CACHE/r['filename'])
        alias=xml.find('./alias')
        data[loc]={'source_url':r['url'],'alias':alias.get('source') if alias is not None else None,'main':xml.findtext('./characters/exemplarCharacters'),
                   'auxiliary':xml.findtext('./characters/exemplarCharacters[@type="auxiliary"]'),
                   'conjunction':xml.findtext('./listPatterns/listPattern/listPatternPart[@type="end"]')}
    (TOPIC/'data/cldr_characters.json').write_text(json.dumps({'release':'48.2','commit':CLDR,'locales':data},ensure_ascii=False,indent=2)+'\n')
    print('Retrieved',sum(r['retrieved'] for r in records),'/',len(records),'reference files')
    print('CLDR locales absent:',', '.join(Path(r['filename']).stem for r in records if not r['retrieved']))

if __name__=='__main__':main()
