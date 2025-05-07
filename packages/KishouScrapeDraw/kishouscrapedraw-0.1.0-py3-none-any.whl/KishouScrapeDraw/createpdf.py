# -*- coding: utf-8 -*-


import os
import matplotlib.pyplot as plt
from PIL import Image
from fpdf import FPDF
from datetime import datetime, timedelta
import pandas as pd
import shutil
from PyPDF2 import PdfMerger
from datetime import datetime

from fpdf import FPDF
from PIL import Image
import os

def create_a4_pdf_with_map_images_and_graph(map_images, graph_image, output_pdf, header_text=""):
    """
    A4縦サイズのPDFを作成し、天気図の画像を横幅が等間隔になるように並べ、
    気象データのグラフ画像を下部に配置し、グラフ画像を線で囲む。
    すべてのページの右上に指定したテキストを挿入する。

    Args:
        map_images (list of str): 天気図画像のパス（複数）。
        graph_image (str): 気象データのグラフ画像のパス。
        output_pdf (str): 出力するPDFファイル名。
        header_text (str, optional): 各ページの右上に挿入するテキスト（デフォルトは空白）。
    """
    # A4サイズ（mm）
    A4_WIDTH = 210
    A4_HEIGHT = 297

    # PDF作成
    pdf = FPDF(unit="mm", format="A4")

    # 日本語フォントの設定
    font_path = "/usr/share/fonts/truetype/fonts-japanese-mincho.ttf"
    pdf.add_font("JapaneseMincho", fname=font_path, uni=True)
    font_name = "JapaneseMincho"

    def add_new_page(A4_WIDTH, margin, header_text, size=12):
        """新しいページを追加し、右上にテキストを配置"""
        pdf.add_page()
        pdf.set_xy(A4_WIDTH - margin - 50, 10)  # 右上の余白部分に配置
        pdf.set_font(font_name, size=size)
        pdf.cell(50, 10, header_text, align='R')

    def draw_dashed_rect(x, y, width, height):
        """画像を囲む点線の枠を描画"""
        pdf.set_draw_color(120, 120, 120)  # 灰色の線
        pdf.set_line_width(0.05)
        pdf.dashed_line(x, y, x + width, y, dash_length=1, space_length=1)
        pdf.dashed_line(x, y + height, x + width, y + height, dash_length=1, space_length=1)
        pdf.dashed_line(x, y, x, y + height, dash_length=1, space_length=1)
        pdf.dashed_line(x + width, y, x + width, y + height, dash_length=1, space_length=1)

    margin = 10  # 左右マージン
    add_new_page(A4_WIDTH, margin, header_text)

    # 左右マージンと画像間隔
    spacing = 5   # 画像間のスペース

    # 画像の横幅を計算（最大3枚/行）
    max_per_row = 3
    available_width = A4_WIDTH - 2 * margin
    image_width = (available_width - (max_per_row - 1) * spacing) / max_per_row

    y_position = 20  # 上端からの位置（テキストがあるため 20mm に変更）
    row = 0  # 現在の行番号
    image_height = 0  # 直前の画像の高さを記録

    for i, image_path in enumerate(map_images):
        # 画像のリサイズ
        img = Image.open(image_path)
        img_aspect = img.height / img.width
        image_height = image_width * img_aspect

        # Y位置を計算
        new_y_position = 20 + row * (image_height + spacing)

        # ページの範囲を超える場合、新しいページを追加
        if new_y_position + image_height > A4_HEIGHT - margin:
            add_new_page(A4_WIDTH, margin, header_text)
            row = 0
            new_y_position = 20

        # X, Y位置を計算して配置
        x_position = margin + (i % max_per_row) * (image_width + spacing)
        y_position = new_y_position
        pdf.image(image_path, x=x_position, y=y_position, w=image_width, h=image_height)

        # 画像を囲む点線の枠を描画
        draw_dashed_rect(x_position, y_position, image_width, image_height)

        # 行が変わるかチェック
        if (i + 1) % max_per_row == 0:
            row += 1

    # グラフ画像を配置
    if graph_image:
        img = Image.open(graph_image)
        img_aspect = img.height / img.width
        graph_width = available_width
        graph_height = graph_width * img_aspect

        # グラフ画像がページを超える場合、新しいページを追加
        if y_position + image_height + spacing + graph_height > A4_HEIGHT - margin:
            add_new_page(A4_WIDTH, margin, header_text)
            y_position = 20

        graph_x = margin
        graph_y = y_position + image_height + spacing

        # グラフ画像を配置
        pdf.image(graph_image, x=graph_x, y=graph_y, w=graph_width, h=graph_height)

        # グラフ画像を囲む点線の枠を描画
        draw_dashed_rect(graph_x, graph_y, graph_width, graph_height)

    # PDF保存
    pdf.output(output_pdf)

