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
    def save(cls, dict):
        if cls.exist_name(dict["name"]):
            return

        # self.save(name=name, time=time, tag=status, image=img, content=content, about=about, down_links=down_links)
        model = MovieDetail()
        model.about = dict["about"]
        model.content = dict["content"]
        model.name = dict["name"]
        model.release_time = datetime.datetime.strptime(dict["time"].strip(), "%Y年%m月%d日").date()
        model.tag = dict["tag"]
        model.status = 1
        # model.about = dict["about"]
        model.save()

        img = MovieImages()
        img.image = dict["image"]
        img.movie = model.get_id()
        img.save()

        d_links = dict["down_links"]
        if not d_links is None:
            for link in d_links:
                durl = MovieDownloadUrl()
                durl.download_url = link
                durl.movie = model.get_id()
                durl.save()
