import config

"""
http://www.bd-film.com/zx/23782.htm
"""


class Common:
	@staticmethod
	def get_features():
		return config.features
	
	@staticmethod
	def get_url(page):
		return "http://www.lbldy.com/movie/page/%d/" % page
