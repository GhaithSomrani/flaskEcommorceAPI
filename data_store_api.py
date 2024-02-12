from flask import request, jsonify
from database_model import data_store


class DataStoreAPI:
    def __init__(self, app):
        self.app = app

    def register_routes(self):
        @self.app.route('/api/stores', methods=['GET'])
        def get_data_stores():
            # Get all stores from the database
            stores = data_store.query.all()

            # Create a list of stores in JSON format
            store_list = [{
                'id': store.id,
                'name': store.name,
                'link': store.link,
                'image': store.imageurl,
            } for store in stores]

            # Return the list of stores as a JSON response
            return jsonify(store_list)

# This code is used to create an API for managing data stores
# The code is organized into a class and methods that perform specific tasks
# The class is initialized with the Flask app object
# The register_routes method is used to create API endpoints
# The GET method is used to retrieve all stores from the database
# The data_store object is queried to get all stores, and a list of stores in JSON format is created
# The list of stores is returned as a JSON response