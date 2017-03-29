# coding=utf-8
from douban_parse import DoubanContentParser
from sit_parse import WebSitParser
from url_hub import UrlHub

start_page = 100


if __name__ == "__main__":
    # url = UrlHub.get_url()
    # WebSitParser(url).parse_list(start_page)
    DoubanContentParser.run()
