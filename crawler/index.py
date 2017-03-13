# coding=utf-8
from crawler.sit_parse import WebSitParser
from crawler.url_hub import UrlHub

if __name__ == "__main__":
    url = UrlHub.get_url()
    WebSitParser(url).parse_list()
    pass
