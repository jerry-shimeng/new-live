import json

from django.forms import model_to_dict

from movie.models import *

page_size = 9
movie_key = "movie"


class DataBaseAccess:
	@classmethod
	def get_product_list(cls, page=1):
		
		product_type_id = cls.get_movie_product_type().id
		print(product_type_id)
		products = ProductInfo.objects.filter(product_type=product_type_id, status=1).order_by("-order_index")[
		           (page - 1) * page_size:page_size * page]
		# print(products)
		return cls.get_movie_list(products)
	
	@classmethod
	def get_product_list_by_search(cls, key, page=1, size=page_size):
		product_type_id = cls.get_movie_product_type().id
		
		products = ProductInfo.objects.filter(product_type=product_type_id, status=1,
		                                      product_name__contains=key).order_by("-update_time")[
		           (page - 1) * size:size * page]
		
		return cls.get_movie_list(products)
	
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
		list = []
		imgs = ProductImagesDetail.objects.filter(product=id)
		# print(imgs)
		for img in imgs:
			img.image.image = img.image.image.replace(".webp", ".jpg")
			list.append(model_to_dict(img.image))
		return list
	
	@classmethod
	def get_product_detail(cls, id):
		
		product = ProductInfo.objects.get(id=id)
		query = ProductMovieDetail.objects.get(id=product.detail)
		query = model_to_dict(query)
		product = model_to_dict(product)
		model = dict(query, **product)
		if not model["release_time"] is None:
			model["release_time"] = model["release_time"].strftime("%Y-%m-%d")
		
		imgs = cls.get_product_images(model["id"])
		if imgs is None or len(imgs) == 0:
			return model
		
		model["images"] = cls.get_product_images(model["id"])[0]
		return model
	
	@classmethod
	def get_product_count(cls):
		product_type_id = cls.get_movie_product_type().id
		return ProductInfo.objects.filter(product_type=product_type_id, status=1).count()
	
	@classmethod
	def get_movie_product_type(cls):
		return ProductType.objects.get(key=movie_key, status=1)
	
	@classmethod
	def save_product(cls, model):
		
		secret = model["secret"]
		
		if secret != cls.get_public_dict("secret"):
			print("secret is error", secret)
			return
		
		product = model["product"]
		if not cls.exist_name(product["product_name"]):
			print("save error ,has ", product["product_name"])
			return
		
		product_detail = model["product_detail"]
		images = model["images"]
		downloads = model["downloads"]
		
		# 先保存detail信息
		product_detail = cls.save_product_detail_by_dict(product_detail)
		# 保存product
		product["detail"] = product_detail.id
		product = cls.save_product_info_by_dict(product)
		# 图片
		cls.save_product_images_by_dict(images, product.id)
		
		# 下载地址
		cls.save_product_download_by_dict(downloads, product.id)
	
	@classmethod
	def save_product_info_by_dict(cls, m):
		pro = ProductInfo()
		pro.order_index = m["order_index"]
		pro.product_name = m["product_name"]
		pro.product_type_id = m["product_type"]
		pro.source_id = m["source"]
		pro.detail = m["detail"]
		pro.status = m["status"]
		pro.save()
		return pro
	
	@classmethod
	def save_product_detail_by_dict(cls, m):
		
		pro = ProductMovieDetail()
		pro.product_name = m["product_name"]
		pro.product_alias = m["product_alias"]
		pro.rating = m["rating"]
		pro.rating_sum = m["rating_sum"]
		pro.release_time = m["release_time"]
		pro.about = m["about"]
		pro.content = m["content"]
		pro.area = m["area"]
		pro.status = m["status"]
		pro.save()
		return pro
	
	@classmethod
	def save_product_images_by_dict(cls, m, product_id):
		for img in m:
			image = PublicImages()
			image.image = img["image"]
			image.img_type = img["img_type"]
			image.status = 1
			image.save()
			pid = ProductImagesDetail()
			pid.product_id = product_id
			pid.image_id = image.id
			pid.save()
			print("%")
	
	@classmethod
	def save_product_download_by_dict(cls, m, product_id):
		for dl in m:
			pdl = PublicDownloadAddress()
			pdl.download_url = dl["download_url"]
			pdl.download_type = dl["download_type"]
			pdl.status = 1
			pdl.save()
			pdd = ProductDownloadDetail()
			pdd.product_id = product_id
			pdd.address_id = pdl.id
			pdd.save()
			print("*")
	
	@classmethod
	def exist_name(cls, name):
		try:
			m = ProductInfo.objects.get(product_name=name)
			return m is None
		except:
			return True
	
	@classmethod
	def get_public_dict(cls, key):
		return PublicDictionary.objects.get(key=key).value
