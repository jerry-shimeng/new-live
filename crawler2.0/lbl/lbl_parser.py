import json
import re

from bs4 import BeautifulSoup

import config
from commons.http_utils import HttpUtils
from dbaccess.db_access import DatabaseAccess
from lbl.common import Common

features = 'lxml'


class LblParser:
    @classmethod
    def run(cls, page):
        while page > 0:
            url = Common.get_url(page)
            cls.process(url)
            page = page - 1

    @classmethod
    def process(cls, url):
        list = cls.get_list(url)
        if list is None:
            return
        for detail in list:
            try:
                model = cls.detail(detail)
                cls.save(model)
            except Exception as e:
                print(e)
                pass

    @classmethod
    def get_list(cls, url):
        html = HttpUtils.get(url, headers=HttpUtils.get_header())
        soup = BeautifulSoup(html, config.features)
        list = soup.find(id="center")
        if list is None:
            return []
        list = list.find_all(class_="postlist")
        return list

    @classmethod
    def detail(cls, data):
        url = data.h4.a["href"]
        return cls.parse_detail(url)

    @classmethod
    def parse_detail(cls, url):

        html = HttpUtils.get(url)
        soup = BeautifulSoup(html, features)

        detail = soup.find(id="center").find(class_="col").find(class_="post")
        # 名字
        name = detail.h2.string
        name = name[name.index("《") + 1:name.index("》")]
        # 验证电影名称是否存在，如存在不继续获取
        if DatabaseAccess.exist_name(name):
            return None
        print(name)

        # 更新时间
        time = detail.find(class_="postmeat").text
        time = time[time.index("：") + 1:time.index("|")]
        # 状态
        status = detail.find(class_="postmeat").span.text

        div = detail.find("div", class_="entry")
        # 下载地址
        down_links = cls.get_download_url(div)

        return {'name': name, 'time': time, 'tag': status, 'down_links': down_links, 'source': url}

    @classmethod
    def get_download_url(cls, div):
        list = []
        list_p = div.find_all("p")
        # 先获取最后一个
        list_p = list_p[::-1]

        for p in list_p:
            a = p.a

            if a is None:
                break
            else:
                reg = r"http://www.lbldy.com/movie/(.+).html"

                if not re.match(reg, a["href"]) is None:
                    continue

                if a["href"].find('http://kuai.xunlei.com') >= 0:
                    continue

                href = cls.process_download_url(a["href"])

                if len(href.strip()) < 10:
                    continue
                if href.find("pan.baidu.com") > 0:
                    href = str(p)
                list.append(href)

        # 字符串列表转换

        return cls.download_url_convert(list)

    @classmethod
    def process_download_url(cls, url):
        url = url.replace("http://www.lbldy.com", "").replace("[www.lbldy.com]", "").replace(
            "&tr=http://www.youjiady.com", "")

        return url

    @classmethod
    def download_url_convert(cls, urls):
        if urls is None or len(urls) == 0:
            return []
        new_urls = {'magnet':[],'thunder':[],'http':[],'baidu':[]}
        for u in urls:
            u = u.strip()
            if u.find('magnet') == 0:
                new_urls['magnet'].append(u)
                continue
            if u.find('thunder') == 0:
                new_urls['thunder'].append(u)
                continue
            if u.find('http') == 0:
                new_urls['http'].append( u)
                continue
            if u.find('<p>') == 0:
                d = cls.process_baidu_yun(u)
                if d is not None:
                    new_urls['baidu'].append(d)
                continue

        return json.dumps(new_urls)

    @classmethod
    def process_baidu_yun(cls, s):
        try:

            s = '<html>' + s + '</html>'

            bf = BeautifulSoup(s, 'lxml')
            # link = bf.strings
            r = list(map(lambda x: str(x), bf.strings))
            link = r[1]
            password = r[2].strip().replace('密码：', '')
            return {'link': link, 'password': password}
        except:
            print('process_baidu_yun error')
            return None

    @classmethod
    def save(cls, d):
        if d is None:
            return

        try:
            DatabaseAccess.save_as_lbl(d)
        except Exception as e:
            print(e)
