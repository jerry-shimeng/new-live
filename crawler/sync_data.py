from playhouse.shortcuts import model_to_dict

from config import async_url
from db_access import DatabaseAccess
from http_utility import HttpUtility
from logger_proxy import logger


class AsyncData:
	@classmethod
	def start(cls):
		r = DatabaseAccess.get_the_new_data()
		
		if r is None:
			return
		
		# 获取详情
		for data in r:
			detail = cls.get_detail(data)
			if detail is None:
				continue
			
			cls.async(detail)
			cls.save_history(data)
			return
	
	@classmethod
	def get_detail(cls, product):
		model = dict()
		
		# 获取detail信息
		product_detail = DatabaseAccess.get_product_detail(product["detail"], product["product_type"])
		
		if product_detail is None:
			return None
		
		product_detail = model_to_dict(product_detail)
		
		# print(product_detail)
		# 获取图片信息
		images = DatabaseAccess.get_product_images(product["id"])
		# print(images)
		# 获取下载地址信息
		downloads = DatabaseAccess.get_product_download(product["id"])
		# print(downloads)
		
		model["product"] = product
		model["product_detail"] = product_detail
		model["images"] = images
		model["downloads"] = downloads
		model["secret"] =DatabaseAccess.get_public_dict_value("secret")
		return model
	
	@classmethod
	def async(cls, data):
		#print(data)
		# async_url
		d = HttpUtility.post(async_url, data)
		logger.info(d)
		pass
	
	@classmethod
	def save_history(cls, product):
		
		DatabaseAccess.save_submit_history(product["id"])
