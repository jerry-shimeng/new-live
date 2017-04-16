import logging

from django.forms import model_to_dict

from movie.models import *

page_size = 9
movie_key = "movie"

logger = logging.getLogger("django")


class DataBaseAccess:
	@classmethod
	def get_product_list(cls, page=1, size=page_size, order=None):
		
		product_type_id = cls.get_movie_product_type().id
		
		if order is None:
			order = "-order_index"
		
		products = ProductInfo.objects.filter(product_type=product_type_id, status=1).order_by(order)
		
		count = products.count()
		products = products[(page - 1) * size:size * page]
		
		return cls.get_movie_list(products), count
	
	@classmethod
	def get_product_list_by_search(cls, key, page=1, size=page_size, order=None):
		product_type_id = cls.get_movie_product_type().id
		
		if not order is None:
			return cls.search_product(key, page, size, order, product_type_id)
		
		order = "-order_index"
		products = ProductInfo.objects.filter(product_type=product_type_id, status=1,
		                                      product_name__contains=key).order_by(order)
		
		count = products.count()
		products = products[(page - 1) * size:size * page]
		
		return cls.get_movie_list(products), count
	
	@classmethod
	def search_product(cls, key, page, size, order, product_type_id):
		
		sql = '''FROM product_info  AS  a
					LEFT JOIN product_movie_detail AS b
					  ON a.detail = b.id
					WHERE a.status =1 AND a.product_type_id = %s	''' % product_type_id
		
		if not key is None and len(key) > 0:
			sql = sql + "AND a.product_name LIKE '%%s%' " % key
		sql = sql + "ORDER BY b.%s DESC" % order
		
		s1 = "SELECT  a.* " + sql
		
		products = ProductInfo.objects.raw(s1)
		
		from django.db import connection
		cursor = connection.cursor()
		s2 = "SELECT count(a.id) " + sql
		cursor.execute(s2)
		count = cursor.fetchone()[0]
		products = products[(page - 1) * size:size * page]
		
		return cls.get_movie_list(products), count
	
	@classmethod
	def get_movie_list(cls, products):
		list = []
		for product in products:
			# 获取详情
			if product.detail == 0:
				continue
			model = cls.get_product_detail(product.id)
			list.append(model)
		return list
	
	@classmethod
	def get_product_images(cls, id):
		try:
			list = []
			imgs = ProductImagesDetail.objects.filter(product=id)
			# print(imgs)
			for img in imgs:
				img.image.image = img.image.image.replace(".webp", ".jpg")
				list.append(model_to_dict(img.image))
			return list
		except Exception as e:
			logger.error("get_product_images id={}", id, e)
			return []
	
	@classmethod
	def get_product_detail(cls, id):
		try:
			product = ProductInfo.objects.get(id=id)
			query = ProductMovieDetail.objects.get(id=product.detail)
			query = model_to_dict(query)
			product = model_to_dict(product)
			model = dict(query, **product)
			if not model["release_time"] is None:
				model["release_time"] = model["release_time"].strftime("%Y-%m-%d")
			model["images"] = cls.get_product_images(model["id"])[0]
			return model
		except Exception as e:
			logger.error("get_product_detail id = {}", id, e)
			return None
	
	@classmethod
	def get_product_count(cls):
		try:
			product_type_id = cls.get_movie_product_type().id
			return ProductInfo.objects.filter(product_type=product_type_id, status=1).count()
		except Exception as e:
			logger.error("get_product_count", e)
			return None
	
	@classmethod
	def get_movie_product_type(cls):
		try:
			return ProductType.objects.get(key=movie_key, status=1)
		except Exception as e:
			logger.error("get_movie_product_type", e)
			return None
