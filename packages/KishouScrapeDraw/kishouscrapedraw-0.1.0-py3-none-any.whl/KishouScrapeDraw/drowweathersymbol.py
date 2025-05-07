# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def textToNum(text_Direction):
  try:
    if text_Direction == "北":
      return 0 / 16 * 360
    elif text_Direction == "北北西":
      return 1 / 16 * 360
    elif text_Direction == "北西":
      return 2 / 16 * 360
    elif text_Direction == "西北西":
      return 3 / 16 * 360
    elif text_Direction == "西":
      return 4 / 16 * 360
    elif text_Direction == "西南西":
      return 5 / 16 * 360
    elif text_Direction == "南西":
      return 6 / 16 * 360
    elif text_Direction == "南南西":
      return 7 / 16 * 360
    elif text_Direction == "南":
      return 8 / 16 * 360
    elif text_Direction == "南南東":
      return 9 / 16 * 360
    elif text_Direction == "南東":
      return 10 / 16 * 360
    elif text_Direction == "東南東":
      return 11 / 16 * 360
    elif text_Direction == "東":
      return 12 / 16 * 360
    elif text_Direction == "東北東":
      return 13 / 16 * 360
    elif text_Direction == "北東":
      return 14 / 16 * 360
    elif text_Direction == "北北東":
      return 15 / 16 * 360

  except:
    print("errorが発生しました；" + __name__)



def rot_Coordinate(x_start, y_start, x_end, y_end, center_x, center_y, degree):
  # 始座標(x_start, y_start)から終座標(x_end, y_end)の線分を中心(center_x, center_y)でdegree度回転させる
  # 回転後の線分の始座標と終座標を出力する

  # (degree)度回転行列を作成
  theta = np.radians(degree)
  rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

  # 線分を回転
  start_point_rotated = np.dot(rotation_matrix, np.array([x_start - center_x, y_start - center_y])) + np.array([center_x, center_y])
  end_point_rotated = np.dot(rotation_matrix, np.array([x_end - center_x, y_end - center_y])) + np.array([center_x, center_y])

  # 回転後の線分の始座標と終座標を出力
  return [start_point_rotated, end_point_rotated]



def drow_WeatherMapSymbols(weather, windPower, deg_Direct, center_x, center_y, dia):
  plt.clf()
  fig, ax = plt.subplots()
  ax.set_xlim(-5, 5)
  ax.set_ylim(-5, 5)

  # 風速・風向の情報を描写する
  drow_wind(ax, windPower, deg_Direct, center_x, center_y, dia)

  # 天気の情報を描写する
  drow_weather(ax, weather, center_x, center_y, dia)

  ax.set_aspect('equal')
  ax.axis('off')



def windPower1(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw):
  # 中心から伸びる長い線を描写
  mm = rot_Coordinate(center_x, center_y, center_x, center_y + dia/2 * (2 + 1), center_x, center_y, deg_Direct)
  line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth = num_lw, edgecolor='black')
  ax.add_patch(line)

  # 内側の羽を描写
  for num in range(1,2):
    mm = rot_Coordinate(center_x, center_y + dia/2 * (num + 1), center_x, center_y + dia/2 * (num + 1) +dia*0.6, center_x, center_y + dia/2 * (num + 1), -60)
    mm = rot_Coordinate(mm[0][0], mm[0][1], mm[1][0], mm[1][1], center_x, center_y, deg_Direct)
    line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)



def windPower2_6(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw):
  # 中心から伸びる長い線を描写
  mm = rot_Coordinate(center_x, center_y, center_x, center_y + dia/2 * (windPower + 1), center_x, center_y, deg_Direct)
  line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
  ax.add_patch(line)

  # 最も外側の羽の線を描写
  mm = rot_Coordinate(center_x, center_y + dia/2 * (windPower + 1), center_x, center_y + dia/2 * (windPower + 1) +dia*1, center_x, center_y + dia/2 * (windPower + 1), -60)
  mm = rot_Coordinate(mm[0][0], mm[0][1], mm[1][0], mm[1][1], center_x, center_y, deg_Direct)
  line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
  ax.add_patch(line)

  # 内側の羽を描写
  for num in range(1,windPower):
    mm = rot_Coordinate(center_x, center_y + dia/2 * (num + 1), center_x, center_y + dia/2 * (num + 1) +dia*0.6, center_x, center_y + dia/2 * (num + 1), -60)
    mm = rot_Coordinate(mm[0][0], mm[0][1], mm[1][0], mm[1][1], center_x, center_y, deg_Direct)
    line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)



