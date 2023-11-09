import pandas as pd
import re


data = pd.read_csv("強羅/強羅.csv", encoding="utf-8")


garbled_str = "晹壆偵壏愹偺敿業揤晽楥晅偒丅偺尵梩偵桿傢傟偰棙梡偟傑偟偨丅晹壆偺瀢偺壏愹業揤晽楥偼丄尒偨"
data_cleaned = data[~data['口コミ'].str.contains('|'.join(garbled_str), na=False)]



japanese_pattern = r'[ぁ-んァ-ン一-龥]'
data_cleaned = data_cleaned[data_cleaned['口コミ'].apply(lambda x: bool(re.search(japanese_pattern, str(x))))]


data_cleaned.to_csv("強羅_整形済み.csv", index=False, encoding="utf-8")