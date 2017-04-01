from django.contrib import admin

# Register your models here.
from movie.models import *

admin.site.register(SensitiveWords)


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_type", "source", "order_index")
    list_per_page = 20
    list_filter = ["source", "product_type"]
    search_fields = ["product_name"]
    ordering = ["-order_index"]


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "describe", "status")


class PublicDataSourceAdmin(admin.ModelAdmin):
    list_display = ("source_name", "key", "source_type", "status")


class ProductDownloadDetailAdmin(admin.ModelAdmin):
    list_display = ("product", "address")
    search_fields = ["product"]


admin.site.register(ProductInfo, ProductInfoAdmin)
#admin.site.register(ProductImagesDetail, ProductImagesAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(PublicDataSource, PublicDataSourceAdmin)
#admin.site.register(ProductDownloadDetail, ProductDownloadDetailAdmin)
# class MovieImagesInline(admin.TabularInline):
#     model = PublicImages
#     extra = 1
#
#
# class MovieDownloadUrlInline(admin.TabularInline):
#     model = PublicDownloadAddress
#     extra = 1
#
#
# class MovieDetailAdmin(admin.ModelAdmin):
#     list_per_page = 20
#     inlines = [MovieImagesInline, MovieDownloadUrlInline]
#     # 列表显示的字段
#     # list_display = ("name", "tag", "sub_name", "area", "datetime_format")
#     # 侧边栏过滤内容
#     # list_filter = ["tag"]
#     # 允许搜索的内容
#     # search_fields = ["name"]
#     # ordering = ["-release_time"]
#
#     pass
#
#
# class MovieTypeAdmin(admin.ModelAdmin):
#     list_per_page = 20
#     # list_display = ("id", "name")
#
#
# admin.site.register(ProductMovieDetail, MovieDetailAdmin)
# admin.site.register(ProductType, MovieTypeAdmin)
