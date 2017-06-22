from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from web.rest import *

app = Flask(__name__)
api = Api(app)


api.add_resource(Product, '/v1/detail/<p_id>')
api.add_resource(DownloadUrl, '/v1/down/<p_id>')
api.add_resource(ProductComment, '/v1/comment/<p_id>')
api.add_resource(ProductList, '/v1/list')


if __name__ == '__main__':
    app.run(debug=True)