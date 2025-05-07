# -*- coding: utf-8 -*-

#if __name__ == "__main__":
  # Google Colab環境を前提としています

  # 必要なPythonライブラリのインストール
  #!pip install matplotlib pandas numpy fpdf requests pdf2image opencv-python-headless japanize_matplotlib

  # 必要なシステムパッケージのインストール
  #!apt-get update
  #!apt-get install -y poppler-utils ghostscript

  # 日本語フォント（IPAフォント）のインストール
  #!apt-get install -y fonts-ipafont

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta, timezone
import os
import cv2
import subprocess
from pdf2image import convert_from_path

def check_weather_map_exists(year, month, day, save_directory="."):
    """指定されたディレクトリ内に天気図が保存されているか確認"""
    year_str = str(year)
    year_short = year_str[2:]
    path = f"{save_directory}/map_{year_short}{month:02d}{day:02d}.png"
    return os.path.exists(path)

def convert_to_utc(jst_datetime):
    """日本標準時 (JST) を UTC に変換"""
    jst = timezone(timedelta(hours=9))
    utc = timezone(timedelta(hours=0))
    return jst_datetime.replace(tzinfo=jst).astimezone(utc)

def fetch_weather_map_png(year, month, day, save_directory=".", color_mode="MONO", jst_time="09:00"):
    """指定された年、月、日の天気図pngを取得"""
    # 気象庁等から天気図画像をダウンロードする処理
    jst_date = datetime.strptime(f"{year}-{month:02d}-{day:02d} {jst_time}", "%Y-%m-%d %H:%M")
    utc_date = convert_to_utc(jst_date)
    formatted_date = utc_date.strftime("%Y%m%d%H%M")
    formatted_date_short = formatted_date[:6]  # 先頭6文字を取得

    # カラーかモノクロの選択
    color_mode = color_mode.upper()  # COLOR または MONO
    if color_mode not in ["COLOR", "MONO"]:
        raise ValueError("無効な color_mode です。'COLOR' または 'MONO' を選択してください。")

    # URLを構築
    base_url = f"https://www.data.jma.go.jp/yoho/data/wxchart/quick/{formatted_date_short}/SPAS_{color_mode}_{formatted_date}.png"

    year_str = str(year)
    year_short = year_str[2:]
    os.makedirs(save_directory, exist_ok=True)
    image_path = f"{save_directory}/map_{year_short}{month:02d}{day:02d}.png"

    response = requests.get(base_url)
    if response.status_code == 200:
        with open(image_path, "wb") as file:
            file.write(response.content)
        return image_path
    else:
        if not os.listdir(save_directory):  # ディレクトリが空か確認
            os.rmdir(save_directory)  # 空のディレクトリを削除
        return None  # URLが見つからない場合

def fetch_weather_map_pdf(year, month, save_directory="."):
    """指定された年と月の「日々の天気図」PDFをダウンロード"""
    year_short = str(year)[2:]

    # URLのフォーマットに基づいてリンクを生成
    base_url = "https://www.data.jma.go.jp/fcd/yoho/data/hibiten/{year}/{year_short}{month:02d}.pdf"
    url = base_url.format(year=year, year_short=year_short, month=month)

    # 保存するファイル名を設定
    file_name = f"{year}{month:02d}.pdf"
    save_path = f"{save_directory}/{file_name}"
    os.makedirs(save_directory, exist_ok=True)

    try:
        # PDFデータをダウンロード
        response = requests.get(url)
        response.raise_for_status()  # エラーがあれば例外を発生

        # ファイルをバイナリモードで保存
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"PDFを正常にダウンロードしました: {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        if os.path.exists(save_path):
            os.remove(save_path)  # 部分的にダウンロードされたファイルを削除
        raise

