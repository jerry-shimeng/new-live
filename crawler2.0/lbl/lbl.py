from lbl.lbl_parser import LblParser


class LblContentParser:
	@classmethod
	def run(cls, page: int = 2):
		LblParser.run(page)
