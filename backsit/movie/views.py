from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader, RequestContext
from django.views import generic
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

    def queryset(self, page=1):
        list = MovieDetail.objects.order_by("-release_time")[(page - 1) * page_size:page_size * page]
        r = self.convert_query_set(list)
        return r

    def index(self, request):
        return render(request, self.template_name,
                      {"movie_list": self.queryset(), "total_count": self.get_page_count(), "pager": 1})

    def page(self, request, page):

        if page is None:
            page = 1
        page = int(page)
        r = self.queryset(page)
        return render(request, self.template_name,
                      {"movie_list": r, "total_count": self.get_page_count(), "pager": page})

    # 查询结果
    def search(self, request):
        key = request.GET.get("key")
        list = MovieDetail.objects.filter(name__contains=key).order_by("-release_time")[:9]

        r = self.convert_query_set(list)
        return render(request, "list.html", {"movie_list": r})

    def get_page_count(self):
        count = MovieDetail.objects.count()
        a = 1
        if count % page_size == 0:
            a = count / page_size
        else:
            a = count / page_size + 1
        return int(a)

    # 模型转换
    def convert_query_set(self, set):
        r = []
        for l in set:
            m = model_to_dict(l)
            m["about"] = m["content"][0:50] + "..."
            # 获取图片
            img = MovieImages.objects.get(movie=l.id)
            m["images"] = model_to_dict(img)
            m["release_time"] = m["release_time"].strftime("%Y-%m-%d")
            r.append(m)
        return r


class DetailView(generic.DetailView):
    model = MovieDetail
    template_name = "detail.html"
    context_object_name = "model"

    def get_detail(self, request, pk):
        model = MovieDetail.objects.get(pk=pk)
        m = model_to_dict(model)
        # 获取图片
        img = MovieImages.objects.get(movie=model.id)
        m["images"] = model_to_dict(img)
        m["release_time"] = m["release_time"].strftime("%Y-%m-%d")

        durls = MovieDownloadUrl.objects.filter(movie=model.id)
        durl = []
        for d in durls:
            durl.append(model_to_dict(d))

        m["download"] = durl
        print(m)
        return render(request, self.template_name, {"model": m})
