# coding=utf-8
import threading

import time

from douban_parse import DoubanContentParser
from sit_parse import WebSitParser
from sync_data import AsyncData
from url_hub import UrlHub

start_page = 5


def get_new_res():
    url = UrlHub.get_url()
    WebSitParser(url, start_page).run()


def get_douban_info():
    DoubanContentParser.run()


threads = []
t1 = threading.Thread(target=get_new_res)
threads.append(t1)
t2 = threading.Thread(target=get_douban_info)
threads.append(t2)

if __name__ == "__main__":
    # 获取 资源
    for t in threads:
        t.setDaemon(True)
        t.start()

    while True:
        time.sleep(50)
