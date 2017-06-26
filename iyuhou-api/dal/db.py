from playhouse.shortcuts import model_to_dict

from dal import models
from dal.models import ProductInfo, ProductMovieDetail, ProductImagesDetail, PublicImages, ProductDownloadDetail, \
	PublicDownloadAddress, ProductCommentDetail, ProductCommentInfo


class ProductInfoDal:
	@classmethod
	def get(cls, pid):
		"""
		获取product信息
		:param pid:
		:return:
		"""
		try:
			d = ProductInfo.get(ProductInfo.id == pid, ProductInfo.status == 1)
		except Exception as e:
			print(e)
			return None
		
		if d is None:
			return None
		else:
			return model_to_dict(d)
	
	@classmethod
	def get_img(cls, pid):
		d = []
		imgs = ProductImagesDetail.filter(ProductImagesDetail.product == pid)
		for img in imgs:
			temp = PublicImages.get(PublicImages.id == img.image)
			
			img_url = temp.image.replace(".webp", ".jpg")
			d.append({"url": img_url, "type": temp.img_type})
		return d
	
	@classmethod
	def query(cls, args):
		sql = '''FROM product_info  AS  a
							LEFT JOIN product_movie_detail AS b
							ON a.detail = b.id
							WHERE a.status =1 AND a.product_type_id = %s	''' % args['type']
		
		if not args['k'] is None and len(args['k']) > 0:
			sql = sql + 'AND a.product_name LIKE "%%%s%%" ' % args['k']
		
		# 总量
		count = "SELECT  count(a.id) as count " + sql
		count = models.database.execute_sql(count)
		
		total = count._result.rows[0][0]
		count.close()
		
		sql = sql + "ORDER BY b.%s DESC" % args['order']
		
		# 分页
		index, size = args['page'], args['size']
		
		sql += " LIMIT %s, %s;" % ((index - 1) * size, size)
		
		sql = "SELECT  a.* " + sql
		ll = ProductInfo.raw(sql)
		ll = map(lambda x: x.id, ll)
		return list(ll), total
	
	@classmethod
	def get_hot(cls):
		try:
			ll = ProductInfo.filter(ProductInfo.hot == 1).order_by(ProductInfo.order_index.desc())
			return list(map(lambda x: x.id, ll))
		except:
			return []


class ProductMovieDAL:
	@classmethod
	def get(cls, id):
		try:
			d = ProductMovieDetail.get(ProductMovieDetail.id == id, ProductMovieDetail.status == 1)
		
		except Exception as e:
			print(e)
			return None
		
		if d is None:
			return None
		else:
			return model_to_dict(d)


class PublicDownloadDAL:
	@classmethod
	def get_address(cls, id):
		l = ProductDownloadDetail.get(ProductDownloadDetail.product == id)
		
		x = PublicDownloadAddress.get(PublicDownloadAddress.id == l.address)
		
		return model_to_dict(x)


class ProductCommentDAL:
	@classmethod
	def get(cls, id):
		ls = ProductCommentDetail.filter(ProductCommentDetail.product == id)
		
		res = []
		
		for l in ls:
			d = ProductCommentInfo.get(ProductCommentInfo.id == l.comment_info)
			res.append(d)
		return list(map(lambda x: model_to_dict(x), res))
