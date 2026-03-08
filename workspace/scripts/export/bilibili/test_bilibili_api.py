#!/usr/bin/env python3
# 测试B站API返回结构

import os
import requests

uid = "700153046"
sessdata = "2b458069%2C1785389602%2Cb850a%2A11CjBBPhS0cy4jU-8xTaWvgBoqxcIaH9PABHW-OCwbFjZma0nq8eLMnNB1y0T0QM-JPVUSVmJNaXVkWHkxM2NaYnZlbFcyT0Z5T0xWb0VIam9lb2ZHNFlwcFg1ejhuakVvbG01MWs2Q3JKV2ZNN3VlT29pZ05UdklUZmhVYTNhZjU1WTEzbzAxVkFBIIEC"

url = "https://api.bilibili.com/x/v3/fav/folder/list4navigate"
params = {'up_mid': uid}
headers = {
    'Cookie': f'SESSDATA={sessdata}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, params=params, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"\n=== 返回数据 ===")
print(response.text)
