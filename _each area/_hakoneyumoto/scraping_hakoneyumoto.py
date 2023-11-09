import requests
from bs4 import BeautifulSoup
import pandas as pd

# リンクのリスト
links = [
"https://www.jalan.net/yad307128/kuchikomi/?screenId=UWW3001&yadNo=307128&minPrice=0&maxPrice=999999&rootCd=7701&stayMonth=&dateUndecided=1&stayYear=&stayDay=&callbackHistFlg=1&smlCd=141602&distCd=01&ccnt=lean-kuchikomi-tab"
,"https://www.jalan.net/yad307128/kuchikomi/archive/?maxPrice=999999&rootCd=7701&screenId=UWW3701&smlCd=141602&dateUndecided=1&minPrice=0&yadNo=307128&callbackHistFlg=1&distCd=01"
,"https://www.jalan.net/yad356061/kuchikomi/?screenId=UWW3001&yadNo=356061&stayMonth=&dateUndecided=1&stayYear=&stayDay=&minPrice=0&maxPrice=999999&rootCd=7701&callbackHistFlg=1&smlCd=141602&distCd=01&ccnt=lean-kuchikomi-tab"
,"https://www.jalan.net/yad356061/kuchikomi/archive/?maxPrice=999999&rootCd=7701&screenId=UWW3701&smlCd=141602&dateUndecided=1&minPrice=0&yadNo=356061&callbackHistFlg=1&distCd=01"
,"https://www.jalan.net/yad341306/kuchikomi/?screenId=UWW3001&yadNo=341306&minPrice=0&maxPrice=999999&rootCd=7701&stayMonth=&dateUndecided=1&stayYear=&stayDay=&callbackHistFlg=1&smlCd=141602&distCd=01&ccnt=lean-kuchikomi-tab"
,"https://www.jalan.net/yad341306/kuchikomi/archive/?maxPrice=999999&rootCd=7701&screenId=UWW3701&smlCd=141602&dateUndecided=1&minPrice=0&yadNo=341306&callbackHistFlg=1&distCd=01"
]

# 空のリストを用意
l = []

# 各リンクに対してループ
for link in links:
    if "archive" in link:  # リンクがタイプ②の場合
        for i in range(1, 100):  # この範囲は実際のページ数に合わせて調整してください
            if i == 1:
                url = link
            else:
                idx_value = (i-1) * 30
                base_url = link.split("archive/")[0]
                yad_no = link.split("&yadNo=")[1].split("&")[0]
                additional_params = link.split("yadNo=" + yad_no)[1]
                url = f"{base_url}archive/{i}.HTML?yadNo={yad_no}{additional_params}"

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            body = soup.find_all("p", {"class": "jlnpc-kuchikomiCassette__postBody"})
            date = soup.find_all("p", {"class": "jlnpc-kuchikomiCassette__postDate"})
            
            for d, b in zip(date, body):
                data = {}
                data["口コミ"] = b.text
                data["投稿日"] = d.text.replace('投稿日：', '')
                l.append(data)

    else:  # リンクがタイプ①の場合
        for i in range(1, 100):  # この範囲は実際のページ数に合わせて調整してください
            if i == 1:
                url = link
            else:
                base_url = link.split("?")[0]
                additional_params = link.split(base_url)[1]
                url = f"{base_url}/{i}.HTML{additional_params}"

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            body = soup.find_all("p", {"class": "jlnpc-kuchikomiCassette__postBody"})
            date = soup.find_all("p", {"class": "jlnpc-kuchikomiCassette__postDate"})
            
            for d, b in zip(date, body):
                data = {}
                data["口コミ"] = b.text
                data["投稿日"] = d.text.replace('投稿日：', '')
                l.append(data)

# データフレームを作成
df = pd.DataFrame(l)

# 重複する口コミを削除
df = df.drop_duplicates(subset='口コミ')

# CSVに保存
df.to_csv("箱根湯本.csv", encoding='utf_8_sig')

# データフレームを表示
print(df)