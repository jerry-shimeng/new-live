from django.conf.urls import url, include

from rest import views

urlpatterns = [
	url(r'^down/(?P<id>[0-9]+)$', views.DownloadUrlList.as_view({'get': 'get'})),
	url(r'^comment/(?P<id>[0-9]+)$', views.ProductCommentList.as_view({'get': 'get'})),
	url(r'^movie/$', views.ProductMovieList.as_view({'conf': 'desc', 'get': 'page'})),
]
