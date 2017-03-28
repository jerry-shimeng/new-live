from django.forms import model_to_dict

from movie.models import *

page_size = 9
movie_key = "movie"


class DataBaseAccess:
    @classmethod
    def get_product_list(cls, page=1):

        product_type_id = cls.get_movie_product_type().id

        products = ProductInfo.objects.filter(product_type=product_type_id, status=1).order_by("-update_time")[
                   (page - 1) * page_size:page_size * page]

        return cls.get_movie_list(products)

    @classmethod
    def get_product_list_by_search(cls, key, page=1):
        product_type_id = cls.get_movie_product_type().id

        products = ProductInfo.objects.filter(product_type=product_type_id, status=1,
                                              product_name__contains=key).order_by("-update_time")[
                   (page - 1) * page_size:page_size * page]

        return cls.movie_list(products)

    @classmethod
    def get_movie_list(cls, products):
        list = []
        for product in products:
            # 获取详情
            if product.detail == 0:
                continue
            model = cls.get_product_detail(product.id)
            # query = ProductMovieDetail.objects.get(id=product.detail)
            # if query is None:
            #     continue
            # # 获取图片
            # query = model_to_dict(query)
            # product = model_to_dict(product)
            # model = dict(query, **product)
            # model["release_time"] = model["release_time"].strftime("%Y-%m-%d")
            # model["images"] = cls.get_product_images(model["id"])
            list.append(model)
        return list

    @classmethod
    def get_product_images(cls, id):
        list = []
        imgs = ProductImagesDetail.objects.filter(product=id)
        for img in imgs:
            img.image.image = img.image.image.replace(".webp", ".jpg")
            list.append(model_to_dict(img.image))
        return list

    @classmethod
    def get_product_detail(cls, id):
        product = ProductInfo.objects.get(id=id)
        query = ProductMovieDetail.objects.get(id=product.detail)
        query = model_to_dict(query)
        product = model_to_dict(product)
        model = dict(query, **product)
        if not model["release_time"] is None:
            model["release_time"] = model["release_time"].strftime("%Y-%m-%d")
        model["images"] = cls.get_product_images(model["id"])
        return model

    @classmethod
    def get_product_count(cls):
        product_type_id = cls.get_movie_product_type().id
        return ProductInfo.objects.filter(product_type=product_type_id, status=1).count()

    @classmethod
    def get_movie_product_type(cls):
        return ProductType.objects.get(key=movie_key, status=1)
