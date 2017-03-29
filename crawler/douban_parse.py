import re
import traceback

import time

import bs4
from bs4 import BeautifulSoup

from db_access import DatabaseAccess
from http_utility import HttpUtility

features = "lxml"

douban_sorce = "douban"


class DoubanContentParser:
    search_url = "https://www.douban.com/search?q=%s"
    sub_search_url = "https://movie.douban.com/subject_search?search_text=%s"

    @classmethod
    def run(cls):
        # 获取数据源非豆瓣的list（size=10）
        list = DatabaseAccess.get_product_by_source(douban_sorce)
        # print(list)
        while list is not None and len(list) > 0:
            for l in list:
                result = cls(l.product_name).start()
                if result is None:
                    continue
                try:
                    DatabaseAccess.save_as_douban(l, result, douban_sorce)
                except Exception as e:
                    print(e)
            time.sleep(10)
            cls.run()

    def __init__(self, name):
        self.movie_name = name
        self.search_url = self.search_url % name
        pass

    def start(self):
        try:
            return self.search_result()
        except Exception as e:
            traceback.print_exc()
            return None

    def search_result(self):
        html = HttpUtility(self.search_url).get()
        # print(content)
        soup = BeautifulSoup(html, features)
        # print(soup)

        result_list = soup.find(class_="result-list")

        if result_list:
            seach_list = result_list.find_all(class_="result")
            if len(seach_list) > 0:
                for result in seach_list:
                    content = result.find(class_="content").find(class_="title")
                    name = content.h3.a.string
                    # 名字验证
                    # if content.h3.span.string == "[电影]" and name.find(self.movie_name) >= 0:
                    if content.h3.span.string == "[电影]":
                        detail_url = content.h3.a["href"]
                        # print(name, detail_url)
                        return self.detail_page(detail_url)
        elif soup.find(id="content"):
            # 找table
            tables = soup.find(id="content").find_all("table")
            if tables and len(tables) > 0:
                a = tables[0].find("a")
                if a:
                    return self.detail_page(a["href"])

        return None

    def detail_page(self, url):
        html = HttpUtility(url).get()
        soup = BeautifulSoup(html, features)
        # 获取内容
        content = soup.find(id="content")
        # 获取sub_name
        name = self.get_name(content)
        # 评分
        rating = 0
        if not content.find(class_="rating_num") is None:
            rating = content.find(class_="rating_num").string
        # 评分人数
        rating_sum_tag = content.find(class_="rating_sum").a.span
        rating_sum = 0
        if not rating_sum_tag is None:
            rating_sum = rating_sum_tag.string

        # 海报
        image_url = content.find(id="mainpic").a.img["src"]
        # 电影信息
        about = self.get_about(content)
        # 电影播放/拍摄 国家
        area = self.get_area(content)
        # 简介
        desc = None
        if not content.find(id="link-report") is None and not content.find(id="link-report").span is None:
            desc = content.find(id="link-report").find(class_="all")
            con = ""
            if desc is None:
                con = content.find(id="link-report").span.string
            else:
                for tag in desc.contents:
                    if type(tag) is bs4.element.NavigableString:
                        con = con + tag.string
            if not con is None:
                con = con.strip()
        # 影评
        comments = self.get_comments(content)

        result = {"sub_name": name, "rating": rating, "rating_sum": rating_sum, "image_url": image_url, "about": about,
                  "content": con, "comments": comments, "area": area, "images": None}
        return result

    def get_name(self, content):
        spans = content.h1.find_all("span")
        name = ""
        for span in spans:
            name = name + span.string
        return name

    def get_about(self, content):
        about = content.find(id="info")
        # print(type(about))
        a_list = about.find_all("a")
        for a in a_list:
            if a["href"].find("/celebrity/") >= 0 or a["href"].find("/search/"):
                s = a.string
                parent = a.parent

                if not parent is None and parent.name != 'div':
                    parent.clear()
                    parent.append(s)
        # 去除超链接
        return str(about)

    def get_comments(self, content):
        items = content.find(id="hot-comments").find_all(class_="comment-item")
        comments = []
        for item in items:
            comment_content = item.find("div").p.string
            tag = item.find("div").find(class_="comment-info")
            user_name = tag.a.string
            time = tag.find(class_="comment-time ")["title"]
            comments.append({"content": comment_content, "user_name": user_name, "comment_time": time})

        return comments

    def get_area(self, content):
        a = content.find(id="info")
        a = str(a)
        pattern = re.compile('<span class="pl">制片国家/地区:</span>(.+)<br/>')
        r = pattern.search(a)
        are = ""
        if r:
            are = r.group(1)
        # print(r, are, "<<<<<<<<<<<<<<<<<<<<")
        return are


if __name__ == "__main__":
    r = DoubanContentParser("下流祖父").start()
    print(r)
