from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r"^$", views.index, name="index"),
    # url(r"^detail/(?P<id>[0-9]+)/", views.detail, name="detail"),
    url(r"^$", views.IndexView().index, name="index"),
    url(r"^page/(?P<page>[0-9]+)$", views.IndexView().page, name="page"),
    url(r"^detail/(?P<pk>[0-9]+)$", views.DetailView.as_view(), name="detail"),
    url(r"^search", views.IndexView().search, name="search"),
]
