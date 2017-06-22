# import json
#
# from django.forms import model_to_dict
# from django.http import HttpResponse
# from django.views import generic
# from django.views.decorators.csrf import csrf_exempt
#
# from movie.dal import DataBaseAccess
# from movie.models import *
#
#
# class ProductDownloadUrlApi(generic.DetailView):
# 	def get_data(self, id):
# 		list = ProductDownloadDetail.objects.filter(product=id)
# 		r = []
# 		for l in list:
# 			t = PublicDownloadAddress.objects.values("download_url").get(id=l.address_id)
#
# 			r.append(t)
# 		return r
#
# 	def get(self, request, id):
# 		list = []
# 		try:
# 			list = self.get_data(id)
# 		except:
# 			pass
# 		return HttpResponse(json.dumps(list))
#
#
# class ProductCommentApi(generic.ListView):
# 	def query_set(self, id):
# 		details = ProductCommentDetail.objects.filter(product=id)
# 		r = []
# 		for detail in details:
# 			t = detail.comment_info
# 			if t is None:
# 				continue
# 			t = model_to_dict(t)
# 			t["comment_time"] = t["comment_time"].strftime('%Y-%m-%d')
#
# 			r.append(t)
# 		return r
#
# 	def get(self, request, id):
# 		list = []
# 		try:
# 			list = self.query_set(id)
# 		except:
# 			pass
# 		return HttpResponse(json.dumps(list, ensure_ascii=False))
#
#
# class ProductInfoApi(generic.DetailView):
# 	@csrf_exempt
# 	def submit_data(self, request):
# 		res = {"code": 1, "message": ""}
#
# 		if request.method != 'POST':
# 			return HttpResponse("yes")
# 		try:
# 			model = json.loads(request.body)
# 			DataBaseAccess.save_product(model)
# 		except Exception as e:
# 			res["code"] = -1
# 			res["message"] = e
# 			print(e)
#
# 		return HttpResponse(res["code"])
