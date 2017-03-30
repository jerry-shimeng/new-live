import datetime
from db_model import *

movie_key = "movie"

base_source = "lbl"


class DatabaseAccess:
    @classmethod
    def exist_name(cls, name):
        try:
            m = cls.get_product_by_name(name)
            return not m is None
        except:
            return False

    @classmethod
    def get_product_by_name(cls, name):
        try:
            return ProductMovieDetail.get(ProductMovieDetail.product_name == name)
        except:
            return None

    @classmethod
    def get_product_detail(cls, detail_id, product_type):
        if product_type == cls.get_product_type(movie_key):
            return ProductMovieDetail.get(ProductMovieDetail.id == detail_id)
        else:
            return None

    @classmethod
    def get_product_type(cls, key=movie_key):
        try:
            return ProductType.get(ProductType.key == key)
        except Exception as e:
            print("not found ProductType = ", key)
            raise e

    @classmethod
    def get_data_source(cls, source=base_source):
        try:
            return PublicDataSource.get(PublicDataSource.key == source)
        except Exception as e:
            print("not found PublicDataSource = ", source)
            raise e

    @classmethod
    def save_as_lbl(cls, data_map):
        if cls.exist_name(data_map["name"]):
            return
        product = ProductInfo()
        product_movie = ProductMovieDetail()

        # 产品
        product.product_name = data_map["name"]
        product.product_type = cls.get_product_type().id
        product.source = cls.get_data_source().id
        product.status = 0
        product.order_index = cls.get_last_order_index() + 1
        # 电影详情
        product_movie.about = data_map["about"]
        product_movie.area = ""
        product_movie.product_name = data_map["name"]
        product_movie.product_alias = data_map["name"]
        product_movie.release_time = datetime.datetime.strptime(data_map["time"].strip(), "%Y年%m月%d日").date()
        product_movie.rating = 0
        product_movie.rating_sum = 0
        product_movie.status = 1

        product_movie.save()

        # 设置id
        product.detail = product_movie.get_id()

        product.save()

        # 保存下载地址
        d_links = data_map["down_links"]
        if not d_links is None:
            for link in d_links:
                d = PublicDownloadAddress()
                d.download_url = link
                d.status = 1
                d.download_type = 1
                d.save()
                detail = ProductDownloadDetail()
                detail.address = d.get_id()
                detail.product = product.get_id()
                detail.save()

    @classmethod
    def get_last_order_index(cls):
        try:
            return ProductInfo.select(ProductInfo.order_index).order_by(ProductInfo.order_index.desc())[0].order_index
        except:
            return 0

    @classmethod
    def get_product_by_source(cls, source):
        source_id = cls.get_data_source(source).id

        list = ProductInfo.filter(ProductInfo.source != source_id).order_by(ProductInfo.id.desc())[0:10]
        return list

    @classmethod
    def save_as_douban(cls, product, result, source):
        detail = cls.get_product_detail(product.detail, product.product_type)
        detail.product_alias = result["sub_name"]
        detail.about = result["about"]
        detail.area = result["area"]
        detail.content = result["content"]
        detail.rating = result["rating"]
        detail.rating_sum = result["rating_sum"]
        detail.status = 1
        detail.save()

        img = PublicImages()
        img.image = result["image_url"]
        img.img_type = 1
        img.status = 1
        img.save()

        # 关系
        pro_img = ProductImagesDetail()
        pro_img.image = img.get_id()
        pro_img.product = product.id
        pro_img.save()

        product.source = cls.get_data_source(source).id
        product.status = 1
        product.save()

        cls.save_comment_info(product.id, result["comments"])

        print(product.product_name, "form source", source)
        # comments 评论信息保存
        # result["comments"]

    @classmethod
    def save_comment_info(cls, product_id, comments):

        if comments is None or len(comments) == 0:
            return

        for comment in comments:
            product_comment = ProductCommentInfo()
            product_comment.content = comment["content"]
            product_comment.user_name = comment["user_name"]
            product_comment.comment_time = datetime.datetime.strptime(comment["comment_time"].strip(),
                                                                      "%Y-%m-%d %H:%M:%S").date()

            product_comment.save()

            product_comment_detail = ProductCommentDetail()
            product_comment_detail.product = product_id
            product_comment_detail.comment_info = product_comment.get_id()
            product_comment_detail.save()
