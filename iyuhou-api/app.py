from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from service import product_api

app = Flask(__name__)

###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api = swagger.docs(Api(app), apiVersion='1.0')
# api = Api(app)
###################################

api.add_resource(product_api.ProductApi, "/product")



if __name__ == '__main__':
	app.run(debug=True)
