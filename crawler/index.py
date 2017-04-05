# coding=utf-8
from douban_parse import DoubanContentParser
from sit_parse import WebSitParser
from sync_data import AsyncData
from url_hub import UrlHub

start_page = 41


if __name__ == "__main__":
    # 获取 资源
    # url = UrlHub.get_url()
    # WebSitParser(url).parse_list(start_page)
    DoubanContentParser.run()
    #sync data
    #AsyncData.start()