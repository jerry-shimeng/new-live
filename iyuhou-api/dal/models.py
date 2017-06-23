from peewee import *
from config import database, db_name
database = MySQLDatabase(db_name,
                         **database)


class UnknownField(object):
	def __init__(self, *_, **__): pass


class BaseModel(Model):
	class Meta:
		database = database


class ProductCommentDetail(BaseModel):
	comment_info = IntegerField(db_column='comment_info_id', index=True)
	product = IntegerField(db_column='product_id', index=True)
	
	class Meta:
		db_table = 'product_comment_detail'


class ProductCommentInfo(BaseModel):
	comment_time = DateField()
	content = TextField()
	user_name = CharField()
	
	class Meta:
		db_table = 'product_comment_info'


class ProductDownloadDetail(BaseModel):
	address = IntegerField(db_column='address_id', index=True)
	product = IntegerField(db_column='product_id', index=True)
	
	class Meta:
		db_table = 'product_download_detail'


class ProductImagesDetail(BaseModel):
	image = IntegerField(db_column='image_id', index=True)
	product = IntegerField(db_column='product_id', index=True)
	
	class Meta:
		db_table = 'product_images_detail'


class ProductInfo(BaseModel):
	create_time = DateTimeField()
	detail = IntegerField()
	order_index = IntegerField(index=True, null=True)
	product_name = CharField(index=True)
	product_type = IntegerField(db_column='product_type_id', index=True)
	source = IntegerField(db_column='source_id', index=True)
	status = IntegerField()
	update_time = DateTimeField()
	
	class Meta:
		db_table = 'product_info'


class ProductMovieDetail(BaseModel):
	about = TextField(null=True)
	area = CharField(null=True)
	content = TextField(null=True)
	douban = IntegerField(db_column='douban_id', null=True)
	product_alias = CharField()
	product_name = CharField()
	rating = CharField(index=True, null=True)
	rating_sum = IntegerField()
	release_time = DateField(null=True)
	status = IntegerField()
	
	class Meta:
		db_table = 'product_movie_detail'


class ProductSubTypeDetail(BaseModel):
	product = IntegerField(db_column='product_id', index=True)
	sub_type = IntegerField(db_column='sub_type_id', index=True)
	
	class Meta:
		db_table = 'product_sub_type_detail'


class ProductType(BaseModel):
	create_time = DateTimeField()
	describe = CharField(null=True)
	key = CharField()
	name = CharField()
	parent = IntegerField(db_column='parent_id')
	status = IntegerField()
	
	class Meta:
		db_table = 'product_type'


class PublicDataSource(BaseModel):
	create_time = DateTimeField()
	key = CharField()
	source_name = CharField()
	source_type = IntegerField()
	status = IntegerField()
	
	class Meta:
		db_table = 'public_data_source'


class PublicDictionary(BaseModel):
	desc = TextField(null=True)
	key = CharField()
	value = CharField()
	
	class Meta:
		db_table = 'public_dictionary'


class PublicDownloadAddress(BaseModel):
	create_time = DateTimeField()
	download_type = IntegerField()
	download_url = CharField()
	status = IntegerField()
	
	class Meta:
		db_table = 'public_download_address'


class PublicImages(BaseModel):
	create_time = DateTimeField()
	image = CharField()
	img_type = IntegerField()
	status = IntegerField()
	
	class Meta:
		db_table = 'public_images'


class SensitiveWords(BaseModel):
	word = CharField()
	word_type = IntegerField()
	
	class Meta:
		db_table = 'sensitive_words'
