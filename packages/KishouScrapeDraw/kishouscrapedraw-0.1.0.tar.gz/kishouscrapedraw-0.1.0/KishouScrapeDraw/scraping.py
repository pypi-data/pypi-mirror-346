# -*- coding: utf-8 -*-

place_codeA = [11,11,12,13,13,14,15,16,16,16,17,17,17,18,19,20,20,21,21,22,23,24,31,31,31,31,32,33,33,33,34,34,35,35,35,36,36,36,36,40,40,41,41,42,43,43,44,44,44,44,44,44,50,45,45,45,45,46,48,48,48,48,48,49,49,50,50,50,50,50,50,51,51,52,52,53,53,53,53,54,54,54,55,55,56,56,57,57,60,61,61,62,63,63,63,63,64,65,65,66,66,67,67,67,68,68,68,69,69,69,71,72,72,73,73,74,74,74,74,81,81,81,82,82,83,83,84,84,84,84,84,84,85,86,86,86,87,87,87,87,88,88,88,88,88,88,88,91,91,91,91,91,91,91,91]
place_codeB = [47401,47402,47407,47404,47406,47412,47413,47411,47433,47421,47405,47435,47409,47420,47418,47417,47440,47424,47423,47426,47430,47428,47576,47575,47574,47581,47582,47584,47585,47512,47592,47590,47587,47520,47588,47595,47570,47597,47598,47629,47646,47690,47615,47624,47626,47641,47662,47675,47677,47678,47971,47991,47639,47648,47682,47674,47672,47670,47610,47622,47618,47620,47637,47638,47640,47657,47668,47656,47654,47655,47666,47636,47653,47617,47632,47684,47649,47651,47663,47602,47604,47612,47606,47607,47600,47605,47616,47631,47761,47750,47759,47772,47747,47769,47770,47776,47780,47777,47778,47756,47768,47767,47765,47766,47740,47741,47755,47742,47744,47746,47895,47891,47890,47887,47892,47893,47899,47897,47898,47754,47784,47762,47809,47807,47814,47815,47800,47805,47812,47817,47818,47843,47813,47819,47824,47838,47822,47830,47829,47835,47823,47827,47831,47837,47836,47909,47942,47940,47929,47936,47945,47927,47912,47917,47918]
place_name = ["稚内", "北見枝幸", "旭川", "羽幌", "留萌", "札幌", "岩見沢", "小樽", "倶知安", "寿都", "雄武", "紋別", "網走", "根室", "釧路", "帯広", "広尾", "苫小牧", "室蘭", "浦河", "函館", "江差", "むつ", "青森", "深浦", "八戸", "秋田", "盛岡", "宮古", "大船渡", "石巻", "仙台", "酒田", "新庄", "山形", "福島", "若松", "白河", "小名浜", "水戸", "つくば", "奥日光", "宇都宮", "前橋", "熊谷", "秩父", "東京", "大島", "三宅島", "八丈島", "父島", "南鳥島", "富士山", "銚子", "千葉", "勝浦", "館山", "横浜", "長野", "軽井沢", "松本", "諏訪", "飯田", "甲府", "河口湖", "三島", "網代", "静岡", "浜松", "御前崎", "石廊崎", "名古屋", "伊良湖", "高山", "岐阜", "四日市", "上野", "津", "尾鷲", "相川", "新潟", "高田", "伏木", "富山", "輪島", "金沢", "福井", "敦賀", "彦根", "舞鶴", "京都", "大阪", "豊岡", "姫路", "神戸", "洲本", "奈良", "和歌山", "潮岬", "津山", "岡山", "福山", "広島", "呉", "西郷", "松江", "浜田", "境", "米子", "鳥取", "徳島", "高松", "多度津", "松山", "宇和島", "高知", "室戸岬", "宿毛", "清水", "萩", "山口", "下関", "飯塚", "福岡", "日田", "大分", "厳原", "平戸", "佐世保", "長崎", "雲仙岳", "福江", "佐賀", "熊本", "人吉", "牛深", "延岡", "宮崎", "都城", "油津", "阿久根", "鹿児島", "枕崎", "種子島", "屋久島", "名瀬", "沖永良部", "名護", "久米島", "那覇", "南大東", "宮古島", "与那国島", "西表島", "石垣島"]

