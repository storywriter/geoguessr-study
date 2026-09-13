"""Generate the page index and package licenses already fetched by the build."""
from pathlib import Path
import json
TOPIC=Path(__file__).resolve().parents[1];ROOT=TOPIC.parents[1]
def main():
    pages=json.loads((TOPIC/'data/page_definitions.json').read_text())
    lines=['# 地図帳のページ一覧','','PDFのページ番号とPNGの番号が対応します。PNGを開くと拡大できます。','','| ページ | 内容 |','|---|---|','| 1 | [対象範囲と使い方](../output/atlas_01.png) |','| 2 | [似た文字の比較早見表](../output/atlas_02.png) |']
    lines += [f'| {p["number"]} | [{p["title"]}](../output/atlas_{p["number"]:02d}.png) |' for p in pages]
    (TOPIC/'docs/ATLAS_INDEX.md').write_text('\n'.join(lines)+'\n')
    for name in ['Unicode-LICENSE.txt','NotoSans-OFL.txt','NotoSansArmenian-OFL.txt','NotoSansGeorgian-OFL.txt']:
        dest='UNICODE-LICENSE.txt' if name=='Unicode-LICENSE.txt' else name
        original=(ROOT/'.cache/european-letterforms'/name).read_text()
        (TOPIC/'docs'/dest).write_text('\n'.join(line.rstrip() for line in original.splitlines())+'\n')
    print('Page index and third-party licenses written.')
if __name__=='__main__':main()
