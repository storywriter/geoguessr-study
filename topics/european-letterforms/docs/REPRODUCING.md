# 更新と再生成

リポジトリのルート `geoguessr-study` で実行する。Python 3.12とルートの固定依存関係を使用する。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/fetch_assets.py
.venv/bin/python topics/european-letterforms/scripts/fetch_reference.py
.venv/bin/python topics/european-letterforms/scripts/build.py
.venv/bin/python topics/european-letterforms/scripts/render.py
.venv/bin/python topics/european-letterforms/scripts/publish_docs.py
.venv/bin/python topics/european-letterforms/scripts/validate.py
```

共有の境界と前回の日本語フォント以外は、このテーマ内のデータを使う。ダウンロードした全文XMLとフォントは `.cache/european-letterforms/` に置き、必要な抽出データ・URL・commit・ハッシュだけをGitへ保存する。最初の取得にはネットワークが必要で、TLS検証を無効化しない。認証済みのGitHub CLIがある場合はGitHub APIを使用し、ない場合はcurlの通常のHTTPS取得を使う。GitHub APIのフォントはblob APIでBase64を復号する。

## 原本

| 原本 | 変更する内容 |
|---|---|
| `scripts/catalog.py` | 国・地域、言語の対応、制度・表示の注記、地図範囲、参照資料ID |
| `scripts/languages.py` | 日本語名、文字体系、特徴字、短語、比較・例外、補助文字資料 |
| `scripts/sources.py` | 出典URL・年・確認日、出典付き統計値と分母 |
| `scripts/fetch_reference.py` | 固定したUnicode CLDR / Google Fontsの版、取得先 |
| `scripts/render.py` | フォント、レイアウト、色、番号・引出線の配置 |

`data/` と `output/` の生成物を直接編集しない。地域IDは維持し、行の挿入でページ・地図番号が変わる場合は `build.py` 以下を再実行する。取得元のcommitを変更する場合は対象キャッシュが旧版のまま残らないよう、そのファイルを改名退避するかキャッシュ名を変更して再取得し、URLとSHA-256を再確認する。

`build.py` は全56地域の収録を確認し、過去の行数を固定値としてテストしない。各ページ最大7カードとして、極端に空いた最終ページが出ないよう均等に分割する。PDF・PNGは決定的なソースから再生成するが、PDFライブラリの版やフォント埋め込みによってファイルのバイト列は変わり得る。

## 座標とID

- `data/study_regions.geojson`：実際に塗った範囲と点。WGS84、座標順は経度・緯度、単位は度。
- `data/regions.json`：`geometry_spec` に元の行政区名、矩形、代表点を保持。`anchor_lonlat` と `bbox` も付く。
- `data/country_shapes.geojson`：このテーマで使う派生国別形状。スヴァールバル等の分離やクリミアの整理を含む。
- `data/page_definitions.json`：ページ、表示経緯度範囲、掲載項目ID。
- `data/map_label_coordinates.json`：ページごとのアンカー、引出線先、PDF上の座標。PDFの左下が原点、単位はpoint、1 inch = 72 points。
- `data/occurrences.json`：地域IDと言語IDを `:` で結んだ掲載項目ID。各項目は地図帳に1回対応付ける。

矩形や行政区の国境切断後にShapelyで妥当性を確認し、0.00001度の精度へそろえる。面積の割合を人口の割合と解釈しない。境界ファイルはルートの `data/input_manifest.json` で出典・版・ハッシュを確認できる。

## CSVの著者作業と確認

ポータブルな再生成はPythonのみでよい。今回のCodexによる著者作業では `@oai/artifact-tool` へ全セルを設定し、同じ値からCSVを保存してPython版との完全一致を確認した。

```sh
node topics/european-letterforms/scripts/export_with_artifact_tool.mjs
```

この任意のコマンドは、Codexの同パッケージがNodeから解決できる環境で実行する。ライブラリ自体や `node_modules` はリポジトリへ含めない。CSVはBOM付きUTF-8、CRLF、全22列。セル値は文字列として扱い、ラテン・キリル・結合記号を勝手に置換しない。

## 表示確認

```sh
mkdir -p .cache/european-letterforms/pdf-qa
pdftoppm -r 90 -png topics/european-letterforms/output/ヨーロッパ周辺の特徴的な文字形_地図帳.pdf .cache/european-letterforms/pdf-qa/page
```

全ページの地図・番号・カードが見えること、字形と語が重ならないこと、点の引出線、アルメニア・ジョージア・拡張キリルの字形を確認する。`validate.py` は完成したPDFの日本語名と特徴字を全項目について照合し、42件の数値の年・分母・出典、幾何形状、地図上の位置も確認する。

公開前にGitの差分を確認し、第一弾のデータと出力に変更がないことを確認する。このテーマの変更をcommitし、ユーザーがpushを依頼した場合に通常のpushを行う。
