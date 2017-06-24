import logger_proxy
from dbaccess.db_access import PublicDataAccess

cate_list = []
logger = logger_proxy.get_logger()


def get_cate_id(name: str, parent=1):
	"""
	分类信息缓存
	:param name:
	:param parent:
	:return:
	"""
	if name is None or len(name.strip()) == 0:
		return 0
	
	r = list(filter(lambda x: x['key'] == name, cate_list))
	
	if len(r) == 0:
		cate = load_cate_by_name(name, parent)
		if cate is not None:
			cate_list.append(cate)
	else:
		cate = cate_list[0]
	
	return 0 if cate is None else cate['id']


def load_cate_by_name(name, parent):
	"""
	数据库里面取出分类数据
	:return:
	"""
	try:
		d = PublicDataAccess.get_categorys_by_name(name, parent)
		
		if d is None:
			d = PublicDataAccess.save_categorys(name, parent)
		
		return d
	except Exception as e:
		logger.error('load_cate_by_name', e)