def image_preparation(point, year, month, day, save_directory=".", color_mode="MONO", jst_time="09:00", m=4, n=4, dpi=300, min_size=300, include_caption=True, caption_height_ratio=0.45, days_back=3):
  # 気象庁HPから「〇〇の〇〇〇〇年〇〇月〇〇日」の気象データを読み取ります．
  from scraping import scraping
  All_list = scraping(point,year,month,day)

  # 「〇〇の〇〇〇〇年〇〇月〇〇日」の気象データをCSVデータとして保存します．
  from scraping import savecsv
  savecsv(All_list,point,year,month,day)

  # 「〇〇の〇〇〇〇年〇〇月〇〇日」の気象データを用いてグラフを作成します．
  from drawgraph import ClassifyWeatherElements
  from drawgraph import draw_weather_elements
  classifyWeatherData = ClassifyWeatherElements(All_list)
  draw_weather_elements(year, month, day, point, classifyWeatherData)
  from fetchweathermap import fetch_weather_map
  fetch_weather_map(year, month, day, save_directory, color_mode, jst_time, m, n, dpi, min_size, include_caption, caption_height_ratio, days_back)

  map_images = []
  for i in range(days_back):
    target_date = datetime(year, month, day) - timedelta(days=i)
    target_year = target_date.year
    target_month = target_date.month
    target_day = target_date.day

    # 保存先のファイルパスを生成
    # 年と月を文字列に変換
    year_str = str(target_year)
    month_str = f"{target_month:02d}"
    year_short = year_str[2:]

    file_name = f"map_{year_short}{month_str}{target_day:02d}.png"
    dir_path = f"{save_directory}/WeatherMap_{year_short}{month_str}"
    file_path = os.path.join(dir_path, file_name)

    map_images.insert(0, file_path)

  return map_images

def create_pdf(point, year, month, day, days_back=3, header_text="", output_dir = "./OutputPDF", img_save_dir=".", color_mode="MONO", jst_time="09:00", m=4, n=4, dpi=300, min_size=300, include_caption=True, caption_height_ratio=0.45):
  map_images = image_preparation(point, year, month, day, img_save_dir, color_mode, jst_time, m, n, dpi, min_size, include_caption, caption_height_ratio, days_back)
  graph_image = f"{img_save_dir}/WeatherGraph/graph_{point}_{year}{month:02d}{day:02d}.png"
  os.makedirs(output_dir, exist_ok=True)
  if header_text == "":
    output_pdf = f"{output_dir}/{point}_{year}{month:02d}{day:02d}.pdf"
  else:
    output_pdf = f"{output_dir}/{header_text}_{point}_{year}{month:02d}{day:02d}.pdf"
  create_a4_pdf_with_map_images_and_graph(map_images, graph_image, output_pdf, header_text)
  print(f"PDFを作成しました。: {output_pdf}")
  print(f"PDFをダウンロードして中身を確認してください。")

def merge_pdfs(output_dir):
    """
    出力ディレクトリ内のすべてのPDFを1つのPDFに統合する。
    """
    merger = PdfMerger()
    pdf_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".pdf")])

    for pdf in pdf_files:
        merger.append(os.path.join(output_dir, pdf))

    # 作成日の情報を取得してファイル名に含める
    today_str = datetime.now().strftime("%y%m%d")
    merged_pdf_path = f"{today_str}_merged_output.pdf"

    merger.write(os.path.join(output_dir, merged_pdf_path))
    merger.close()
    print(f"PDFを1つにまとめました。: {merged_pdf_path}")

def create_pdfs_from_csv(csv_file_path, output_dir="./OutputPDFfromCSV", days_back=3, img_save_dir=".", color_mode="MONO", jst_time="09:00", m=4, n=4, dpi=300, min_size=300, include_caption=True, caption_height_ratio=0.45):
    """
    指定されたCSVファイルを読み込み、各行のデータをもとにPDFを生成する関数。

    Args:
        csv_file_path (str): CSVファイルのパス。
        output_dir (str, optional): 生成されたPDFの出力ディレクトリ。デフォルトは "./OutputPDFfromCSV"。
        その他の引数は `create_pdf` 関数に渡される。
    """
    # 出力ディレクトリを空にする
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # CSVファイルの読み込み
    df = pd.read_csv(csv_file_path, dtype={"組・番号": str, "観測所": str})
    df["年"] = pd.to_numeric(df["年"], errors='coerce').fillna(0).astype(int)
    df["月"] = pd.to_numeric(df["月"], errors='coerce').fillna(0).astype(int)
    df["日"] = pd.to_numeric(df["日"], errors='coerce').fillna(0).astype(int)

    # 必要な列を取得
    group_number_list = df["組・番号"].tolist()
    point_list = df["観測所"].tolist()
    year_list = df["年"].tolist()
    month_list = df["月"].tolist()
    day_list = df["日"].tolist()

    # PDFの生成処理
    for group_number, point, year, month, day in zip(group_number_list, point_list, year_list, month_list, day_list):
        if pd.isna(point) or year == 0 or month == 0 or day == 0:
            continue  # 空白がある場合はスキップ
        create_pdf(point, int(year), int(month), int(day), days_back=days_back, header_text=group_number, output_dir=output_dir, img_save_dir=img_save_dir, color_mode=color_mode, jst_time=jst_time, m=m, n=n, dpi=dpi, min_size=min_size, include_caption=include_caption, caption_height_ratio=caption_height_ratio)

    # すべてのPDFを結合
    merge_pdfs(output_dir)

if __name__ == "__main__":
  point  = "鳥取"
  year = 2023
  month = 12
  day = 3
  create_pdf(point, year, month, day, days_back=3, header_text="A0_岸田")

if __name__ == "__main__":
  csv_file_path = "./test.csv"
  create_pdfs_from_csv(csv_file_path)