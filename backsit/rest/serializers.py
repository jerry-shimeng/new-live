from rest_framework import serializers

from movie.models import PublicDownloadAddress, ProductCommentInfo


class DownloadSerializer(serializers.Serializer):
	class Meta:
		model = PublicDownloadAddress
		fields = ('download_url')
	
	download_url = serializers.CharField()

class ProductCommentSerializer(serializers.Serializer):
	class Meta:
		model = ProductCommentInfo
		fields = ('content','user_name','comment_time')
		
	content = serializers.CharField()
	user_name = serializers.CharField()
	comment_time = serializers.DateField()



 