import urllib.request
import re
import os
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


def get_interface():
    data = {"pageNum": 1, "pageSize": 1218}
    # 1218
    url = 'http://data.xinxueshuo.cn/nsi-1.0/school/list.do'
    r = requests.get(url, params=data)  # 发get请求
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


def myjoin(base, url):
    url1 = urllib.parse.urljoin(base, url)
    arr = urllib.parse.urlparse(url1)
    path = normpath(arr[2])
    return urllib.parse.urlunparse(
        (arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))


def get_page(url):
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


def run():
    list, listname = get_interface()
    for i in range(len(list)):
        if list[i] == "http://www.ycid.net":
            continue
        html = get_page(list[i])
        soup = BeautifulSoup(html, 'html.parser')
        urls = soup.find_all("a")
        url_list = []
        strings = ""
        o = urllib.parse.urlparse(list[i])
        head_url = o[0] + "://" + o[1]
        print(head_url)
        if urls:
            for url2 in urls:
                url2_1 = url2.get("href")
                url2_1 = myjoin(head_url, url2_1)
                url_list.append(url2_1)
        else:
            pass
        # 获取内容信息
        for url_ in url_list:
            print(url_)
            url2_list = []
            back_html = get_page(url_)
            soup = BeautifulSoup(back_html, 'html.parser')
            urlss = soup.find_all("a")
            if urlss:
                for url3 in urlss:
                    url3_1 = url3.get("href") or url3.get("HREF")
                    url3_1 = myjoin(head_url, url3_1)
                    url2_list.append(url3_1)
            else:
                pass
            url_list.extend(url2_list)
        print(len(url_list))
        for pdf_url in url_lst:
            url_lst = getUrl(pdf_url)
            if url_lst:
                getFile(url_lst[0])
            else:
                pass


# compile the regular expressions and find
# all stuff we need
def getUrl(html):
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    url_re = re.compile(reg)
    url_lst = re.findall(url_re, html)
    return (url_lst)


def getFile(url):
    file_name = url.split('/')[-1]
    print(file_name)
    # u = get_page(url)
    u = requests.get(url)
    if not os.path.exists('ldf_download'):
        os.mkdir('ldf_download')
    os.chdir(os.path.join(os.getcwd(), 'ldf_download'))
    with open(file_name, mode='wb', encoding='utf-8') as f:
        f.write(u.content)
    # u = urllib.request.urlopen(url)
    # f = open(file_name, 'wb')

    # block_sz = 8192
    # while True:
    #     buffer = u.read(block_sz)
    #     if not buffer:
    #         break
    #
    #     f.write(buffer)
    # f.close()
    print("Sucessful to download" + " " + file_name)


# root_url = 'https://www.bcis.cn'
#
# raw_url = 'https://www.bcis.cn/admissions/tuition-fees'
# list, listname = get_interface()
# html = getHtml(raw_url)
# url_lst = getUrl(html)
# if not os.path.exists('ldf_download'):
#     os.mkdir('ldf_download')
# os.chdir(os.path.join(os.getcwd(), 'ldf_download'))
#
# for url in url_lst[:]:
#     print(url)
#     url = root_url + url
#     getFile(url)


if __name__ == '__main__':
    run()
