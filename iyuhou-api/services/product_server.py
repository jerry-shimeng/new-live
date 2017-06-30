from flask import json

from common import utils, result
from dal.db import ProductInfoDal, ProductMovieDAL


class Products:
	@classmethod
	def get_detail(cls, pid: int) -> dict:
		# 获取概况
		pro = ProductInfoDal.get(pid)
		
		if utils.is_blank(pro):
			return result.success()
		
		# 获取详情
		detail = ProductMovieDAL.get(pro['detail'])
		
		if utils.is_blank(detail):
			return result.success()
		
		res = {
			'id': pro['id'],
			'area': detail['area'],
			'imgs': ProductInfoDal.get_img(pid),
			'name': detail['product_name'],
			'alias': detail['product_alias'],
			'summary': detail['content'],
			'score': json.loads(detail['rating']) if detail['rating'] is not None and len(detail['rating']) > 0 else 0,
			'release_time': str(detail['release_time']),
			# 'category': [],
			'about': cls.process_about(detail['about']),
			'online': False
		}
		return result.of(res)
	
	@classmethod
	def get(cls, pid: int) -> object:
		# 获取概况
		pro = ProductInfoDal.get(pid)
		
		if utils.is_blank(pro):
			return None
		
		# 获取详情
		detail = ProductMovieDAL.get(pro['detail'])
		
		if utils.is_blank(detail):
			return None
		
		res = {
			'id': pro['id'],
			'area': detail['area'],
			'img': cls.get_main_image(ProductInfoDal.get_img(pid)),
			'name': detail['product_name'],
			'alias': detail['product_alias'],
			'summary': detail['content'],
			'score': cls.get_score(detail['rating']),
			'time': str(detail['release_time']),
			# 'category': []
			'online': False
		}
		return res
	
	@classmethod
	def query(cls, args) -> dict:
		
		if 'page' not in args.keys() or args['page'] is None or not isinstance(args['page'], int) \
				or args['page'] <= 0:
			args['page'] = 1
		if 'size' not in args.keys() or args['size'] is None or not isinstance(args['size'], int) \
				or args['size'] <= 0:
			args['size'] = 10
		if 'type' not in args.keys() or args['type'] is None or not isinstance(args['type'], int) \
				or args['type'] <= 0:
			args['type'] = 1
		if 'sort' not in args.keys() or args['sort'] is None or not isinstance(args['sort'], int) \
				or args['sort'] <= 0:
			args['sort'] = 1
		
		if 'k' not in args.keys():
			args['k'] = None
		elif not args['k'] is None:
			args['k'] = args['k'].strip()
		
		args['order'] = cls.get_order_field(args['sort'])
		
		ds, count = ProductInfoDal.query(args)
		res = []
		for t in ds:
			d = cls.get(t)
			if d is not None:
				res.append(d)
		
		return result.of(dict({"list": res, "count": count}, **args))
	
	@classmethod
	def hot(cls):
		d = ProductInfoDal.get_hot()
		
		max_len = 15
		
		if len(d) > max_len:
			d = d[:max_len]
		
		res = []
		for t in d:
			t1 = cls.get(t)
			if t1 is not None:
				res.append(t1)
		
		return result.of({'hot': res[:6], 'list': res[6:max_len]})
	
	@classmethod
	def get_score(cls, s: str) -> int:
		if s is None or len(s) == 0:
			return 0
		d = json.loads(s)
		
		if isinstance(d, float):
			return d
		if isinstance(d, int):
			return d
		if isinstance(d, str):
			return float(d)
		if isinstance(d, dict):
			if 'average' in d.keys():
				return d['average']
		return 0
	
	@classmethod
	def get_main_image(cls, ll: list):
		l = filter(lambda x: x['type'] == 1, ll)
		l = list(l)
		if len(l) > 0:
			return l[0]['url']
		return ''
	
	@classmethod
	def get_order_field(cls, order=1):
		
		if order is None:
			order = 'id'
		if order == 1:
			return 'id'
		elif order == 2:
			return "score"
		elif order == 3:
			return "rating_sum"
		elif order == 4:
			return "release_time"
		return None
	
	@classmethod
	def process_about(cls, about):
		if about is None or len(about) == 0:
			return {}
		
		try:
			ab = json.loads(about)
			
			if isinstance(ab, str):
				# 处理处理。。。
				return {}
			elif isinstance(ab, dict):
				return ab
			else:
				return {}
		except Exception as e:
			print(e)
			return {}
