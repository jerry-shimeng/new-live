import datetime

import django
from django.db import models


# Create your models here.

# 电影详情
class MovieDetail(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sub_name = models.CharField(max_length=100, null=True)
    rating = models.FloatField(default=0)
    rating_sum = models.IntegerField(default=0)
    release_time = models.DateField(null=True, blank=True, default=datetime.date.today())
    about = models.TextField(null=True)
    content = models.TextField(null=True)
    tag = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    # movie_type = models.
    status = models.SmallIntegerField(default=1)
    create_time = models.TimeField(auto_created=True, default=django.utils.timezone.now)
    source = models.CharField(max_length=100, null=True)

    def get_desc(self):
        return self.content[0:20] + "..."

    def datetime_format(self):
        return datetime.datetime.strftime(self.release_time, "%Y-%m-%d")

    class Meta:
        db_table = 'movie_detail'
 

# 电影海报图片
class MovieImages(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieDetail, null=True)
    image = models.CharField(max_length=500)
    # 图片类型 1：海报  2：剧照
    img_type = models.SmallIntegerField(default=1, null=True)

    class Meta:
        db_table = 'movie_images'


# 电影下载地址
class MovieDownloadUrl(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieDetail, null=True)
    download_url = models.CharField(max_length=1000)

    class Meta:
        db_table = 'movie_download_url'


class MovieType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # 删除字段
    status = models.SmallIntegerField(default=1)

    class Meta:
        db_table = "movie_type"


class MovieTypeDetail(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieDetail)
    movie_type = models.ForeignKey(MovieType)

    class Meta:
        db_table = "movie_type_detail"


# 敏感词词库
class SensitiveWords(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=20)
    # 区分关键词 0为系统敏感关键词 1为用户敏感关键词 2通用或其他敏感关键词
    tag = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "sensitive_words"
