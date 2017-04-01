import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader, RequestContext
from django.views import generic

from movie.dal import DataBaseAccess
from movie.models import *

# def index(request):
#     movie_list = MovieDetail.objects.order_by("id")[:10]
#     # output = ",".join([p.name for p in movie_list])
#     # template = loader.get_template("./index.html")
#     # context = RequestContext(request, {
#     #     "movie_list": movie_list,
#     # })
#     # return HttpResponse(template.render(context))
#     context = {"movie_list": movie_list}
#     return render(request, "index.html", context)
#
#
# def detail(request, id):
#     # model = MovieDetail.objects.get(pk=id)
#     # print(model)
#     # return HttpResponse(model)
#     model = get_object_or_404(MovieDetail, pk=id)
#     return render(request, "detail.html", {"model": model})


page_size = 9


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "movie_list"

    def queryset(self, key=None, page=1):
        r = None
        try:
            if key is None:
                r = DataBaseAccess.get_product_list(page)
            else:
                r = DataBaseAccess.get_product_list_by_search(key, page, size=20)
            return r
        except:
            return None

    def index(self, request):
        list = self.queryset()
        return render(request, self.template_name,
                      {"movie_list": list, "total_count": self.get_page_count(), "pager": 1})

    def help(self, request):
        return render(request, "help.html", {})

    def contact(self, request):
        return render(request, "contact.html", {})

    def page(self, request, page):

        if page is None:
            page = 1
        page = int(page)
        r = self.queryset(page=page)
        return render(request, self.template_name,
                      {"movie_list": r, "total_count": self.get_page_count(), "pager": page})

    # 查询结果
    def search(self, request):
        key = request.GET.get("key")
        page = request.GET.get("page")
        if key is None:
            key = ""
        else:
            key = key.strip()

        if page is None:
            page = 1
        page = int(page)
        r = self.queryset(key=key, page=page)
        return render(request, "list.html", {"movie_list": r, "key": key})

    def get_page_count(self):
        count = DataBaseAccess.get_product_count()
        a = 1
        if count % page_size == 0:
            a = count / page_size
        else:
            a = count / page_size + 1
        return int(a)


class DetailView(generic.DetailView):
    model = ProductMovieDetail
    template_name = "detail.html"
    context_object_name = "model"

    def get_detail(self, request, pk):
        m = DataBaseAccess.get_product_detail(pk)
        return render(request, self.template_name, {"model": m})
