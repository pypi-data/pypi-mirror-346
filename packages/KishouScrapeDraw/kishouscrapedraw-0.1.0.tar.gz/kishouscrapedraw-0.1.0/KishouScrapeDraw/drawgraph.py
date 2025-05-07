# -*- coding: utf-8 -*-

import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.ticker import MaxNLocator,MultipleLocator,AutoMinorLocator
plt.rcParams["font.size"] = 15

from drowweathersymbol import drow_wind, drow_weather, textToNum, drow_DirectionSymbol
from scraping import getURL
import os

# CSVファイルをインポートしてリストの形式にする
def ImportCSV(csv_file_path):
  with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    print(csvreader)
    csv_data_list = list(csvreader)
  return csv_data_list


# 風速のデータを風力に変換
def VelocityToPower(windVelocity):
  try:
      windVelocity = float(windVelocity)
  except ValueError:
      windVelocity = 0.

  if windVelocity >= 32.7:
    return 12
  elif windVelocity >= 28.5:
    return 11
  elif windVelocity >= 24.5:
    return 10
  elif windVelocity >= 20.8:
    return 9
  elif windVelocity >= 17.2:
    return 8
  elif windVelocity >= 13.9:
    return 7
  elif windVelocity >= 10.8:
    return 6
  elif windVelocity >= 8.0:
    return 5
  elif windVelocity >= 5.5:
    return 4
  elif windVelocity >= 3.4:
    return 3
  elif windVelocity >= 1.6:
    return 2
  elif windVelocity >= 0.3:
    return 1
  else:
    return 0


# 気象要素ごとにリストをディクショナリに保存
def ClassifyWeatherElements(csv_data_list):
  # 気象要素ごとにリストを保持するディクショナリ
  classifyWeatherData = {}

  # '気温(℃)', '相対湿度(％)', '現地気圧(hPa)', '降水量(mm)', '風速(m/s)', '風向', '天気'をリストに保存
  for key in csv_data_list[0]:
    value = csv_data_list[0].index(key)
    classifyWeatherData[key] = [row[value] for row in csv_data_list[1:]]

  # 風速から風力を求めてリストに保存
  classifyWeatherData["風力"] = [VelocityToPower(i) for i in classifyWeatherData["風速(m/s)"]]

  # 時刻をリストに保存
  #classifyWeatherData["時間"] = [row[0] for row in csv_data_list[1]]

  return classifyWeatherData


def upperLimitRangeSelection(num1):
  num2 = round(num1, -1)
  if num2 - num1 == 0:
    return num1
  elif num2 - num1 == 5:
    return num1
  elif num2 - num1 > 0:
    return num2
  elif num2 - num1 < 0:
    return num2 + 5


def lowerLimitRangeSelection(num1):
  num2 = round(num1, -1)
  if num2 - num1 == 0:
    return num1
  elif num2 - num1 == 5:
    return num1
  elif num2 - num1 > 0:
    return num2 - 5
  elif num2 - num1 < 0:
    return num2


