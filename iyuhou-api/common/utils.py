from bs4 import BeautifulSoup


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
		
		print(result)
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
