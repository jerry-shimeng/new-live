from flask import json

from common import utils, result
from dal.db import PublicDownloadDAL, ProductCommentDAL


class Downloads:
	@classmethod
	def get(cls, id):
		details = PublicDownloadDAL.get_address(id)
		details = list(details)
		
		details = list(map(lambda x: {"url": json.loads(x['download_url']), 'type': x['download_type']}, details))
		
		return result.of(details)


class Comments:
	@classmethod
	def get(cls, id):
		details = ProductCommentDAL.get(id)
		
		res = list(
			map(lambda x: {'comment': utils.format_content(x['content']), 'name': x['user_name'],
			               'time': str(x['comment_time']), 'pic': ''}, details))
		
		return result.of(res)
