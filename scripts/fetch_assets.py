"""Download only requested public inputs, atomically and with SHA-256 checks."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]

def fetch(asset):
    dest=ROOT/'.cache'/asset['filename'];dest.parent.mkdir(exist_ok=True)
    if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()==asset['sha256']:return
    tmp=dest.with_name(dest.name+'.partial')
    command=['curl','--fail','--location','--show-error','--silent','--retry','2','--connect-timeout','20','--max-time','120',asset['url'],'--output',str(tmp)]
    # Normal TLS verification is always enabled; callers may supply their host's
    # trusted CA bundle through curl's standard CURL_CA_BUNDLE environment option.
    subprocess.run(command,check=True)
    actual=hashlib.sha256(tmp.read_bytes()).hexdigest()
    if actual!=asset['sha256']:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"Source changed: {asset['filename']}. Expected {asset['sha256']}, got {actual}. Review the source before updating the manifest.")
    tmp.replace(dest);print('Downloaded',asset['filename'],flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--statistics',action='store_true',help='Original statistical tables, for re-extraction')
    p.add_argument('--geometry',action='store_true',help='Pinned original Natural Earth geometry')
    p.add_argument('--teikoku',action='store_true',help='Personal-use publisher map; never added to Git')
    args=p.parse_args();groups={'font'}
    for name in ['statistics','geometry','teikoku']:
        if getattr(args,name):groups.add(name)
    for asset in json.loads((ROOT/'data/input_manifest.json').read_text()):
        if asset['group'] in groups:fetch(asset)

if __name__=='__main__':main()
