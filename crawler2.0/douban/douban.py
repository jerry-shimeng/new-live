from dbaccess.db_access import DatabaseAccess


class DoubanContentParser:
	@classmethod
	def parse(cls, name):
		exist = DatabaseAccess.exist_name(name)
		print(exist)
