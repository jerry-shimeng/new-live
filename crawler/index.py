# coding=utf-8

from sit_parse import WebSitParser
from url_hub import UrlHub

start_page = 51


if __name__ == "__main__":
    # 获取 资源
    url = UrlHub.get_url()
    WebSitParser(url).parse_list(start_page)
    #DoubanContentParser.run()
