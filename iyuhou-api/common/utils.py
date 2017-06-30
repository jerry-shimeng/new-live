

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
 

 