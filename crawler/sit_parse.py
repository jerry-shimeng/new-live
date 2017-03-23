# coding=utf-8
import re
from bs4 import BeautifulSoup
import time
from db_access import DatabaseAccess
from douban_parse import DoubanContentParser
from http_utility import HttpUtility

# 使用的解析器
features = "lxml"


# 第二页地址 http://www.lbldy.com/movie/page/2/

class WebSitParser:
    def __init__(self, url):
        self.url = url
        pass

    # 获取电影列表
    def parse_list(self, page=1):
        url = self.url
        if page != 0:
            url = self.url + "page/%d/" % page
        print(url, end="\n")

        h = HttpUtility(url)
        html = h.get()
        soup = BeautifulSoup(html, features)
        list = soup.find(id="center").find_all(class_="postlist")

        # 没有数据的时候结束
        if list is None or len(list) == 0:
            return
        for l in list:
            self.parse_about(l)
            time.sleep(1)
        # 递归获取数据
        self.parse_list(page + 1)
        pass

    # 获取电影简介
    def parse_about(self, about):
        name = about.h4.a["title"]
        url = about.h4.a["href"]
        self.parse_detail(url)
        pass

    # 获取电影详情
    def parse_detail(self, url):
        h = HttpUtility(url)
        html = h.get()
        soup = BeautifulSoup(html, features)

        detail = soup.find(id="center").find(class_="col").find(class_="post")
        # 名字
        name = detail.h2.string
        name = name[name.index("《") + 1:name.index("》")]

        # 验证电影名称是否存在，如存在不继续获取
        if DatabaseAccess.exist_name(name):
            return

        # 更新时间
        time = detail.find(class_="postmeat").text
        time = time[time.index("：") + 1:time.index("|")]
        # 状态
        status = detail.find(class_="postmeat").span.text
        # 图片
        imgs = detail.find_all("img")
        img = ""
        if len(imgs) > 0:
            # print(imgs[0])
            img = imgs[0]["src"]

        div = detail.find("div", class_="entry")
        # 下载地址
        down_links = self.get_download_url(div)

        # 豆瓣上获取详情
        result = DoubanContentParser(name).start()

        #  获取内容
        content, about = self.get_content(div)
        print(name, time, status, img, content, about, down_links, result, end="\n \n \n")

        self.save(result, name=name, time=time, tag=status, image_url=img, content=content, about=about,
                  down_links=down_links)
        pass

    def get_download_url(self, div):

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

                href = self.process_download_url(a["href"])
                # print(href)
                if len(href.strip()) < 10:
                    continue
                if href.find("pan.baidu.com") > 0:
                    href = p
                list.append(href)
                pass

        return list

    def get_content(self, div):

        isContent = True
        about = ""
        list_p = div.find_all("p")
        content = ""
        for p in list_p:
            if not p.img is None:
                isContent = False
                continue
            if isContent:
                content = content + p.text
            else:
                s = p.text
                if len(s) < 10:
                    break
                else:
                    about = about + s

        about = self.process_content(about)
        return content, about

    def process_content(self, content):
        # 电影下载 http://www.lbldy.com/ 在线电影 http://www.youjiady.com/
        content = content.replace("电影下载", "").replace("@电影下载", "").replace("在线电影", "").replace("@在线电影", "").replace(
            "@在线电影",
            "").replace(
            "http://www.lbldy.com", "").replace("http://www.youjiady.com", "").replace("下载地址：", "").replace("龙部落",
                                                                                                            "").replace(
            "龙太子", "")

        return content

    def process_download_url(self, url):
        # 不能取消的地址 http://xz.66vod.net:889/2016/%E8%8E%AB%E6%96%AF%E7%A7%91%E9%99%B7%E8%90%BD.720p.HD%E4%BF%AE%E6%AD%A3%E4%B8%AD%E5%AD%97[www.66ys.tv].mp4.torrent
        url = url.replace("http://www.lbldy.com", "").replace("[www.lbldy.com]", "").replace(
            "&tr=http://www.youjiady.com", "")
        return url

    def save(self, result, **d_map):

        data_map = {}
        if result is None:
            data_map = d_map
        else:
            data_map = dict(d_map, **result)
            pass
        try:
            DatabaseAccess.save(data_map)
        except Exception as e:
            print(e)
        pass
