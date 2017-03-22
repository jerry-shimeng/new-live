from django.conf.urls import url, include

from movie.restapi import MovieDownloadUrlApi
from . import views

# router = routers.DefaultRouter()
# # router.register(r"download", DownloadApiView)
#
# router.register(r"movies", MovieDetailView.as_view())

urlpatterns = [
    # url(r"^$", views.index, name="index"),
    # url(r"^detail/(?P<id>[0-9]+)/", views.detail, name="detail"),
    url(r"^$", views.IndexView().index, name="index"),
    url(r"^page/(?P<page>[0-9]+)$", views.IndexView().page, name="page"),
    url(r"^detail/(?P<pk>[0-9]+)$", views.DetailView().get_detail, name="detail"),
    url(r"^search", views.IndexView().search, name="search"),

    url(r'^api/down/(?P<movie>[0-9]+)$', MovieDownloadUrlApi().get, name="down_url"),
    # url(r'^down/', MovieDownloadUrlView.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
