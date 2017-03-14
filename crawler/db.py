from peewee import *

database = MySQLDatabase('test_db1', **{'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'root123'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class MovieDetail(BaseModel):
    about = TextField(null=True)
    content = TextField(null=True)
    create_time = DateTimeField()
    name = CharField()
    release_time = DateField(null=True)
    status = IntegerField()
    tag = CharField(null=True)

    class Meta:
        db_table = 'movie_detail'


class MovieDownloadUrl(BaseModel):
    download_url = CharField()
    movie = IntegerField(db_column='movie_id')

    class Meta:
        db_table = 'movie_download_url'


class MovieImages(BaseModel):
    image = CharField()
    movie = IntegerField(db_column='movie_id')

    class Meta:
        db_table = 'movie_images'