def windPower7_12(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw):
  # 風力6を描写
  windPower2_6(ax, 6, deg_Direct, center_x, center_y, dia, num_lw)

  # 最も外側の羽の線を描写
  mm = rot_Coordinate(center_x, center_y + dia/2 * (6 + 1), center_x, center_y + dia/2 * (6 + 1) +dia*1, center_x, center_y + dia/2 * (6 + 1), 60)
  mm = rot_Coordinate(mm[0][0], mm[0][1], mm[1][0], mm[1][1], center_x, center_y, deg_Direct)
  line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
  ax.add_patch(line)

  # 内側の羽を描写
  for num in range(5, 12-windPower, -1):
    mm = rot_Coordinate(center_x, center_y + dia/2 * (num + 1), center_x, center_y + dia/2 * (num + 1) +dia*0.6, center_x, center_y + dia/2 * (num + 1), 60)
    mm = rot_Coordinate(mm[0][0], mm[0][1], mm[1][0], mm[1][1], center_x, center_y, deg_Direct)
    line = patches.ConnectionPatch((mm[0][0], mm[0][1]), (mm[1][0], mm[1][1]), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)




def drow_wind(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw):
  if windPower == 1:
    windPower1(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw)

  elif windPower >= 2 and windPower <= 6:
    windPower2_6(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw)

  elif windPower >= 7 and windPower <= 12:
    windPower7_12(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw)



