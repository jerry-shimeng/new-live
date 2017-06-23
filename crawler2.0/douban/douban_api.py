import json
import traceback

import httplib2
from bs4 import BeautifulSoup

# api doc https://developers.douban.com/wiki/?title=movie_v2#subject
import config
from commons import utils
from dbaccess.db_models import ProductInfo
from logger_proxy import logger

base_url = "https://api.douban.com"
search_url = base_url + "/v2/movie/search?q=%s"
detail_url = base_url + "/v2/movie/subject/%d"


# 评论接口不可用
# comment_url = base_url + "/v2/movie/subject/%s/comments"


class DoubanApi:
    @classmethod
    def get_movie(cls, m: ProductInfo) -> object:

        """
        获取电影的公共信息
        :rtype: object
        """
        logger.info("douban source %s", m.product_name)
        result = cls.start(m.product_name)
        return result

    @classmethod
    def start(cls, name: str):

        id = cls.search(name)
        # print(id)
        if id <= 0:
            return None

        res = cls.detail(id)
        return res

    @classmethod
    def get(cls, url):

        """
        http请求公共函数
        :param url:
        :return:
        """
        http = httplib2.Http()

        headers = dict()
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        headers[
            "Cookie"] = 'll="108296"; bid=39emvg4Fy5U; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1490075263%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DoErbS-KqLWVrkGxsKUBvvgGx6OPkrAbIrMV-lp0BKQIbwNvkW7mvI4_x40D0aYr-myfC25BGRTeF006RakGarK%26wd%3D%26eqid%3Dffb46cf60002fc900000000658cfb031%22%5D; _vwo_uuid_v2=5DD8628BA737EC9F2AF13BE5DC8DCEFF|798f0581c8fbef5f60eb92196d4962f6; __utmt=1; _pk_id.100001.8cb4=803be523dd8f0bb3.1487313761.11.1490076190.1490073088.; _pk_ses.100001.8cb4=*; __utma=30149280.891910915.1483680709.1490073077.1490075263.13; __utmb=30149280.5.10.1490075263; __utmc=30149280; __utmz=30149280.1490006078.11.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'

        h, content = http.request(url, headers=headers)
        return content.decode("utf-8")

    @classmethod
    def search(cls, name):
        """
        在豆瓣上搜索该电影名
        :rtype: object 返回该电影的豆瓣id
        """
        url = search_url % name
        content = cls.get(url)
        obj = json.loads(content)
        if "total" in obj.keys() and obj["total"] == 0:
            logger.info("not result for ", name)
            return 0

        if 'subjects' not in obj:
            print(obj)
            return 0

        for a in obj["subjects"]:
            if name.__contains__(a["title"]) or a["title"].__contains__(name):
                # print(a["id"])
                return int(a["id"])
        return 0

    @classmethod
    def detail(cls, id: int):
        """
        豆瓣电影的公共信息详情
        :rtype: object
        """
        if id == 0:
            return None

        url = detail_url % id
        content = cls.get(url)
        model = json.loads(content)
        name = model["title"]
        sub_name = model["original_title"]
        rating = json.dumps(model["rating"])
        rating_sum = model["ratings_count"]
        image_url = model["images"]["large"]
        content = model["summary"]
        area = "/".join(model["countries"])

        about, comments = cls.get_other(model["alt"])

        result = {"id": model["id"], "name": name, "sub_name": sub_name, "rating": rating, "rating_sum": rating_sum,
                  "image_url": image_url, "about": json.dumps(utils.convert_html_to_json(about)),
                  "content": content, "comments": comments, "area": area, "images": None}
        return result

    @classmethod
    def get_other(cls, url: str):
        """
        其他的信息，如简介和评论信息
        :param url:
        :return:
        """
        try:
            html = cls.get(url)
            soup = BeautifulSoup(html, config.features)
            # 获取内容
            content = soup.find(id="content")

            return cls.get_about(content), cls.get_comments(content)
        except:
            return '', []

    @classmethod
    def get_comments(cls, content):
        """
        电影的评论top5
        :param content:
        :return:
        """
        items = content.find(id="hot-comments").find_all(class_="comment-item")
        comments = []
        for item in items:
            comment_content = item.find("div").p.string
            tag = item.find("div").find(class_="comment-info")
            user_name = tag.a.string
            time = tag.find(class_="comment-time ")["title"]
            comments.append({"content": comment_content, "user_name": user_name, "comment_time": time})

        return comments

    @classmethod
    def get_about(cls, content):
        """
        电影的简介信息，把html格式一并抓下来
        :param content:
        :return:
        """
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
