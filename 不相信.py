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
import pymysql
import datetime
import os
from io import StringIO
from PIL import Image
import json


def get_interface():
    data = {"pageNum": 1, "pageSize": 1218}
    # 1218
    url = 'http://data.xinxueshuo.cn/nsi-1.0/school/list.do'
    r = requests.get(url, params=data)  # 发get请求
    # list = self.list
    # listName = self.listName
    list = []
    listname = []
    listid = []
    for index in range(len(r.json()["data"]["list"])):
        s = r.json()["data"]["list"][index]["website"]
        name = r.json()["data"]["list"][index]["schoolName"]
        listname.append(name)
        school_id = r.json()["data"]["list"][index]["id"]
        listid.append(school_id)
        if s != "0":
            if s[:4] != "http":
                s = "http://" + s
        list.append(s)
    return listid, listname, list


class SchoolSpider:
    def __init__(self, school_name):
        self.school_name = school_name
        self.school_url = "https://www.baidu.com/s?ie=utf-8&tn=baidu&wd={}".format(school_name)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    def get_filter(self, soup):
        [s.extract() for s in soup("script")]
        [s.extract() for s in soup("style")]
        comments = soup.findAll(
            text=lambda text: isinstance(
                text, Comment))
        [comment.extract() for comment in comments]
        return soup

    def parse_url(self, url):
        if url != "0":
            try:
                response_decode = ""
                response = requests.get(url, headers=self.headers, timeout=(5, 10))
                if response.status_code == 200:
                    try:
                        response_decode = response.content.decode('utf-8')
                    except UnicodeDecodeError:
                        response_decode = response.content.decode('gb18030')
                    finally:
                        return response_decode
                return "None"
            except (RequestException, UnicodeDecodeError) as e:
                print(e)
                return "Error"
        else:
            return "null"

    def get_content_list(self, html_str):
        if html_str != "None" or html_str != "Error" or html_str != "null":
            html = etree.HTML(html_str)
            h3_list = html.xpath("//h3[contains(@class,'t')]")
            content_list = []
            for h3 in h3_list:
                item = {}
                item["title"] = h3.xpath("./a/text()")[0] if len(h3.xpath("./a/text()")) > 0 else None
                item["href"] = h3.xpath("./a/@href")[0] if len(h3.xpath("./a/@href")) > 0 else None
                item["detail"] = self.get_content(item["href"])
                content_list.append(item)
            return content_list

    def get_content(self, detail_url):
        # strings2 = ""
        content = self.parse_url(detail_url)
        # soup = BeautifulSoup(content, 'html.parser')
        # soup = self.get_filter(soup)
        # for string in soup.stripped_strings:
        #     strings2 = strings2 + string + "\n"
        html_xml = etree.HTML(content)
        text_list = html_xml.xpath("./html/text()")
        text = "\n".join(text_list)
        return text

    def save_content_list(self, content_list, school_name):
        file_path = school_name + ".txt"
        with open(file_path, mode='a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")

    def run(self):
        school_url = self.school_url
        html_str = self.parse_url(school_url)
        content_list = self.get_content_list(html_str)
        self.save_content_list(content_list, listname[i])


# 1.学校的地址
# 2.发送请求，获取相应
# 3.提取数据
# 3.1提取列表页的地址和标题
# 3.2
# 4.保存数据
# 5.请求下一个学校的地址，循环2—4步
if __name__ == '__main__':
    listid, listname, list = get_interface()
    for i in range(len(list)):
        school_spider = SchoolSpider(listname[i])
        school_spider.run()
