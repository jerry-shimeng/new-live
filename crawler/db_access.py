import datetime

from crawler.db import *


class DatabaseAccess:
    @classmethod
    def exist_name(cls, name):
        try:
            m = MovieDetail.get(MovieDetail.name == name)
            return not m is None
        except:
            return False

    @classmethod
    def save(cls, data_map):
        if cls.exist_name(data_map["name"]):
            return

        # self.save(name=name, time=time, tag=status, image=img, content=content, about=about, down_links=down_links)
        model = MovieDetail()
        model.about = data_map["about"]
        model.content = data_map["content"]
        model.name = data_map["name"]
        if "sub_name" in data_map.keys():
            model.sub_name = data_map["sub_name"]
        else:
            model.sub_name = None
        if "rating" in data_map.keys():
            model.rating = data_map["rating"]
            if model.rating is None:
                model.rating = 0
        else:
            model.rating = 0

        if "rating_sum" in data_map.keys():
            model.rating_sum = data_map["rating_sum"]
        else:
            model.rating_sum = 0

        model.release_time = datetime.datetime.strptime(data_map["time"].strip(), "%Y年%m月%d日").date()
        model.tag = data_map["tag"]
        model.status = 1
        # model.about = dict["about"]
        model.save()

        img = MovieImages()
        img.image = data_map["image_url"]
        img.movie = model.get_id()
        img.img_type = 1
        img.save()

        d_links = data_map["down_links"]
        if not d_links is None:
            for link in d_links:
                durl = MovieDownloadUrl()
                durl.download_url = link
                durl.movie = model.get_id()
                durl.save()
