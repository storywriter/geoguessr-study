# 再生成・更新手順

## 通常の再生成

Python 3.12と `requirements.txt` の環境を使う。作業ディレクトリはリポジトリ直下。`scripts/fetch_assets.py` は通常、日本語フォントだけを取得する。HTTP取得のTLS検証を無効にしない。組織のCA証明書が必要な環境ではcurlの標準設定を使用する。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/fetch_assets.py
.venv/bin/python scripts/build.py
```

元の統計サイトへアクセスせず、保存した数値とNatural Earthの地理データからCSV・GeoJSON・世界図・10ページの地図帳を再生成する。ダウンロード後はネットワークなしで実行できる。

`build.py` の処理順は次のとおり。

1. `source_catalog.py`：出典・手作業で確認した統計・服装調査の表を生成。
2. `build_dataset.py`：地域定義と数値資料を結合し、国境で切り抜き、重複を処理。UTF-8 BOM・CRLFのCSVを書き出す。
3. `render_maps.py`：日本語フォントを読み込み、Natural Earthを白地図に図・PDFを描画。
4. `validate.py`：データの結合、数値、図形、PDFを検証し `output/validation.json` を更新。

Codexのartifact-tool環境がある場合は、`scripts/export_with_artifact_tool.mjs` で同じ値をシートへ書き込み、CSVを書き出してPython版と完全一致を確認できる。通常の再生成にはNode.jsもartifact-toolも不要。

## 地域・判定を変更する

- 編集する原本は `scripts/catalog.py`。`country`、`admin`、`box`、`polygon`、`city` を使い分ける。
- 既存の `ISO3-slug` 形式の地域IDは維持する。地図番号は行順から生成する表示番号であり、恒久IDではない。
- ユーザー向け地域名は方角、国境、沿岸、都市で記す。離れた集積を一つの塗りにまとめない。
- 出典の追加は `scripts/source_catalog.py`。数値は分母、資料年、原資料の地域名、出典IDを必ず持たせる。
- 広域や全国の統計を小地域の統計に改称しない。主観的な衣服の判定と人口比率の数値を分ける。
- 州名がNatural Earthの `name` と完全一致するか、`data/basemap_admin1.geojson` で確認する。原データにない州を推測してつなげない。
- 更新後に `scripts/build.py` を実行し、関連する拡大図を開いて境界、ラベル、文字欠けを確認する。生成物を手で直さない。

## 元の統計から再抽出する

```sh
.venv/bin/python scripts/fetch_assets.py --statistics
.venv/bin/python scripts/extract_statistics.py
.venv/bin/python scripts/build.py
```

`data/input_manifest.json` にURL、SHA-256、ファイルサイズ、出典IDがある。国勢調査のXLSやPDFは原文のまま `.cache/` に置き、公開しない。

HTMLの内容が更新されているとハッシュ検証で停止する。無条件に新しい内容を受け入れず、設問・列・分母・資料年を確認してからmanifestと抽出処理を更新する。2011年インドの地区ファイルはジャンムー・カシミール、デリー、アッサム、西ベンガル、マハラシュトラ、カルナータカ、ケララを取得している。他の州については全国版の州集計のみ。必要な地区表を後から追加できる。

USDOS報告の保存版URL・確認状態は `data/irf_source_metadata.json` に記録している。`collect_irf.py` は初回調査用の取得補助で、国別一覧の掲載順に依存する。再取得後、本文を読んでから公開メタデータへ反映する。全文のコピーを公開しない。

## 境界データを再生成する

```sh
.venv/bin/python scripts/fetch_assets.py --geometry
.venv/bin/python scripts/prepare_geography.py
.venv/bin/python scripts/build.py
```

Natural Earthの上流Git commitは `ca96624a56bd078437bca8184e78163e5039ad19`。1:10mの行政界を0.012度でトポロジーを保って簡略化し、経緯度を小数5桁で保存する。簡略化後の座標は学習用であり、測量精度ではない。

GeoJSONはWGS84 (EPSG:4326)、**経度、緯度**の順。世界図はRobinson図法、地域図は経緯度を中緯度のcosで縦横補正した簡略図。

## 塗色範囲の座標を探す

CSVの「地域ID」は `data/study_regions.geojson` の各Featureの `id` と一致する。`geometry` に面の頂点または都市の点の経緯度、`properties` に判定と地図番号がある。面のSVG要素は `地域ID-0`、`地域ID-1` のように図形ごとの枝番号を付けている。都市の点の座標はGeoJSONから取得する。

位置や塗色を変更するときは `scripts/catalog.py` の同じ地域IDを編集し、`scripts/build.py` で再生成する。描画時の投影と図の配置は `scripts/render_maps.py` に保存しているため、画像サイズを変える場合も経緯度から再描画できる。

## 公開前の確認

```sh
.venv/bin/python scripts/validate.py
git status --short
git diff --stat
git ls-files
```

`.cache/`、`.venv/`、`node_modules`、元の参考画像、報告書全文、個人情報を追加しない。公開対象は編集した数値資料・地域データ・Natural Earthを使った地図・プログラム・手順書である。
