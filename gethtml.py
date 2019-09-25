import requests
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

strings = ""
data = {"pageNum": 1, "pageSize": 1028}
url = 'http://data.xinxueshuo.cn/nsi-1.0/school/list.do'
##data = {'username':'testuser1','passwd':'111111'}
r = requests.get(url, params=data)  # 发get请求
# print(r.json()["data"]) #将返回的json串转为字典
list = []
print(len(r.json()["data"]["list"]))
for index in range(len(r.json()["data"]["list"])):
    s = r.json()["data"]["list"][index]["website"]
    school_id = r.json()["data"]["list"][index]["id"]
    print(s)
    # print(s[:4])
    if s != "0":
        list.append(s)

# print(list)
# print(len(list))

for i in range(len(list)):
    if list[i][:4] != "http":
        list[i] = "http://" + list[i]
        strings = strings + list[i] + "---"
# print(list)
# print(len(list))
with open("url.txt", "w") as f:
    f.write(strings)
# for ele in list:
#     if ele[:4] != "http":
#         ele = "http://" + ele
#         print(ele)
# print(list)

# print(r.text)  #返回get到的页面的返回数据