def drow_weather(ax, weather, center_x, center_y, dia, num_lw):
  # weatherには文字列"clear","sunny", "cloudy", "rainy"

  if weather == "快晴":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)

  elif weather == "晴れ" or  weather == "薄曇":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    line = patches.ConnectionPatch((center_x, center_y + dia*0.5), (center_x, center_y - dia*0.5), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)

  elif weather == "曇":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    circle = patches.Circle((center_x, center_y), dia*0.25, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)

  elif weather == "雨" or weather == "しゅう雨" or weather == "しゅう雪":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='black', linewidth=num_lw)
    ax.add_patch(circle)

  elif weather == "霧":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    circle = patches.Circle((center_x, center_y), dia*0.2, edgecolor='black', facecolor='black', linewidth=num_lw)
    ax.add_patch(circle)

  elif weather == "みぞれ":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    line = patches.ConnectionPatch((center_x + dia*0.5, center_y), (center_x - dia*0.5, center_y), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    mm = rot_Coordinate(center_x + dia*0.5, center_y, center_x - dia*0.5, center_y, center_x, center_y, 60)
    line = patches.ConnectionPatch(mm[0], mm[1], coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    mm = rot_Coordinate(center_x + dia*0.5, center_y, center_x - dia*0.5, center_y, center_x, center_y, 120)
    line = patches.ConnectionPatch(mm[0], mm[1], coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    wedge = patches.Wedge(center=(center_x, center_y), r=dia*0.5, theta1=180, theta2=360, edgecolor='none', facecolor='black', alpha=1)
    ax.add_patch(wedge)

  elif weather == "雪" or weather == "しゅう雪":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    line = patches.ConnectionPatch((center_x + dia*0.5, center_y), (center_x - dia*0.5, center_y), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    mm = rot_Coordinate(center_x + dia*0.5, center_y, center_x - dia*0.5, center_y, center_x, center_y, 60)
    line = patches.ConnectionPatch(mm[0], mm[1], coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    mm = rot_Coordinate(center_x + dia*0.5, center_y, center_x - dia*0.5, center_y, center_x, center_y, 120)
    line = patches.ConnectionPatch(mm[0], mm[1], coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)

  elif weather == "雷":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    line = patches.ConnectionPatch((center_x + dia*0.5, center_y), (center_x - dia*0.5, center_y), coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    wedge = patches.Wedge(center=(center_x, center_y), r=dia*0.5, theta1=180, theta2=360, edgecolor='none', facecolor='black', alpha=1)
    ax.add_patch(wedge)

  elif weather == "あられ":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    cp = patches.CirclePolygon((center_x, center_y), dia * 0.5 ,resolution=3, edgecolor="black", facecolor="white", linewidth=num_lw)
    ax.add_patch(cp)

  elif weather == "ひょう":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    cp = patches.CirclePolygon((center_x, center_y), dia * 0.5 ,resolution=3, edgecolor="black", facecolor="black",linewidth=num_lw)
    ax.add_patch(cp)

  elif weather == "天気不明":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='white', linewidth=num_lw)
    ax.add_patch(circle)
    mm = rot_Coordinate(center_x + dia*0.5, center_y, center_x - dia*0.5, center_y, center_x, center_y, 45)
    line = patches.ConnectionPatch(mm[0], mm[1], coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)
    mm = rot_Coordinate(center_x + dia*0.5, center_y, center_x - dia*0.5, center_y, center_x, center_y, 135)
    line = patches.ConnectionPatch(mm[0], mm[1], coordsA='data', coordsB='data', arrowstyle='-', linewidth=num_lw, edgecolor='black')
    ax.add_patch(line)

  elif weather == "霧雨":
    circle = patches.Circle((center_x, center_y), dia*0.5, edgecolor='black', facecolor='black', linewidth=num_lw)
    ax.add_patch(circle)
    plt.text(center_x + dia*0.7, center_y - dia*0.7, "ki" )

def drow_DirectionSymbol(ax, center_x, center_y, scale = 0.4, num_lw = 0.8):
  line = patches.FancyArrowPatch((center_x - scale, center_y), (center_x + scale, center_y),shrinkA = 0, shrinkB = 0, arrowstyle='-', lw=num_lw, edgecolor='black',clip_on=False)
  ax.add_patch(line)

  line = patches.FancyArrowPatch((center_x, center_y - scale), (center_x, center_y + scale*2.5), shrinkA = 0, shrinkB = 0,arrowstyle='-', lw=num_lw , edgecolor='black',clip_on=False)
  ax.add_patch(line)

  line = patches.FancyArrowPatch((center_x, center_y + scale*2.5), (center_x - scale*0.5, center_y + scale*1.5),shrinkA = 0, shrinkB = 0, arrowstyle='-', lw=num_lw , edgecolor='black',clip_on=False)
  ax.add_patch(line)

  line = patches.FancyArrowPatch((center_x - scale*0.5, center_y + scale*1.5), (center_x + scale*0.4, center_y + scale*1.3),shrinkA = 0, shrinkB = 0 ,arrowstyle='-', lw=num_lw , edgecolor='black',clip_on=False)
  ax.add_patch(line)

if __name__ == "__main__":
  windPower = 3
  deg_Direct = 90
  weather = "霧雨"
  center_x = 12
  center_y = 0
  dia = 0.3
  num_lw = 0.8

  # 図を描写する
  plt.clf()
  fig, ax = plt.subplots(figsize=(14, 3)) # 新しいグラフfigと軸ax1を定義する
  ax.set_xticks(np.arange(0, 25, 3))

  ax.set_xlim([0,24])
  ax.set_ylim([-2,2])

  # 風速・風向の情報を描写する
  drow_wind(ax, windPower, deg_Direct, center_x, center_y, dia, num_lw)

  # 天気の情報を描写する
  drow_weather(ax, weather, center_x, center_y, dia, num_lw)

  ax.set_aspect('equal')

  # 目盛り線の非表示
  ax.axis('on')

  plt.show()