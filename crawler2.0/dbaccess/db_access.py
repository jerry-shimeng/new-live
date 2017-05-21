from playhouse.shortcuts import model_to_dict

from dbaccess.db_models import *
from logger_proxy import logger


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
		if product_type == cls.get_product_type(movie_key):
			return ProductMovieDetail.get(ProductMovieDetail.id == detail_id)
		else:
			return None
	
	@classmethod
	def get_product_type(cls, key=movie_key):
		global movie_key_id
		try:
			if movie_key_id == 0:
				movie_key_id = ProductType.get(ProductType.key == key).id
			return movie_key_id
		except Exception as e:
			logger.error("not found ProductType = ", key)
			raise e
	
	@classmethod
	def get_data_source(cls, source=base_source):
		global base_source_id
		
		if base_source_id > 0:
			return base_source_id
		
		try:
			base_source_id = PublicDataSource.get(PublicDataSource.key == source).id
		except Exception as e:
			logger.error("not found PublicDataSource = ", source)
			raise e
	
	@classmethod
	def save_as_lbl(cls, data_map):
		if cls.exist_name(data_map["name"]):
			return
		product = ProductInfo()
		product_movie = ProductMovieDetail()
		
		# 产品
		product.product_name = data_map["name"]
		product.product_type = cls.get_product_type()
		product.source = cls.get_data_source()
		product.status = 0
		product.order_index = cls.get_last_order_index() + 1
		# 电影详情
		product_movie.about = data_map["about"]
		product_movie.area = ""
		product_movie.product_name = data_map["name"]
		product_movie.product_alias = data_map["name"]
		product_movie.release_time = datetime.datetime.strptime(data_map["time"].strip(), "%Y年%m月%d日").date()
		product_movie.rating = 0
		product_movie.rating_sum = 0
		product_movie.status = 1
		product_movie.content = " "
		
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
	def get_product_by_source(cls, source):
		source_id = cls.get_data_source(source)
		
		list = ProductInfo.filter(ProductInfo.source != source_id, ProductInfo.status == 0).order_by(
			ProductInfo.order_index.desc())[0:10]
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
		
		product.source = cls.get_data_source(source)
		product.status = 1
		product.save()
		
		cls.save_comment_info(product.id, result["comments"])
		
		logger.info(product.product_name, "form source", source)
	
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
	
	# 获取未更新的数据提交到生产环境
	@classmethod
	def get_the_new_data(cls, size=10):
		history = None
		try:
			history = SubmitHistory.select().order_by(SubmitHistory.submit_time.desc())[0]
		except:
			history = None
		
		query = None
		
		if history is None:
			query = ProductInfo.select().filter(ProductInfo.status == 1)
		else:
			query = ProductInfo.select().filter(ProductInfo.status == 1, ProductInfo.update_time > history.submit_time)
		
		r = query.order_by(ProductInfo.update_time)[0:size]
		
		if r is None or len(r) == 0:
			return []
		
		list = []
		
		for d in r:
			d = model_to_dict(d)
			list.append(d)
		
		return list
	
	# 获取图片信息
	@classmethod
	def get_product_images(cls, product_id):
		r = ProductImagesDetail.select().filter(ProductImagesDetail.product == product_id)
		list = []
		for d in r:
			temp = PublicImages.select(PublicImages.image, PublicImages.img_type).filter(
				PublicImages.id == d.image).first()
			list.append(model_to_dict(temp))
		return list
	
	# 获取下载地址
	@classmethod
	def get_product_download(cls, product_id):
		r = ProductDownloadDetail.select().filter(ProductDownloadDetail.product == product_id)
		
		list = []
		for d in r:
			temp = PublicDownloadAddress.select(PublicDownloadAddress.download_type,
			                                    PublicDownloadAddress.download_url).filter(
				PublicDownloadAddress.id == d.address).first()
			list.append(model_to_dict(temp))
		return list
	
	@classmethod
	def get_public_dict_value(cls, key):
		return PublicDictionary.get(PublicDictionary.key == key).value
	
	@classmethod
	def save_submit_history(cls, product_id):
		m = SubmitHistory()
		m.product = product_id
		m.save()
	
	@classmethod
	def update_fail(cls, id):
		try:
			pro = ProductInfo.get(ProductInfo.id == id)
			pro.status = 3
			pro.save()
		except Exception as e:
			logger.error("update status for %d error" % id, e)