# 図を描写する
def draw_weather_elements(year, month, day, place, weatherData, show=False, save_directory="."):
  time = weatherData["時間"]
  temperature = weatherData["気温(℃)"]
  humidity = weatherData["湿度(%)"]
  pressure = weatherData["現地気圧(hPa)"]
  precipitation = weatherData["降水量(mm)"]
  wind_I = weatherData["風力"]
  wind_D = weatherData["風向"]
  weather = weatherData["天気"]


  # 軸の範囲の決定
  if len(temperature) == 0:
    temp_max = 30
  else:
    temp_max = upperLimitRangeSelection(max(temperature))

  temp_min = temp_max - 5 * 5
  humi_max = 100
  humi_min = 0

  if len(pressure) == 0:
    press_min = 1010
  else:
    press_min =lowerLimitRangeSelection(min(pressure))

  press_max = press_min + 5 * 5
  hour_max = 24
  hour_min = 0
  precipitation_max = 50
  precipitation_min = 0
  temp_color = "red"
  humi_color = "blue"
  press_color = "green"

  center_x = 12
  center_y = 0.5
  dia = 0.4
  num_lw = 0.8

  plt.rcParams["font.size"] = 15

  fig = plt.figure(figsize=(10.6, 5.0))
  fig.subplots_adjust(hspace = -0.35, wspace=0.2)

  ax1 = fig.add_subplot(2, 1, 2)


  ax1.set_ylabel("気温 [℃]") # 軸ax1を"y1"と名付ける
  ax1.plot(time,temperature, marker="o",label='気温',color=temp_color,clip_on=False) # y1のデータを共通のx軸に対して青い線でプロット
  ax1.set_xticks(np.arange(0, 24, 3))

  ax2 = ax1.twinx() # ax1と同じx軸を共有する2番目の軸ax2を作成
  ax2.plot(time,humidity, marker="s",label='湿度',color=humi_color,clip_on=False) # y2のデータを共通のx軸に対して赤い線でプロット
  ax2.set_ylabel("湿度 [%]") # 軸ax2を"y2"と名付ける

  ax3 = ax1.twinx() # ax1と同じx軸を共有する3番目の軸ax3を作成
  ax3.plot(time,pressure, marker="^",label=r"気圧",color=press_color,clip_on=False) # y3のデータを共通のx軸に対してシアン線でプロット
  ax3.set_ylabel("気圧 [hPa]") # 軸ax3を"y3"と名付ける
  ax3.spines["right"].set_position(("axes", 1.1)) # 右のy軸ax3を1.1倍だけ右に移動

  ax4 = ax1.twinx()
  ax4.bar(time, precipitation, color='lightblue', clip_on=False, alpha=0.5,label="降水量")
  ax4.set_ylabel("降水量 [mm]")
  ax4.spines["right"].set_position(("axes", 1.22))

  plt.title("気象要素の推移"+"(" + str(year)+"/"+ str(month).zfill(2)+"/" + str(day).zfill(2) + "，" + place + ")", fontsize=15, x=0.5, y=-0.45)

  # 凡例
  # グラフの本体設定時に、ラベルを手動で設定する必要があるのは、barplotのみ。plotは自動で設定される＞
  handler1, label1 = ax1.get_legend_handles_labels()
  handler2, label2 = ax2.get_legend_handles_labels()
  handler3, label3 = ax3.get_legend_handles_labels()
  handler4, label4 = ax4.get_legend_handles_labels()
  # 凡例をまとめて出力する
  ax1.legend(handler1 + handler2 + handler3 + handler4, label1 + label2 + label3 + label4, loc='upper right', bbox_to_anchor=(0.84, -0.1), ncol=4, borderaxespad=0.5)


  ax1.set_xlim([0,25])
  ax1.set_ylim([temp_min,temp_max])
  ax2.set_ylim([humi_min,humi_max])
  ax3.set_ylim([press_min, press_max])
  ax4.set_ylim([precipitation_min, precipitation_max])

  #plt.xticks(np.arange(start, stop, step))
  ax1.set_xticks(np.arange(hour_min, hour_max+1, 3))

  ax1.set_yticks(np.arange(temp_min, temp_max+1, 5))
  ax2.set_yticks(np.arange(humi_min, humi_max+1, 20))#20
  ax3.set_yticks(np.arange(press_min, press_max+1, 5))
  ax4.set_yticks(np.arange(precipitation_min, precipitation_max+1, 10))#20


  # 補助目盛を表示
  ax1.minorticks_on()
  ax2.minorticks_on()
  ax3.minorticks_on()
  ax4.minorticks_on()

  ax2.yaxis.set_minor_locator(AutoMinorLocator(5))

  # グラフの表示順
  ax4.set_zorder(5)
  ax1.set_zorder(2)
  ax2.set_zorder(3)
  ax3.set_zorder(4)


  ax1.xaxis.set_minor_locator(AutoMinorLocator(3))

  # 目盛り線の表示
  ax1.grid(which="major", color="black", alpha=0.5)
  ax1.grid(which="minor", color="gray", linestyle=":")

  ax5 = fig.add_subplot(2, 1, 1)

  ax5.set_xticks(np.arange(0, 24, 3))

  ax5.set_xlim([0,25])
  ax5.set_ylim([-2,2])

  for i, data_time in enumerate(time):
    # 風速・風向の情報を描写する
    drow_wind(ax5, wind_I[i], textToNum(wind_D[i]), data_time, center_y, dia, num_lw)

    # 天気の情報を描写する
    drow_weather(ax5, weather[i], data_time, center_y, dia, num_lw)

  ax5.set_aspect('equal')

  # 方位記号を表示する
  drow_DirectionSymbol(ax5, -1.5, center_y)


  add_qr_with_label(ax5, getURL(place,year,month,day), label="気象庁｜過去の気象データ検索", zoom=0.15,text_size=8)

  # 目盛り線の非表示
  #ax2.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
  ax5.axis('off')

  # 画像を保存
  save_dir = f"{save_directory}/WeatherGraph"
  os.makedirs(save_dir, exist_ok=True)  # ディレクトリがなければ作成
  save_path = os.path.join(save_dir,  'graph_'+place + '_'+ str(year)+ str(month).zfill(2) + str(day).zfill(2)+".png")
  plt.savefig(save_path, bbox_inches='tight',dpi=400)
  print(f"グラフを作成しました。: {save_path}")

  # `show=True` の場合はグラフを表示
  if show:
      plt.show()

  # メモリ解放（`plt.show()` を呼ばない場合、明示的に close する）
  plt.close()

import matplotlib.pyplot as plt
import qrcode
from qrcode.image.pil import PilImage
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, VPacker, TextArea
import io

def add_qr_with_label(ax, url, label="サイト名", position=(0.8, 0.8), fill_color="black", back_color="white", zoom=0.2, text_size=10):
    """
    QRコードとラベル（テキスト）を軸の外に表示する関数。

    Parameters:
    ----------
    ax : matplotlib.axes.Axes
        表示対象の軸。
    url : str
        QRコードに埋め込むURL。
    label : str
        QRコード下部に表示するテキスト。
    position : tuple of float
        位置（figure全体に対する割合）。
    zoom : float
        QRコードの拡大率。
    fill_color : str
        QRコードの色。
    back_color : str
        QRコードの背景色。
    text_size : int
        テキストのフォントサイズ。

    Returns:
    -------
    AnnotationBbox
        配置されたAnnotationBboxオブジェクト。
    """

    # 1. QRコード生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # 2. QRコードをバイトオブジェクトとして読み込み
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    qr_img = plt.imread(buf)

    # 3. OffsetImageとTextAreaを作成
    imagebox = OffsetImage(qr_img, zoom=zoom)
    text = TextArea(label, textprops=dict(color="black", fontsize=text_size, ha='center'))

    # 4. VPackerで画像とテキストを縦に積む
    vbox = VPacker(children=[imagebox, text], align="center", pad=0, sep=5)

    # 5. AnnotationBboxで配置
    ab = AnnotationBbox(vbox, position,
                        xycoords='figure fraction',
                        boxcoords="figure fraction",
                        frameon=False)

    ax.figure.add_artist(ab)