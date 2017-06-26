import datetime
import decimal

import simplejson
from bs4 import BeautifulSoup


class DatetimeJSONEncoder(simplejson.JSONEncoder):
	"""可以序列化时间的JSON"""
	
	DATE_FORMAT = "%Y-%m-%d"
	TIME_FORMAT = "%H:%M:%S"
	
	def default(self, o):
		if isinstance(o, datetime.datetime):
			d = self.safe_new_datetime(o)
			return d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
		elif isinstance(o, datetime.date):
			d = self.safe_new_date(o)
			return d.strftime(self.DATE_FORMAT)
		elif isinstance(o, datetime.time):
			return o.strftime(self.TIME_FORMAT)
		elif isinstance(o, decimal.Decimal):
			return str(o)
		else:
			return super(DatetimeJSONEncoder, self).default(o)
	
	def safe_new_datetime(d):
		kw = [d.year, d.month, d.day]
		if isinstance(d, datetime.datetime):
			kw.extend([d.hour, d.minute, d.second, d.microsecond, d.tzinfo])
		return datetime.datetime(*kw)
	
	def safe_new_date(d):
		return datetime.date(d.year, d.month, d.day)


def is_blank(d):
	"""
	判断对象是否为空
	:param d:
	:return:
	"""
	if d is None:
		return True
	if isinstance(d, dict):
		return d == {}
	
	return False


def format_content(s):
	if s is None or len(s) == 0:
		return ''
	
	return s.strip()


def convert_html_to_json(html):
	result = {}
	try:
		soup = BeautifulSoup(html, 'lxml')
		soup = soup.find(id='info')
		
		# 获取所有分类
		categorys = get_class_type(soup)
		result['categorys'] = categorys
		
		result['area'] = get_html_value(soup, '制片国家/地区:')
		result['language'] = get_html_value(soup, '语言:')
		
		soup = soup.find_all_next('span')
		# for s in soup:
		# 	print(s)
		result['director'] = get_soup_value(soup, '导演')
		result['screenwriter'] = get_soup_value(soup, '编剧')
		result['actor'] = get_soup_value(soup, '主演')
		result['time'] = get_soup_value(soup, '上映日期:')
		result['duration'] = get_soup_value(soup, '片长:')
		
	except:
		print('')
	
	return result


def get_class_type(soup):
	ll = soup.find_all(property="v:genre")
	
	r = (l.string for l in ll)
	return list(r)


def get_soup_value(soup: BeautifulSoup, name: str):
	for s1 in soup:
		if s1.string == name:
			# 找下一个
			return s1.find_next_sibling().string
	return ''


def get_html_value(soup: BeautifulSoup, name: str):
	value = None
	
	for s in soup.strings:
		if s == name:
			value = ''
			continue
		if value is not None and len(value) == 0:
			return s.strip() if s is not None else ''
	
	return ''
