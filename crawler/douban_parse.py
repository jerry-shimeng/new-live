import traceback

from bs4 import BeautifulSoup

from crawler.http_utility import HttpUtility

features = "lxml"


class DoubanContentParser:
    search_url = "https://www.douban.com/search?q=%s"

    def __init__(self, name):
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
        result_list = soup.find(class_="result-list").find_all(class_="result")
        # print(len(result_list))
        if len(result_list) > 0:
            for result in result_list:
                content = result.find(class_="content").find(class_="title")
                name = content.h3.a.string
                if content.h3.span.string == "[电影]":
                    detail_url = content.h3.a["href"]
                    # print(name, detail_url)
                    return self.detail_page(detail_url)

        return None

    def detail_page(self, url):
        html = HttpUtility(url).get()
        soup = BeautifulSoup(html, features)

        content = soup.find(id="content")
        name = self.get_name(content)

        rating = 0
        if not content.find(class_="rating_num") is None:
            rating = content.find(class_="rating_num").string

        rating_sum_tag = content.find(class_="rating_sum").a.span
        rating_sum = 0
        if not rating_sum_tag is None:
            rating_sum = rating_sum_tag.string

        image_url = content.find(id="mainpic").a.img["src"]
        about = self.get_about(content)

        desc = None
        if not content.find(id="link-report") is None and not content.find(id="link-report").span is None:
            desc = content.find(id="link-report").span.string
            if not desc is None:
                desc = desc.strip()

        comments = self.get_comments(content)

        result = {"sub_name": name, "rating": rating, "rating_sum": rating_sum, "image_url": image_url, "about": about,
                  "content": desc, "comments": comments, "images": None}
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


if __name__ == "__main__":
    r = DoubanContentParser("克里斯汀").start()
    print(r)
