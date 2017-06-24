from flask import json

import logger_proxy
from commons.enums import PublicSourceEnums
from dbaccess.db_access import DatabaseAccess, ProductInfo, PublicDataAccess
from douban.douban_api import DoubanApi
import traceback

from localcache import categotys_cache
logger = logger_proxy.get_logger()


class DoubanContentParser:
	@classmethod
	def parse(cls, name: str):
		exist = DatabaseAccess.exist_name(name)
		logger.info(exist)
	
	@classmethod
	def run(cls, size: int = 10):
		list = DatabaseAccess.get_product_by_source(PublicSourceEnums.DOUBAN_SOURCE, size)
		for l in list:
			logger.info(l.product_name)
			try:
				detail = DoubanApi.get_movie(l)
				if detail is not None:
					cls.save(l, detail)
			except Exception as e:
				traceback.print_exc()
				logger.error('douban',e)
				DatabaseAccess.update_fail(l.id)
	
	@classmethod
	def save(cls, product: ProductInfo, model: object):
		try:
			DatabaseAccess.save_as_douban(product, model, PublicSourceEnums.DOUBAN_SOURCE)
			
			# 保存分类信息
			cls.save_categorys(product.id, model["about"])
		
		except Exception as e:
			logger.error('douban save',e)
			DatabaseAccess.update_fail(product.id)
	
	@classmethod
	def save_categorys(cls, id, cates):
		if isinstance(cates, str):
			cates = json.loads(cates)
		
		cates = cates['categorys']
		
		for c in cates:
			# 电影是一级分类
			cid = categotys_cache.get_cate_id(c.strip(), 1)
			if cid >0:
				# 保存电影分类信息
				PublicDataAccess.save_product_type_detail(id,cid)
