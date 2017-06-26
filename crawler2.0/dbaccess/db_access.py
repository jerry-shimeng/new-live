import datetime

from playhouse.shortcuts import model_to_dict

import logger_proxy
from commons.enums import PublicSourceEnums, PublicTypesEnums
from dbaccess.db_models import *
from logger_proxy import logger

logger = logger_proxy.get_logger()


class DatabaseAccess:
	@classmethod
	def exist_name(cls, name):
		try:
			m = cls.get_product_by_name(name)
			return not m is None
		except:
			return False
	
	@classmethod
	def get_product_by_name(cls, name):
		try:
			return ProductMovieDetail.get(ProductMovieDetail.product_name == name)
		except:
			return None
	
	@classmethod
	def get_product_detail(cls, detail_id, product_type):
		if product_type == PublicTypesEnums.MOVIE.value:
			return ProductMovieDetail.get(ProductMovieDetail.id == detail_id)
		else:
			return None
	
	@classmethod
	def save_as_lbl(cls, data_map):
		
		product = ProductInfo()
		product_movie = ProductMovieDetail()
		
		# 产品
		product.product_name = data_map["name"]
		product.product_type = PublicTypesEnums.MOVIE.value
		product.source = PublicSourceEnums.LBL_SOURCE.value
		product.status = 0
		product.order_index = cls.get_last_order_index() + 1
		# 电影详情
		product_movie.about = ""
		product_movie.area = ""
		product_movie.product_name = data_map["name"]
		product_movie.product_alias = data_map["name"]
		product_movie.release_time = datetime.datetime.strptime(data_map["time"].strip(), "%Y年%m月%d日").date()
		product_movie.rating = 0
		product_movie.rating_sum = 0
		product_movie.status = 1
		product_movie.content = " "
		product_movie.source_url = data_map['source']
		
		product_movie.save()
		
		# 设置id
		product.detail = product_movie.get_id()
		
		product.save()
		
		# 保存下载地址
		d_links = data_map["down_links"]
		if not d_links is None:
			for link in d_links:
				d = PublicDownloadAddress()
				d.download_url = link
				d.status = 1
				d.download_type = 1
				d.save()
				detail = ProductDownloadDetail()
				detail.address = d.get_id()
				detail.product = product.get_id()
				detail.save()
	
	@classmethod
	def get_last_order_index(cls):
		try:
			return ProductInfo.select(ProductInfo.order_index).order_by(ProductInfo.order_index.desc())[0].order_index
		except:
			return 0
	
	@classmethod
	def get_product_by_source(cls, source: PublicSourceEnums, size: int = 10) -> []:
		
		list = ProductInfo.filter(ProductInfo.source != source.value, ProductInfo.status == 0).order_by(
			ProductInfo.order_index.desc())[0:size]
		return list
	
	# 保存豆瓣数据
	@classmethod
	def save_as_douban(cls, product, result, source):
		detail = cls.get_product_detail(product.detail, product.product_type)
		detail.product_alias = result["sub_name"]
		detail.about = result["about"]
		detail.area = result["area"]
		detail.content = result["content"]
		detail.rating = result["rating"]
		detail.rating_sum = result["rating_sum"]
		detail.score = result["score"]
		detail.status = 1
		detail.douban_id = result["id"]
		
		if detail.content is None or len(detail.content) == 0:
			detail.content = "  "
		
		detail.save()
		
		img = PublicImages()
		img.image = result["image_url"]
		img.img_type = 1
		img.status = 1
		img.save()
		
		# 关系
		pro_img = ProductImagesDetail()
		pro_img.image = img.get_id()
		pro_img.product = product.id
		pro_img.save()
		
		product.source = source.value
		product.status = 1
		product.save()
		
		cls.save_comment_info(product.id, result["comments"])
		
		logger.info(product.product_name + " form source " + str(source))
	
	# comments 评论信息保存
	# result["comments"]
	@classmethod
	def save_comment_info(cls, product_id, comments):
		
		if comments is None or len(comments) == 0:
			return
		
		for comment in comments:
			product_comment = ProductCommentInfo()
			product_comment.content = comment["content"]
			product_comment.user_name = comment["user_name"]
			product_comment.comment_time = datetime.datetime.strptime(comment["comment_time"].strip(),
			                                                          "%Y-%m-%d %H:%M:%S").date()
			
			if product_comment.content is None:
				product_comment.content = " "
			
			product_comment.save()
			
			product_comment_detail = ProductCommentDetail()
			product_comment_detail.product = product_id
			product_comment_detail.comment_info = product_comment.get_id()
			product_comment_detail.save()
	
	@classmethod
	def update_fail(cls, id):
		try:
			pro = ProductInfo.get(ProductInfo.id == id)
			pro.status = 3
			pro.save()
		except Exception as e:
			logger.error("update status for %d error" % id, e)


class PublicDataAccess:
	@classmethod
	def get_categorys_by_name(cls, name, parent=1):
		try:
			ll = ProductType.get(ProductType.key == name, ProductType.parent == parent)
			return model_to_dict(ll)
		except Exception as e:
			# logger.error('get_categorys_by_name', e)
			return None
	
	@classmethod
	def save_product_type_detail(cls, pid, cid):
		detail = ProductSubTypeDetail()
		detail.product = pid
		detail.sub_type = cid
		
		detail.save()
	
	@classmethod
	def save_categorys(cls, key, pid):
		ptype = ProductType()
		ptype.parent = pid
		ptype.key = key
		ptype.name = key
		ptype.describe = key
		ptype.status = 1
		
		ptype.save()
		return model_to_dict(ptype)
