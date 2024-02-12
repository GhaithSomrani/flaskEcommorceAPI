from datetime import datetime, timedelta
from math import ceil
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, or_, and_
from sqlalchemy.orm import aliased
from data_store_api import DataStoreAPI
from products_api import ProductsAPI
from database_model import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS support for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://userflask:Hunter2015@localhost/product_comparator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

ProductsAPI(app).register_routes()
DataStoreAPI(app).register_routes()

if __name__ == '__main__':
    app.run(debug=True)
