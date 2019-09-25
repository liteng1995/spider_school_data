# from flask import Flask

# app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()

import requests
from requests import RequestException
from bs4 import BeautifulSoup, Comment
import urllib.request
import urllib.error
import re
from urllib import parse
import os
from posixpath import normpath
import urllib.parse


class school_spider:
    def __init__(self):
        self.list = []
        self.listName = []

    def get_interface(self):
        data = {"pageNum": 1, "pageSize": 1218}
        # 1218
        url = 'http://data.xinxueshuo.cn/nsi-1.0/school/list.do'
        r = requests.get(url, params=data)  # 发get请求
        # list = []
        # listName = []
        for index in range(len(r.json()["data"]["list"])):
            s = r.json()["data"]["list"][index]["website"]
            name = r.json()["data"]["list"][index]["schoolName"]
            if s != "0":
                self.list.append(s)
                self.listName.append(name)
                # print(listName)
        for i in range(len(list)):
            if list[i][:4] != "http":
                list[i] = "http://" + list[i]
        return self.list, self.listName

    def myjoin(self, base, url):
        url1 = urllib.parse.urljoin(base, url)
        arr = urllib.parse.urlparse(url1)
        path = normpath(arr[2])
        return urllib.parse.urlunparse(
            (arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def get_page(self, url):
        try:
            response_encode = ""
            response_decode = ""
            headers = {
                "user-agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=(5, 10))
            response_encode = response.encoding
            print(response_encode)
            print(response.status_code)
            if response.status_code == 200:
                # return response.text
                try:
                    response_decode = response.content.decode('utf8')
                except UnicodeDecodeError:
                    response_decode = response.content.decode('gb18030')
                finally:
                    return response_decode
            return "None"

        except (RequestException, UnicodeDecodeError) as e:
            print(e)
            return "Error"

    def storageToLocalFiles(storagePath, data):
        with open(storagePath, mode='w', encoding='utf-8') as f:
            # with open(storagePath, mode='w') as f:
            f.write(data)


def main(url):
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all("a")
    url_list = []
    strings = ""
    # 网址前缀
    o = urllib.parse.urlparse(url)
    head_url = o[0] + "://" + o[1]
    print(head_url)
    if urls:
        for url2 in urls:
            url2_1 = url2.get("href")
            url2_1 = myjoin(head_url, url2_1)
            url_list.append(url2_1)
            # if url2_1:
            #     if url2_1[0] == "/":
            #         url2_1 = head_url + url2_1
            #         url_list.append(url2_1)
            #         if url2_1[0:24] == head_url:
            #             url2_1 = url2_1
            #             url_list.append(url2_1)
            #         else:
            #             pass
            #     elif url2_1[0] == ".":
            #         url2_1 = url2_1[1:]
            #         print("------" + url2_1)
            #         url2_1 = head_url + url2_1
            #         url_list.append(url2_1)
            #         # if url2_1[0:24] == head_url:
            #         #     url2_1 = url2_1
            #         #     url_list.append(url2_1)
            #         # else:
            #         #     pass
            #     else:
            #         pass
            # else:
            #     pass
    else:
        pass

    print(len(url_list))

    # 获取内容信息
    for url_ in url_list:
        print(url_)
        back_html = get_page(url_)
        soup = BeautifulSoup(back_html, 'html.parser')
        [s.extract() for s in soup("script")]
        [s.extract() for s in soup("style")]
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]
        # back_text = soup.body.strings
        for string in soup.stripped_strings:
            strings = strings + string
            print(string)
    print(len(url_list))
    storagePath = listName[i] + ".txt"
    print(storagePath)
    storageToLocalFiles(storagePath, strings)


if __name__ == '__main__':
    for i in range(len(list)):
        if list[i] == "http://www.ycid.net":
            continue
        # try:
        main(list[i])
    # except UnicodeDecodeError as e:
    #     print("======================" + list[i])
