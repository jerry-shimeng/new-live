from bs4 import BeautifulSoup

import config
from commons.http_utils import HttpUtils
from lbl.common import Common


class LblParser:
    @classmethod
    def run(cls, page):
        while page > 0:
            url = Common.get_url(page)
            cls.process(url)
            page = page - 1

    @classmethod
    def process(cls, url):
        list = cls.get_list(url)

        for detail in list:
            model = cls.detail(detail)

    @classmethod
    def get_list(cls, url):
        html = HttpUtils.get(url, headers=HttpUtils.get_header())
        soup = BeautifulSoup(html, config.features)
        list = soup.find(id="center")
        if list is None:
            return None
        list = list.find_all(class_="postlist")
        return list

    @classmethod
    def detail(cls, data):
        pass

    @classmethod
    def save(cls):
        pass
