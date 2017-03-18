from django.contrib import admin

# Register your models here.
from movie.models import *

admin.site.register(SensitiveWords)


class MovieImagesInline(admin.TabularInline):
	model = MovieImages
	extra = 1


class MovieDownloadUrlInline(admin.TabularInline):
	model = MovieDownloadUrl
	extra = 1


class MovieDetailAdmin(admin.ModelAdmin):
	list_per_page = 20
	inlines = [MovieImagesInline, MovieDownloadUrlInline]
	# 列表显示的字段
	list_display = ("name", "tag", "get_desc", "datetime_format")
	# 侧边栏过滤内容
	list_filter = ["tag"]
	# 允许搜索的内容
	search_fields = ["name"]
	ordering = ["-release_time"]
	
	pass


class MovieTypeAdmin(admin.ModelAdmin):
	list_per_page = 20
	list_display = ("id", "name")


admin.site.register(MovieDetail, MovieDetailAdmin)
admin.site.register(MovieType, MovieTypeAdmin)
