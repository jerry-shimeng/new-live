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


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "movie_list"

    def get_queryset(self):
        list = MovieDetail.objects.order_by("-release_time")[:9]
        r = []
        for l in list:
            m = model_to_dict(l)
            m["about"] = m["about"][0:20] + "..."
            # 获取图片
            img = MovieImages.objects.get(movie=l.id)
            m["images"] = model_to_dict(img)
            r.append(m)
        # print(r)
        return r


class DetailView(generic.DetailView):
    model = MovieDetail
    template_name = "detail.html"
    context_object_name = "model"
