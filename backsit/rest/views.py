import logging
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from movie.config import AppConfig
from movie.dal import DataBaseAccess
from movie.models import PublicDownloadAddress, ProductDownloadDetail, ProductCommentDetail, ProductInfo
from rest.serializers import DownloadSerializer, ProductCommentSerializer

logger = logging.getLogger()


class DownloadUrlList(ModelViewSet):
	'''
		下载地址
	'''
	queryset = PublicDownloadAddress.objects.all()
	
	def get(self, request, id, format=None):
		details = ProductDownloadDetail.objects.filter(product=id).all()
		
		result = list(map(lambda x: x.address, details))
		
		ser = DownloadSerializer(result, many=True)
		return Response(ser.data)


class ProductCommentList(ModelViewSet):
	'''
		热评信息
	'''
	queryset = ProductCommentDetail.objects.all()
	
	def get(self, request, id):
		details = ProductCommentDetail.objects.filter(product=id)
		
		result = list(map(lambda x: x.comment_info, details))
		
		ser = ProductCommentSerializer(result, many=True)
		return Response(ser.data)


class ProductMovieList(ModelViewSet):
	queryset = ProductInfo.objects.all()
	
	def query(self, key=None, page=1, size=10, order=1):
		# r = None
		# count = 0
		order_field = self.get_order_field(order)
		try:
			if key is None:
				r, count = DataBaseAccess.get_product_list(page, size)
			else:
				r, count = DataBaseAccess.get_product_list_by_search(key, page, size=size, order=order_field)
				
			res = []
			for v in r:
				res.append(v)
			
			return res, count
		except Exception as e:
			logger.error("queryset ", e)
			return None, 0
	
	def get_order_field(self, order=1):
		if order == 1:
			return None
		elif order == 2:
			return "rating"
		elif order == 3:
			return "rating_sum"
		elif order == 4:
			return "release_time"
		return None
	
	def desc(self):
		return Response(AppConfig)
	
	def page(self, request, page=1):
		
		if page is None:
			page = 1
		page = int(page)
		if page <= 0:
			page = 1
		
		r, count = self.query(page=page)
		temp = {'data': r, 'count': count}
	 
		return Response(temp)
