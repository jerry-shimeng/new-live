import json

import httplib2

from commons.utils import DatetimeJSONEncoder
from logger_proxy import logger


class HttpUtils:
	@classmethod
	def get(cls, url, headers=None, recall=False, encoding='utf-8'):
		try:
			return cls.get_not_decode(url).decode(encoding)
		except UnicodeDecodeError as e:
			if not recall:
				return cls.get(url, headers, recall=True, encoding="ISO-8859-1")
			else:
				logger.error(e)
				return ""
		except TimeoutError:
			return ""
	
	@classmethod
	def get_not_decode(cls, url, headers=None):
		h = httplib2.Http()
		(req_headers, content) = h.request(url, method="GET", body=None, headers=headers)
		return content
	
	@classmethod
	def post(cls, address, data, headers=None, encoding='utf-8'):
		body = None
		if type(data) is str:
			body = data
		else:
			body = json.dumps(data, cls=DatetimeJSONEncoder)
		
		h = httplib2.Http()
		
		# body = bytes(body,encoding="utf-8")
		logger.info(body)
		(req_headers, content) = h.request(address, method="POST", body=body)
		return content.decode(encoding)
	
	@classmethod
	def get_header(cls):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
			# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
		}
		return headers
