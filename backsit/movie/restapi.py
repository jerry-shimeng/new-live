from django.forms import model_to_dict
from django.http import HttpResponse
from django.views import generic

from movie.models import MovieDownloadUrl


class MovieDownloadUrlApi(generic.DetailView):
    def get_data(self, id):
        list = MovieDownloadUrl.objects.filter(movie=id)
        r = []
        for l in list:
            r.append(model_to_dict(l))
        return r

    def get(self, request, movie):
        list = self.get_data(movie)
        return HttpResponse(list)
