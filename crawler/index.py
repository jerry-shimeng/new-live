# coding=utf-8
import threading

import time
import traceback

from douban_api import DoubanApi
from douban_parse import DoubanContentParser
from proxy_parser import ProxyParser
from sit_parse import WebSitParser
from sync_data import AsyncData
from url_hub import UrlHub

start_page = 2


def get_new_res():
	try:
		url = UrlHub.get_url()
		WebSitParser(url, start_page).run()
	except:
		traceback.print_exc()
		print("get_new_res recall")
		get_new_res()


def get_douban_info():
	try:
		# DoubanContentParser.run()
		DoubanApi.run()
	except:
		traceback.print_exc()
		print("get_douban_info recall")
		get_douban_info()


threads = []
t1 = threading.Thread(target=get_new_res)
threads.append(t1)
t2 = threading.Thread(target=get_douban_info)
threads.append(t2)

if __name__ == "__main__":
	ProxyParser.run()
	
	# 获取 资源
	for t in threads:
		t.setDaemon(True)
		t.start()
	
	while True:
		time.sleep(4*3600)
