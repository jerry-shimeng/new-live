import json

from flask_restful_swagger import swagger



@swagger.model
class Result(dict):
	def __init__(self, code=0, message='', data=None):
		self['code'] = code
		self['message'] = message
		self['data'] = data
		
		# dict.__init__(self, code=code, message=message, data=data)
	
	@classmethod
	def success(cls, d):
		return cls(0, "", d)
	
	@classmethod
	def success(cls):
		return cls(0)
	
	@classmethod
	def fail(cls, code, msg=''):
		return cls(code, msg, None)
