# KishouScrapeDraw

**KishouScrapeDraw** は、気象庁（JMA）の気象データと天気図をもとに、グラフやPDFレポートを生成できる教育向けPythonパッケージです。

気象探究・理科の授業などでの活用を想定し、**日本語対応・PDF出力・一括処理**など、実用的な機能を備えています。

---

## 🚀 主な機能（4つ）

### ✅ 機能①：1日の気象要素の変化を取得・グラフ化

- 指定した観測地点と日付の気温・気圧・湿度・降水量などを取得
- 多軸グラフとして1枚の画像に描画
- 観測地点は日本全国に対応（気象庁のデータ使用）

```python
from drawgraph import DrawWeatherElements
DrawWeatherElements(year=2023, month=12, day=1, point="鳥取", classifyWeatherData=True)
```

出力例（保存先）：`WeatherGraph/graph_鳥取_20231201.png`

---

### ✅ 機能②：天気図のダウンロード・分割・保存

- 気象庁から天気図（実況図・日々の天気図）を自動取得
- PDFまたはPNG形式に対応
- 1日ごとに画像をトリミングして保存

```python
from fetchweathermap import fetch_weather_map
fetch_weather_map(year=2023, month=12, day=1)
```

出力例（保存先）：`WeatherMap_2312/map_231201.png`

---

### ✅ 機能③：気象グラフと天気図を統合したPDFレポートを作成

- グラフと天気図を1ページにまとめたA4縦型のPDFを自動生成
- 日本語フォント対応・QRコード付き
- 教員や生徒の個人レポート用に最適

```python
from createpdf import create_pdf
create_pdf(point="鳥取", year=2023, month=12, day=1)
```

出力例：`OutputPDF/鳥取_20231201.pdf`

---

### ✅ 機能④：複数人分のPDFを一括生成（CSV対応）

- 生徒名簿CSV（組・番号／地点／日付）から複数PDFを自動出力
- 各PDFに個別のファイル名を付けて保存

```python
from createpdf import create_pdfs_from_csv
create_pdfs_from_csv("students.csv")
```

CSVファイル例：

```
組・番号,観測所,年,月,日
A1_田中,東京,2024,11,15
B2_鈴木,大阪,2024,11,16
```

出力例：`OutputPDF/A1_田中_東京_20241115.pdf`

---

## 📦 インストール方法

```bash
pip install KishouScrapeDraw
```

※ Python 3.8 以上推奨

---

## 🛠 システム前提条件（Linux / Google Colab）

天気図の画像変換や日本語PDF生成には、以下の外部ツールが必要です：

```bash
sudo apt-get update
sudo apt-get install -y poppler-utils ghostscript fonts-ipafont
```

---

## 📚 依存ライブラリ（pipで自動インストールされます）

- matplotlib, japanize_matplotlib
- pandas, numpy
- fpdf, PyPDF2, pdf2image
- requests
- opencv-python-headless
- qrcode[pil]

---

## 🧑‍🏫 開発者

- **S.Kishida**（<s.kishida98@gmail.com>）

---

## 📄 ライセンス

MIT License

---

## 🔗 GitHubリポジトリ

https://github.com/surugukishida/KishouScrapeDraw
