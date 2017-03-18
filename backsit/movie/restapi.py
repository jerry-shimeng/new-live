from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie.models import *
from rest_framework import serializers, viewsets


class MovieDownloadUrlSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MovieDownloadUrl
		fields = ('download_url', 'movie_id')


# @api_view(['GET'])
class DownloadApiView(viewsets.ModelViewSet):

	queryset = MovieDownloadUrl.objects.all()
	serializer_class = MovieDownloadUrlSerializer
	
	
	
	@api_view(['GET'])
	def get_downlad_url(self, request):
		id = request.GET.get("id")
		downloads = MovieDownloadUrl.objects.filter(movie=id)
		serializer = MovieDownloadUrlSerializer(downloads, many=True)
		return Response(serializer.data)
	