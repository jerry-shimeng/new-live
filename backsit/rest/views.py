from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from movie.models import PublicDownloadAddress, ProductDownloadDetail, ProductCommentDetail
from rest.serializers import DownloadSerializer, ProductCommentSerializer


class DownloadUrlList(ModelViewSet):
	queryset = PublicDownloadAddress.objects.all()
	
	def get(self, request, id, format=None):
		details = ProductDownloadDetail.objects.filter(product=id).all()
		
		result = list(map(lambda x: x.address, details))
		
		ser = DownloadSerializer(result, many=True)
		return Response(ser.data)


class ProductCommentList(ModelViewSet):
	queryset = ProductCommentDetail.objects.all()
	
	def get(self, request, id):
		
		details = ProductCommentDetail.objects.filter(product=id)
		
		result = list(map(lambda x: x.comment_info, details))
		
		ser = ProductCommentSerializer(result, many=True)
		return Response(ser.data)