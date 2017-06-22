from common import utils
from dal.db import PublicDownloadDAL, ProductCommentDAL


class Downloads:
	@classmethod
	def get(cls, id):
		details = PublicDownloadDAL.get_address(id)
		result = list(map(lambda x: x['download_url'], details))
		return result


class Comments:
	@classmethod
	def get(cls, id):
		details = ProductCommentDAL.get(id)
		
		res = list(
			map(lambda x: {'content': utils.format_content(x['content']), 'name': x['user_name'],
			               'time': str(x['comment_time'])}, details))
		
		return res
