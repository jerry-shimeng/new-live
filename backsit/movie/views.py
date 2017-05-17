import logging
from django.shortcuts import render, get_object_or_404

from django.views import generic

from movie.config import AppConfig
from movie.dal import DataBaseAccess
from movie.models import *

page_size = 9

logger = logging.getLogger()


class IndexView(generic.ListView):
	template_name = "index.html"
	context_object_name = "movie_list"
	
	def queryset(self, key=None, page=1, order=1):
		r = None
		count = 0
		order_field = self.get_order_field(order)
		try:
			if key is None:
				r, count = DataBaseAccess.get_product_list(page)
			else:
				r, count = DataBaseAccess.get_product_list_by_search(key, page, order=order_field)
			return r, count
		except Exception as e:
			logger.error("queryset ", e)
			return None, 0
	
	def index(self, request):
		list, count = self.queryset()
		return render(request, self.template_name,
		              {"movie_list": list, "config": AppConfig, "total_count": self.get_page_count(count), "pager": 1})
	
	def help(self, request):
		return render(request, "help.html", {"config": AppConfig})
	
	def contact(self, request):
		return render(request, "contact.html", {"config": AppConfig})
	
	def page(self, request, page):
		
		if page is None:
			page = 1
		page = int(page)
		if page <= 0:
			page = 1
		
		r, count = self.queryset(page=page)
		return render(request, self.template_name,
		              {"movie_list": r, "total_count": self.get_page_count(count), "pager": page,"config": AppConfig})
	
	# 查询结果
	def search(self, request):
		key = request.GET.get("key")
		page = request.GET.get("page")
		order = request.GET.get("order")
		if key is None:
			key = ""
		else:
			key = key.strip()
		
		if order is None:
			order = 1
		# 获取排序的key
		order = int(order)
		
		if page is None:
			page = 1
		page = int(page)
		r, count = self.queryset(key=key, page=page, order=order)
		
		return render(request, "list.html", {"movie_list": r, "total_count": self.get_page_count(count), "key": key,"config": AppConfig})
	
	def get_page_count(self, count):
		a = 1
		if count % page_size == 0:
			a = count / page_size
		else:
			a = count / page_size + 1
		return int(a)
	
	def get_order_field(self, order=1):
		if order == 1:
			return None
		elif order == 2:
			return "rating"
		elif order == 3:
			return "rating_sum"
		elif order == 4:
			return "release_time"
		return None


class DetailView(generic.DetailView):
	model = ProductMovieDetail
	template_name = "detail.html"
	context_object_name = "model"
	
	def get_detail(self, request, pk):
		m = DataBaseAccess.get_product_detail(pk)
		return render(request, self.template_name, {"model": m,"config": AppConfig})
