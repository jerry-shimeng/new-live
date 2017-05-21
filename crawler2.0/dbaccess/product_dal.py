from dbaccess.db_models import *


class ProductDAL:
	@classmethod
	def get_product_by_name(cls, name):
		try:
			return ProductInfo.get(ProductInfo.product_name == name)
		except:
			return None
	
	@classmethod
	def get_product_like_name(cls, name):
		try:
			return ProductInfo.get(ProductInfo.product_name.contains(name))
		except:
			return None
