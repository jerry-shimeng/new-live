import datetime

import django
from django.db import models


# 敏感词词库
class SensitiveWords(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=20)
    # 区分关键词 0为系统敏感关键词 1为用户敏感关键词 2通用或其他敏感关键词
    tag = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "sensitive_words"


class ProductInfo(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_type = models.ForeignObject

    class Meta:
        db_table = "product_info"


class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    describe = models.CharField(max_length=200, null=True)
    status = models.SmallIntegerField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = "product_type"
