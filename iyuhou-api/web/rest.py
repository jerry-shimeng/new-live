import argparse

from flask_restful import Resource, reqparse

# Set the response code to 201 and return custom headers
# return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}
from common import result
from services.other_server import Downloads, Comments
from services.product_server import Products


class Product(Resource):
	def get(self, p_id) -> object:
		if p_id is None:
			return result.fail(-101, 'params error')
		p_id = int(p_id)
		if p_id <= 0:
			return result.fail(-101, 'params must greater than 0')
		
		return Products.get_detail(p_id)
	
	def put(self, p_id):
		return 'error', 500
	
	def post(self, p_id):
		return 'error', 500
	
	def delete(self, p_id):
		return 'error', 500


class ProductList(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('page', type=int, help='page')
	parser.add_argument('size', type=int, help='page')
	parser.add_argument('k', type=str, help='page')
	parser.add_argument('sort', type=int, help='排序类型')
	parser.add_argument('type', type=int, help='类型')
	parser.add_argument('online', type=bool, help='online?')
	
	def get(self) -> object:
		try:
			args = self.parser.parse_args()
			return Products.query(args)
		except Exception as e:
			return result.fail(-1, str(e))


class DownloadUrl(Resource):
	def get(self, p_id) -> object:
		return Downloads.get(p_id), 200


class ProductComment(Resource):
	def get(self, p_id) -> object:
		return Comments.get(p_id)
