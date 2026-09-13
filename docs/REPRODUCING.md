# 再生成・更新手順

## 通常の再生成

Python 3.12と `requirements.txt` の環境を使う。作業ディレクトリはリポジトリ直下。`scripts/fetch_assets.py` は通常、日本語フォントだけを取得する。HTTP取得のTLS検証を無効にしない。組織のCA証明書が必要な環境ではcurlの標準設定を使用する。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/fetch_assets.py
.venv/bin/python scripts/build.py
```

元の統計サイトへアクセスせず、保存した数値と地理データからCSV・GeoJSON・世界図・10ページの地図帳を再生成する。ダウンロード後はネットワークなしで実行できる。帝国書院の原図がキャッシュにある環境では、ローカル版も更新する。

`build.py` の処理順は次のとおり。

1. `source_catalog.py`：出典・手作業で確認した統計・服装調査の表を生成。
2. `build_dataset.py`：地域定義と数値資料を結合し、国境で切り抜き、重複を処理。UTF-8 BOM・CRLFのCSVを書き出す。
3. `render_maps.py`：日本語フォントを読み込み、公開版の図・PDFを描画。帝国書院の原図があれば個人学習用の加工図を描画。
4. `validate.py`：データの結合、数値、図形、PDF、投影座標を検証し `output/validation.json` を更新。

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

公開GeoJSONはWGS84 (EPSG:4326)、**経度、緯度**の順。世界図はRobinson図法、地域図は経緯度を中緯度のcosで縦横補正した簡略図。公開SVGの着色パスには地域IDを付けてある。

## 帝国書院版をローカルで再生成する

利用条件を確認した個人学習の範囲で次を実行する。原図・加工図を公開Gitへ追加しない。

```sh
.venv/bin/python scripts/fetch_assets.py --teikoku
.venv/bin/python scripts/render_maps.py
.venv/bin/python scripts/validate.py
```

生成先は `local-only/ヒジャブの出現率_帝国書院.png`。原図は `世界全図 ヨーロッパ中心 メルカトル図法` の9921×7016ピクセルPNG。元の著作権表示を残す。

- 投影：楕円体メルカトル、EPSG:3395。
- 画像座標：左上原点、xは右向き、yは下向き。
- 変換：`x_px = x0 + scale * easting`、`y_px = y0 - scale * northing`。
- `(x0, y0) = (4763, 3511)`。縮尺・基準点・原図ハッシュは `data/teikoku_calibration.json` に保存。
- 完成図の塗色範囲は `data/teikoku_pixel_regions.json` の `region_id` から検索できる。

経緯線の位置合わせは基準点7点で最大1ピクセル未満。これは海岸線・国境の一致精度ではない。出版社の原図とNatural Earthは独立した地図なので、個々の境界が異なることがある。原図の版・画像サイズを変更したときは、同じ変換値を使い回さない。

## 公開前の確認

```sh
.venv/bin/python scripts/validate.py
git status --short
git diff --stat
git ls-files
```

`.cache/`、`.venv/`、`node_modules`、`local-only/`、元の参考画像、報告書全文、個人情報を追加しない。公開対象は編集した数値資料・地域データ・自作の公開版図・プログラム・手順書である。
