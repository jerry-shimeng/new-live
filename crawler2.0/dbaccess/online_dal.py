import json

import datetime
import traceback

from commons.enums import PublicTypesEnums, PublicSourceEnums
from dbaccess.db_access import DatabaseAccess
from dbaccess.db_models import ProductInfo, ProductMovieDetail, PublicDownloadAddress, PublicImages
from dbaccess.product_dal import ProductDAL


class OnlineDAL:
	@classmethod
	def save(cls, d, t):
		# 判断是否已经存在
		product = ProductDAL.get_product_by_name(d['name'])
		
		if product is None:
			product = ProductInfo()
			product.status = 1
			product.order_index = DatabaseAccess.get_last_order_index() + 1
			product.product_name = d['name']
			product.product_type = PublicTypesEnums.MOVIE.value
			product.source = t.value
		
		detail = cls.get_save_detail(product, d)
		
		product.detail = detail.id
		product.save()
		
		cls.save_address(product.id, d['online_url'], t)

		cls.save_imgs(product.id,d)

		return product, detail
	
	# 保存地址
	
	
	@classmethod
	def get_save_detail(cls, product, d, type=PublicTypesEnums.MOVIE):
		
		detail = DatabaseAccess.get_product_detail(product.detail, type)
		
		if detail is None or product.source == PublicSourceEnums.LBL.value:
			detail = DatabaseAccess.get_product_detail_by_name(product.product_name, type)
			
			if detail is None:
				detail = ProductMovieDetail()
			
			detail.product_name = d['name']
			detail.product_alias = d['sub_name']
			detail.rating = d['rating']
			detail.score = d['score']
			detail.rating_sum = d['rating_sum']
			if len(d['about']['time'].strip()) > 0:
				try:
					detail.release_time = datetime.datetime.strptime(d['about']['time'].strip(), "%Y-%m-%d").date()
				except:
					pass
			detail.about = json.dumps(d['about'])
			detail.content = d['content']
			detail.area = d['area']
			detail.status = 1
			detail.source_url = d['online_url']
			detail.save()
		
		return detail
	
	@classmethod
	def save_address(cls, pid, address, t):
		
		# 保存地址信息
		# 获取地址信息
		try:
			dt = PublicDownloadAddress.get(PublicDownloadAddress.product == pid,
			                               PublicDownloadAddress.download_type == 2)
		except:
			dt = None
		
		if dt is None:
			dt = PublicDownloadAddress()
			dt.download_url = json.dumps({t.name: address})
			dt.download_type = 2
			dt.product = pid
			dt.status = 1
			dt.save()
		else:
			try:
				du = json.loads(dt.download_url)
				du[t.name] = address
				dt.download_url = json.dumps(du)
				
				dt.save()
			except:
				traceback.print_exc()
				print(address)
				print(dt.download_url)

	@classmethod
	def save_imgs(cls,pid,d):
		img = PublicImages()
		img.image = d["image_url"]
		img.img_type = 1
		img.status = 1
		img.product = pid
		img.save()
