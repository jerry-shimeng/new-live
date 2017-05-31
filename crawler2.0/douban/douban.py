from dbaccess.db_access import DatabaseAccess, ProductInfo
from douban.douban_api import DoubanApi

douban_sorce = "douban"


class DoubanContentParser:
	@classmethod
	def parse(cls, name: str):
		exist = DatabaseAccess.exist_name(name)
		print(exist)
	
	@classmethod
	def run(cls, size: int = 10):
		list = DatabaseAccess.get_product_by_source(douban_sorce, size)
		for l in list:
			print('1:', l.product_name)
			detail = DoubanApi.get_movie(l)
			if detail is not None:
				cls.save(l, detail)
	
	@classmethod
	def save(cls, product: ProductInfo, model: object):
		DatabaseAccess.save_as_douban(product, model, "douban")
