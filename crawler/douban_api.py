import json
import traceback

import httplib2
import time
from bs4 import BeautifulSoup

# api doc https://developers.douban.com/wiki/?title=movie_v2#subject
from db_access import DatabaseAccess
from db_model import ProductInfo
from logger_proxy import logger
from proxy_parser import ProxyParser

base_url = "https://api.douban.com"
search_url = base_url + "/v2/movie/search?q=%s"
detail_url = base_url + "/v2/movie/subject/%d"
# 评论接口不可用
# comment_url = base_url + "/v2/movie/subject/%s/comments"

douban_sorce = "douban"
features = "lxml"


class DoubanApi:
	@classmethod
	def run(cls):
		list = DatabaseAccess.get_product_by_source(douban_sorce)
		# print(len(list))
		if list is not None and len(list) > 0:
			for l in list:
				logger.info("douban source %s ", l.product_name)
				result = cls.start(l.product_name)
				if result is None:
					logger.warn("not found  ", l.product_name)
					DatabaseAccess.update_fail(l.id)
					time.sleep(60)
				else:
					try:
						cls.save_db(l, result)
					except Exception as e:
						traceback.print_exc()
						logger.error("save_db error", result["name"])
						# 更新状态为3，获取源数据失败
						DatabaseAccess.update_fail(l.id)
				
				time.sleep(20)
		
		list = None
		time.sleep(10)
		cls.run()
	
	@classmethod
	def start(cls, name):
		try:
			id = cls.search(name)
			res = cls.detail(id)
			return res
		except Exception as e:
			traceback.print_exc()
			logger.error("get detail error", name)
			return None
	
	@classmethod
	def get(cls, url):
		
		proxy = ProxyParser.get()
		http = httplib2.Http(proxy_info=httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL,
		                                                   proxy["host"], proxy["port"]))
		
		# http = httplib2.Http()
		headers = dict()
		headers[
			"User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
		headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
		headers[
			"Cookie"] = 'll="108296"; bid=39emvg4Fy5U; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1490075263%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DoErbS-KqLWVrkGxsKUBvvgGx6OPkrAbIrMV-lp0BKQIbwNvkW7mvI4_x40D0aYr-myfC25BGRTeF006RakGarK%26wd%3D%26eqid%3Dffb46cf60002fc900000000658cfb031%22%5D; _vwo_uuid_v2=5DD8628BA737EC9F2AF13BE5DC8DCEFF|798f0581c8fbef5f60eb92196d4962f6; __utmt=1; _pk_id.100001.8cb4=803be523dd8f0bb3.1487313761.11.1490076190.1490073088.; _pk_ses.100001.8cb4=*; __utma=30149280.891910915.1483680709.1490073077.1490075263.13; __utmb=30149280.5.10.1490075263; __utmc=30149280; __utmz=30149280.1490006078.11.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
		
		# ProxyParser
		
		h, content = http.request(url, headers=headers)
		ProxyParser.save(proxy["host"], proxy["port"])
		return content.decode("utf-8")
	
	@classmethod
	def search(cls, name):
		url = search_url % name
		content = cls.get(url)
		obj = json.loads(content)
		if "total" in obj.keys() and obj["total"] == 0:
			logger.info("not result for ", name)
			return
		
		for a in obj["subjects"]:
			if name.__contains__(a["title"]) or a["title"].__contains__(name):
				# print(a["id"])
				return int(a["id"])
		return 0
	
	@classmethod
	def detail(cls, id):
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
		          "image_url": image_url, "about": about,
		          "content": content, "comments": comments, "area": area, "images": None}
		return result
	
	@classmethod
	def get_other(cls, url):
		html = cls.get(url)
		soup = BeautifulSoup(html, features)
		# 获取内容
		content = soup.find(id="content")
		
		return cls.get_about(content), cls.get_comments(content)
	
	@classmethod
	def get_comments(cls, content):
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
	
	@classmethod
	def save_db(cls, product, result):
		# product.product_name = result["name"]
		DatabaseAccess.save_as_douban(product, result, douban_sorce)
		pass


if __name__ == "__main__":
	product = ProductInfo()
	product.product_name = "入场券"
	id = DoubanApi.search(product)
	res = DoubanApi.detail(id)
	DoubanApi.save_db(product, res)
	logger.info(res)
