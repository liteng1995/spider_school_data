import urllib.request
import re
import os


# open the url and read
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    page.close()
    return html


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
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print("Sucessful to download" + " " + file_name)


root_url = 'https://www.bcis.cn'

raw_url = 'https://www.bcis.cn/admissions/tuition-fees'

html = getHtml(raw_url)
url_lst = getUrl(html)
if not os.path.exists('ldf_download'):
    os.mkdir('ldf_download')
os.chdir(os.path.join(os.getcwd(), 'ldf_download'))

for url in url_lst[:]:
    print(url)
    url = root_url + url
    getFile(url)
