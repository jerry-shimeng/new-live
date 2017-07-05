import json
import traceback

from commons.enums import PublicSourceEnums
from commons.http_utils import HttpUtils
from dbaccess.online_dal import OnlineDAL
from dbaccess.product_dal import ProductDAL
from douban.douban import DoubanContentParser

languages = {'70001': '中文', '70003': '英语', '70000': '俄罗斯','70004':'日语'}


class LeTvMovie:
	@classmethod
	def run(cls,page=1):

		while page>0:
			cls.get_data(cls.get_url(page))
			page = page -1
	
	@classmethod
	def get_url(cls, page=1, size=60):
		api_url = 'http://api.vip.le.com/search/interface?' \
		          'cg=1&src=1&ispay=1&stype=1&stt=1' \
		          '&ps=%d&pn=%d&vt=180001&sc=&ar=&yr=&or=1' % (size, page)
		# cg=1 类型是电影 / ps=60 page size /pn=1 page index / vt=180001 正片
		# yr=2016 是年份过滤
		return api_url
	
	@classmethod
	def get_data(cls, url):
		print(url)
		res = HttpUtils.get(url, headers=HttpUtils.get_header())
		
		result = json.loads(res)
		
		cls.process(result['album_list'])
	
	@classmethod
	def process(cls, ds):
		if ds is None or len(ds) == 0:
			return
		
		for r in ds:
			detail = cls.detail(r)
			if detail is not None and cls.valid(detail):
				try:
					product, detail = OnlineDAL.save(detail, PublicSourceEnums.LETV)
					# 保存成功
					DoubanContentParser.save_categorys(product.id, detail.about)
				except:
					traceback.print_exc()
	@classmethod
	def detail(cls, d):

		if len( d['videoList']) == 0:
			return None

		about = cls.get_about(d)
		video =  d['videoList'][0]
		
		m = {'name': d['name'], 'time': d['releaseDate'], 'online_url': video['url'], 'source': ""}
		
		# "id": model["id"],
		result = {"name": d['name'], "sub_name": d['subname'],
		          "rating": 0, "rating_sum": 0,
		          "image_url":  d['images']['120*160'],
		          "about": about,
		          "content": d['description'], "comments": [], "area": d['areaName'],
		          "images": None, 'score': d['rating']}
		
		r = dict(m, **result)
		
		return r
	
	@classmethod
	def get_about(cls, d):
		
		def value(t):
			s = ''
			for t1 in t:
				s += list(t1.values())[0] + ","
			return s
		
		def lang(no):
			if not isinstance(no, str):
				no = str(no)
			if no in languages.keys():
				return languages[no]
			else:
				print(no)
				return '未知'
		
		def sub(s):
			return s.split(",")

		if len( d['videoList'])>0:
			time =  d['videoList'][0]['releaseDate']
		else:
			time = '0'

		return {
			"categorys": sub(d['subCategoryName']),
			"area": d['areaName'],
			"language": lang(d['language']),
			"director": list(d['directory'].values()),
			"screenwriter": d['screenwriter'],
			"actor": value(d['starring']),
			"time":time,
			"duration": d['duration']
		}
	
	@classmethod
	def valid(cls, d):
		print(d['name'])
		if d['sub_name'].find("购买本片") > 0:
			return False
		if d['sub_name'].find("预告片") > 0 or d['name'].find("预告片") > 0:
			return False
		return True
