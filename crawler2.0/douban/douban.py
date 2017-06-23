from commons.enums import PublicSourceEnums
from dbaccess.db_access import DatabaseAccess, ProductInfo
from douban.douban_api import DoubanApi
import traceback

class DoubanContentParser:
    @classmethod
    def parse(cls, name: str):
        exist = DatabaseAccess.exist_name(name)
        print(exist)

    @classmethod
    def run(cls, size: int = 10):
        list = DatabaseAccess.get_product_by_source(PublicSourceEnums.DOUBAN_SOURCE, size)
        for l in list:
            print(l.product_name)
            try:
                detail = DoubanApi.get_movie(l)
                if detail is not None:
                    cls.save(l, detail)
            except Exception as e:
                traceback.print_exc()
                DatabaseAccess.update_fail(l.id)

    @classmethod
    def save(cls, product: ProductInfo, model: object):
        try:
            DatabaseAccess.save_as_douban(product, model, PublicSourceEnums.DOUBAN_SOURCE)
        except Exception as e:
            print(e)
            DatabaseAccess.update_fail(product.id)
