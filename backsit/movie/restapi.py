from django.forms import model_to_dict
from django.http import HttpResponse
from django.views import generic

from movie.models import *


class MovieDownloadUrlApi(generic.DetailView):
    def get_data(self, id):
        list = ProductDownloadDetail.objects.filter(product=id)
        r = []
        for l in list:
            t = PublicDownloadAddress.objects.get(id=l.address_id)
            r.append(model_to_dict(t))
        return r

    def get(self, request, movie):
        list = self.get_data(movie)
        return HttpResponse(list)
