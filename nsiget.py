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
from lxml import etree
from retrying import retry


class SchoolSpider(object):
    def __init__(self):
        pass

    def get_interface(self):
        data = {"pageNum": 1, "pageSize": 1218}
        # 1218
        url = 'http://data.xinxueshuo.cn/nsi-1.0/school/list.do'
        r = requests.get(url, params=data)  # 发get请求
        # list = self.list
        # listName = self.listName
        list = []
        listName = []
        for index in range(len(r.json()["data"]["list"])):
            s = r.json()["data"]["list"][index]["website"]
            name = r.json()["data"]["list"][index]["schoolName"]
            if s != "0":
                list.append(s)
                listName.append(name)
                # print(listName)
        for i in range(len(list)):
            if list[i][:4] != "http":
                list[i] = "http://" + list[i]
        return list, listName

    def myjoin(self, base, url):
        url1 = urllib.parse.urljoin(base, url)
        arr = urllib.parse.urlparse(url1)
        path = normpath(arr[2])
        return urllib.parse.urlunparse(
            (arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    @retry(stop_max_attempt_number=3)
    def get_page(self, url):
        try:
            response_encode = ""
            response_decode = ""
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
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

    def storageToLocalFiles(self, storagepath, data):
        with open(storagepath, mode='a', encoding='utf-8') as f:
            # with open(storagePath, mode='w') as f:
            f.write(data)
            f.write("\n\n\n\n\n\n\n\n\n")

    def read_txt(self, storagetpath, storagetpath1):
        try:
            with open(storagetpath, mode="r", encoding='utf-8') as file1:
                tmp = []
                for line in file1:
                    line = line + "\n"
                    tmp.append(line)
                tmp1 = set(tmp)
            with open(storagetpath, mode='w', encoding='utf-8') as file2:
                file2.writelines(tmp1)
        except MemoryError as e:
            with open(storagetpath, mode="r", encoding='utf-8') as file1:
                with open(storagetpath1, mode='a', encoding='utf-8') as file2:
                    lines_seen = set()
                    for line in file1:
                        line = line + "\n"
                        if line not in lines_seen:
                            # with open(storagetpath1, mode='a', encoding='utf-8') as file2:
                            file2.writelines(line)
                            lines_seen.add(line)
            # with open(storagetpath, mode="r", encoding='utf-8') as file1:
            #     lines_seen = set()
            #     for line in file1:
            #         line = line + "\n"
            #         if line not in lines_seen:
            #             with open(storagetpath1, mode='a', encoding='utf-8') as file2:
            #                 file2.writelines(line)
            #             lines_seen.add(line)
            # tmp = file1.read().splitlines()
            # tmp1 = set(tmp)  # 利用内置的列表去重方法工作
            # tmp1 = [tmp + "\n" for tmp in tmp1]  # 给每一行的结尾加一个换行符
        #     tmp = []
        #     for line in file1:
        #         line = line + "\n"
        #         tmp.append(line)
        #     tmp1 = set(tmp)
        #
        # with open(storagetpath, mode='w', encoding='utf-8') as file2:
        #     file2.writelines(tmp1)

    def filter(self, soup):
        [s.extract() for s in soup("script")]
        [s.extract() for s in soup("style")]
        comments = soup.findAll(
            text=lambda text: isinstance(
                text, Comment))
        [comment.extract() for comment in comments]
        return soup

    def run(self):
        list, listname = self.get_interface()
        for i in range(len(list)):
            if list[i] == "http://www.ycid.net":
                continue
            html = self.get_page(list[i])
            # html = etree.HTML(html)
            storagepath = listname[i] + ".txt"
            storagepath1 = listname[i] + "去重版.txt"
            print(storagepath)
            soup = BeautifulSoup(html, 'html.parser')
            urls = soup.find_all("a")
            url_list = []
            strings = ""
            # 网址前缀
            o = urllib.parse.urlparse(list[i])
            head_url = o[0] + "://" + o[1]
            print(head_url)
            # soup = soup.prettify()
            soup = self.filter(soup)
            for string in soup.stripped_strings:
                strings = strings + string + "\n"
            self.storageToLocalFiles(storagepath, strings)
            if urls:
                for url2 in urls:
                    url2_1 = url2.get("href")
                    url2_1 = self.myjoin(head_url, url2_1)
                    url_list.append(url2_1)
            else:
                pass

            print(len(url_list))

            # 获取内容信息
            for url_ in url_list:
                strings = ""
                print(url_)
                back_html = self.get_page(url_)
                # back_html = etree.HTML(back_html)
                soup = BeautifulSoup(back_html, 'html.parser')
                # soup = soup.prettify()
                soup = self.filter(soup)
                for string in soup.stripped_strings:
                    strings = strings + string + "\n"
                    # print(string)
                self.storageToLocalFiles(storagepath, strings)
            print(len(url_list))
            self.read_txt(storagepath, storagepath1)


if __name__ == '__main__':
    school_spider = SchoolSpider()
    school_spider.run()
    # for i in range(len(list)):
    #     if list[i] == "http://www.ycid.net":
    #         continue
    #     # try:
    #     main(list[i])
    # except UnicodeDecodeError as e:
    #     print("======================" + list[i])
