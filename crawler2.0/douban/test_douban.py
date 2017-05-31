import unittest

from douban.douban import DoubanContentParser


class TestDouban(unittest.TestCase):
	def setUp(self):
		self.seq = range(10)
	
	def test_parse(self):
		DoubanContentParser.run(10)
		
if __name__ == '__main__':
	unittest.main()