import requests
from bs4 import BeautifulSoup
import csv
import os

# URLで年と月ごとの設定ができるので%sで指定した英数字を埋め込めるようにします。
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=%s&view=p1"

#取ったデータをfloat型に変えるやつ。(データが取れなかったとき気象庁は"/"を埋め込んでいるから0に変える)
def str2float(str):
  try:
    return float(str)
  except:
    return 0.0


#天気をよみとる
def getweather(row):
  try:
    return row.find('img').get('alt')
  except:
    return ""

def getURL(place,year,month,day):
  index = place_name.index(place)
  return base_url%(place_codeA[index], place_codeB[index], year, month, day)

#ある場所の1日のデータをスクレイピング
def scraping(place,year,month,day):
  try:
    #最終的にデータを集めるリスト (下に書いてある初期値は一行目。つまり、ヘッダー。)
    All_list = [['年月日', '時間', '現地気圧(hPa)', '降水量(mm)', '気温(℃)', '湿度(%)', '風速(m/s)', '風向' ,'天気']]

    r = requests.get(getURL(place,year,month,day))
    r.encoding = r.apparent_encoding

    # まずはサイトごとスクレイピング
    soup = BeautifulSoup(r.text,"lxml")
    # findAllで条件に一致するものをすべて抜き出します。
    # 今回の条件はtrタグでclassがmtxになってるものです。
    rows = soup.findAll('tr',class_='mtx')

    # 表の最初の1~4行目はカラム情報なのでスライスする。(indexだから初めは0だよ)
    rows = rows[2:]

  # 1日〜最終日までの１行を網羅し、取得します。
    for row in rows:
    # 今度はtrのなかのtdをすべて抜き出します
      data = row.findAll('td')
      #print(data)
      #１行の中には様々なデータがあるので全部取り出す。
      # ★ポイント
      rowData = [] #初期化
      rowData.append(str(year) + "/" + str(month) + "/" + str(day))
      rowData.append(str2float(data[0].string))
      rowData.append(str2float(data[1].string))
      rowData.append(str2float(data[3].string))
      rowData.append(str2float(data[4].string))
      rowData.append(str2float(data[7].string))
      rowData.append(str2float(data[8].string))
      rowData.append(data[9].string)
      rowData.append(getweather(row))

      #次の行にデータを追加
      All_list.append(rowData)

    return All_list

  except:
    print(f"スクレイピング先のサイトのURL: {getURL(place,year,month,day)}")
    print("errorが発生しました；" + __name__)


#スクレイピングしたデータをCSVに保存
def savecsv(All_list,place,year,month,day,save_directory="."):
  save_dir = f"{save_directory}/WeatherCSV"
  os.makedirs(save_dir, exist_ok=True)  # ディレクトリがなければ作成
  save_path = os.path.join(save_dir, place + '_'+ str(year)+ str(month).zfill(2) + str(day).zfill(2) + '.csv')
  try:
    #都市ごとにデータをファイルを新しく生成して書き出す。(csvファイル形式。名前は都市名)
    with open(save_path, 'w') as file:
      writer = csv.writer(file, lineterminator='\n')
      writer.writerows(All_list)
      print(f"スクレイピング先のサイトのURL: {getURL(place,year,month,day)}")
      print(f"スクレイピングしたデータをCSVとして保存しました。: {save_path}")

  except:
    print(f"スクレイピング先のサイトのURL: {getURL(place,year,month,day)}")
    print("errorが発生しました；" + __name__)


if __name__ == "__main__":
  #都市を網羅します
  place  = "鳥取"
  print(place)
  year = 1998
  month = 12
  day = 3
  All_list = scraping(place,year,month,day)
  savecsv(All_list,place,year,month,day)