def extract_images_from_pdf(pdf_dir, output_dir, year, month, m=4, n=4, dpi=300, min_size=300, include_caption=False, caption_height_ratio=0.45):
    """
    PDFから画像を抽出し、ファイル名に年・月・日を基にした名前を付けて保存します。

    Args:
        pdf_dir (str): PDFファイルが格納されているディレクトリ。
        output_dir (str): 抽出した画像を保存するディレクトリ。
        year (int): 年（4桁）。
        month (int): 月（整数値）。
        m (int): 縦方向の分割数（デフォルト: 4）。
        n (int): 横方向の分割数（デフォルト: 4）。
        dpi (int): PDFを画像としてレンダリングする際の解像度（デフォルト: 300）。
        min_size (int): 抽出する画像領域の最小サイズ（ピクセル単位、デフォルト: 300）。
        include_caption (bool): キャプションを含めるかどうか（デフォルト: False）。
        caption_height_ratio (float): キャプションの高さの比率（画像の高さに対する割合、デフォルト: 0.45）。

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    # 年と月を文字列に変換
    year_str = str(year)
    month_str = f"{month:02d}"

    # PDFファイル名を生成
    pdf_filename = f"{year_str}{month_str}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    # 再生成されたPDFファイルのパス
    fixed_pdf_path = os.path.join(output_dir, f"{year_str}{month_str}_fixed.pdf")

    # Ghostscriptコマンドでフォントを代用してPDFを再生成
    gs_command = [
        "gs", "-o", fixed_pdf_path, "-sDEVICE=pdfwrite", "-dEmbedAllFonts=true", "-dPDFSETTINGS=/prepress",
        "-sFONTPATH=/usr/share/fonts/truetype:/usr/share/fonts/truetype/ipafont",
        "-f", pdf_path
    ]
    subprocess.run(gs_command, check=True)

    # 再生成されたPDFを画像としてレンダリング
    pages = convert_from_path(fixed_pdf_path, dpi=dpi)

    # 年の下2桁を取得
    year_short = year_str[2:]

    # ページごとに処理
    for page_num, page_image in enumerate(pages):
        # 一時ファイルとして保存
        temp_image_path = f"{output_dir}/page_{page_num + 1}.png"
        page_image.save(temp_image_path, "PNG")

        # OpenCVで画像を読み込み
        image = cv2.imread(temp_image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 画像領域を検出（閾値処理 + 輪郭抽出）
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 画像サイズを取得
        img_height, img_width = image.shape[:2]
        cell_height = img_height / m  # 1セルの高さ
        cell_width = img_width / n   # 1セルの幅

        # 検出された領域を処理
        for idx, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            # 最小サイズのフィルタリング（小さいノイズを除外）
            if w > min_size and h > min_size:
                # キャプションを含める場合の高さを計算
                caption_height = int(h * caption_height_ratio) if include_caption else 0
                cropped_image = image[y-int(h*0.01):y+h+caption_height+int(h*0.01), x-int(w*0.01):x+w+int(w*0.02)]

                # 中心座標を計算（キャプションを考慮）
                center_x = x + w / 2
                center_y = y + (h + caption_height) / 2

                # セル番号を計算
                cell_row = int(center_y // cell_height)
                cell_col = int(center_x // cell_width)
                cell_number = cell_row * n + cell_col  # 左上から数えた番号（0スタート）

                # ページ番号に応じたセル番号の調整
                if page_num == 0:
                    final_cell_number = cell_number  # 1ページ目はそのまま
                else:
                    final_cell_number = page_num * m * n + cell_number  # 2ページ目以降

                cell_number_formatted = f"{final_cell_number:02d}"  # 2桁にフォーマット

                # 画像ファイルとして保存
                output_image_path = f"{output_dir}/map_{year_short}{month_str}{cell_number_formatted}.png"
                cv2.imwrite(output_image_path, cropped_image)
                print(f"画像を保存: {output_image_path}")

def fetch_weather_map(year, month, day, save_directory=".", color_mode="MONO", jst_time="09:00", m=4, n=4, dpi=300, min_size=300, include_caption=True, caption_height_ratio=0.45, days_back=3, overwrite = False,show=False, s_width=300):
    """天気図を取得 (PNG または PDF形式)"""
    from datetime import datetime, timedelta

    try:
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

            # ファイルが既に存在するか確認
            if check_weather_map_exists(target_year, target_month, target_day, dir_path) and overwrite == False:
                print(f"{target_year}-{target_month:02d}-{target_day:02d}: 天気図が既に存在します: {file_path}")
                continue
            elif check_weather_map_exists(target_year, target_month, target_day, dir_path) and overwrite == True:
                print(f"{target_year}-{target_month:02d}-{target_day:02d}: 天気図が既に存在しますが、上書きして新たに保存します。: {file_path}")

            # PNG形式の天気図を試みる
            png_path = fetch_weather_map_png(target_year, target_month, target_day, dir_path, color_mode, jst_time)
            if png_path:
                print(f"{target_year}-{target_month:02d}-{target_day:02d}: 「過去の実況天気図」から天気図のPNGファイルを取得しました: {png_path}")
            else:
                print(f"{target_year}-{target_month:02d}-{target_day:02d}: 「過去の実況天気図」から天気図のPNGファイルが見つかりません。「日々の天気図」からPDFの取得を試みます。")
                # PDF形式の天気図をダウンロード
                pdf_path = fetch_weather_map_pdf(target_year, target_month, dir_path)
                print(f"{target_year}-{target_month:02d}-{target_day:02d}: 「日々の天気図」からPDFを取得しました: {pdf_path}")
                # 保存先フォルダ名を生成
                extract_images_from_pdf(dir_path, dir_path, target_year, target_month, m, n, dpi, min_size, include_caption, caption_height_ratio)

    except Exception as e:
        print(f"「日々の天気図」からPDFの取得に失敗しました: {e}")
        print(f"{year}年{month}月{day}日の天気図について，「天気図【全号まとめ】 - 国立国会図書館デジタルコレクション」を探してみてください：https://dl.ndl.go.jp/pid/12896309")
        raise

    print("すべての天気図の取得が完了しました。")

    if show:
        display_map_image(year, month, day, save_directory, days_back, width=s_width)

# 指定されたフォルダ内から 'map_YYMMDD.png' フォーマットの画像を探して縦に表示します
import os
from datetime import datetime, timedelta
from IPython.display import display
from PIL import Image as PILImage
from IPython.display import Image as IPImage
import io

def display_map_image(year, month, day, save_directory=".",days_back=3, width=300):
    """
    年と月に応じたフォルダ内から 'map_YYMMDD.png' フォーマットの画像を探して縦に順番に表示する関数。
    days_backで指定された日数分、さかのぼって画像を表示します。

    Args:
        year (int): 年（4桁または下2桁）
        month (int): 月（2桁）
        day (int): 日（2桁）
        days_back (int, optional): さかのぼる日数。デフォルトは3。
        width (int, optional): 表示する各画像の幅（ピクセル単位）。デフォルトは600。
    """
    # 基準日を作成
    base_date = datetime(year=2000 + (year % 100), month=month, day=day)

    for i in range(days_back):
        current_date = base_date - timedelta(days=i)
        year_short = current_date.year % 100
        month_short = current_date.month
        day_short = current_date.day

        folder_name = f"{save_directory}/WeatherMap_{year_short:02d}{month_short:02d}"
        filename = f"map_{year_short:02d}{month_short:02d}{day_short:02d}.png"
        file_path = os.path.join(folder_name, filename)

        print(f"ファイルパス: {file_path}")  # 画像を表示する前にパスを出力

        if os.path.exists(file_path):
            img = PILImage.open(file_path)
            aspect_ratio = img.height / img.width
            new_height = int(width * aspect_ratio)
            img = img.resize((width, new_height))
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            display(IPImage(data=buffer.getvalue()))
        else:
            print(f"ファイルが見つかりませんでした: {file_path}")

if __name__ == "__main__":
  fetch_weather_map(2009,12,1)