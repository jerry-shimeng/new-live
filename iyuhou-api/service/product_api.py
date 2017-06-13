from flask import jsonify
from flask_restful import Resource, fields
from flask_restful_swagger import swagger

from vo.result import Result


class ProductApi(Resource):
	@swagger.operation(
		notes='some really good notes',
		responseClass=Result.__name__,
		nickname='upload',
		parameters=[
			{
				"name": "body",
				"description": "blueprint object that needs to be added. YAML.",
				"required": True,
				"allowMultiple": False,
				"dataType": "Str",
				"paramType": "body"
			}
		],
		responseMessages=[
			{
				"code": 201,
				"message": "Created. The URL of the created blueprint should be in the Location header"
			},
			{
				"code": 405,
				"message": "Invalid input"
			}
		]
	)
	def get(self):
		res = Result.success()
		res['message'] = 123
		return jsonify(res)
