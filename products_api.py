import json
from math import ceil
from flask import request, jsonify
from sqlalchemy.sql import desc, distinct, func
from database_model import data_product
from datetime import datetime, timedelta
from database_model import db
from sqlalchemy.sql import func as sql_func


class ProductsAPI:
    def __init__(self, app):
        self.app = app

    def register_routes(self):
        @self.app.route('/api/products', methods=['GET'])
        def get_products():
            name = request.args.get('name', default=None, type=str)
            brand = request.args.get('brand', default=None, type=str)
            category = request.args.get('category', default=None, type=str)
            start_date = request.args.get('start_date', default=None, type=str)
            end_date = request.args.get('end_date', default=None, type=str)
            min_price = request.args.get('min_price', default=None, type=float)
            max_price = request.args.get('max_price', default=None, type=float)
            store = request.args.get('store', default=None, type=str)
            page = request.args.get('page', default=1, type=int)
            page_size = request.args.get('page_size', default=10, type=int)
            sort_by = request.args.get(
                'sort_by', default='add_date', type=str)
            sort_order = request.args.get(
                'sort_order', default='desc', type=str)

            if not store:
                return jsonify({'error': 'Store name is required.'}), 400

            valid_sort_fields = ['price', 'reference',
                                 'name', 'category', 'brand', 'add_date']
            if sort_by not in valid_sort_fields:
                return jsonify(message=f"Invalid sort field. Available options: {', '.join(valid_sort_fields)}"), 400

            valid_sort_orders = ['asc', 'desc']
            if sort_order not in valid_sort_orders:
                return jsonify(message=f"Invalid sort order. Available options: {', '.join(valid_sort_orders)}"), 400

            query = db.session.query(data_product)

            if name:
                query = query.filter(data_product.name.ilike(f"%{name}%"))

            if store:
                query = query.filter(data_product.store.ilike(f"%{store}%"))

            if brand:
                query = query.filter(data_product.brand.ilike(f"%{brand}%"))

            if category:
                query = query.filter(
                    data_product.category.ilike(f"%{category}%"))

            if start_date:
                query = query.filter(data_product.add_date >= start_date)

            if end_date:
                query = query.filter(data_product.add_date <= end_date)

            if min_price is not None:
                query = query.filter(data_product.price >= min_price)

            if max_price is not None:
                query = query.filter(data_product.price <= max_price)

            query = query.order_by(data_product.reference, data_product.add_date.desc(
            )).distinct(data_product.reference)

            if sort_order == 'asc':
                query = query.order_by(getattr(data_product, sort_by))
            else:
                query = query.order_by(getattr(data_product, sort_by).desc())

            offset = (page - 1) * page_size

            products = query.offset(offset).limit(page_size).all()

            result = {
                'total_pages': (query.count() + page_size - 1) // page_size,
                'current_page': page,
                'page_size': len(products),
                'products': [{
                    'id': p.id,
                    'store': p.store,
                    'reference': p.reference,
                    'name': p.name,
                    'price': p.price,
                    'category': p.category,
                    'availability': p.availability,
                    'brand': p.brand,
                    'url': p.url,
                    'imageurl': p.imageurl,
                    'add_date': p.add_date
                } for p in products]
            }

            return jsonify(result)

        @self.app.route('/api/grouped-products', methods=['GET'])
        def get_grouped_products():

            store = request.args.get('store', default=None, type=str)

            if not store:
                return jsonify({'error': 'Store name is required.'}), 400

            grouped_data = db.session.query(
                data_product.brand,
                data_product.category
            ).filter(data_product.store.ilike(f"%{store}%")).order_by(data_product.add_date.desc())

            grouped_data = grouped_data.group_by(
                data_product.brand,
                data_product.category
            ).all()

            brands = []
            categories = []

            for row in grouped_data:
                brand = row[0] if row[0] else 'Unknown Brand'
                category = row[1] if row[1] else 'Unknown Category'

                if brand not in brands:
                    brands.append(brand)
                if category not in categories:
                    categories.append(category)

            return jsonify({
                'brands': brands,
                'categories': categories
            })

        @self.app.route('/api/products-by-reference', methods=['GET'])
        def get_products_by_reference():

            reference = request.args.get('reference', default=None, type=str)
            store = request.args.get('store', default=None, type=str)

            if reference is None or store is None:
                return jsonify(message="Reference and store parameters are required"), 400

            products = data_product.query.filter_by(
                reference=reference, store=store).all()

            return jsonify([{
                'id': p.id,
                'store': p.store,
                'reference': p.reference,
                'name': p.name,
                'price': p.price,
                'category': p.category,
                'availability': p.availability,
                'brand': p.brand,
                'url': p.url,
                'imageurl': p.imageurl,
                'add_date': p.add_date
            } for p in products])

        def calculate_total_pages(total_items, page_size):
            return (total_items + page_size - 1) // page_size

        @self.app.route('/api/new-products', methods=['GET'])
        def get_new_products():

            date_str = request.args.get('date', default=None, type=str)
            store = request.args.get('store', default=None, type=str)
            category = request.args.get('category', default=None, type=str)
            brand = request.args.get('brand', default=None, type=str)
            page = request.args.get('page', default=1, type=int)
            page_size = request.args.get('page_size', default=10, type=int)

            if date_str is None or store is None:
                return jsonify(message="Date and store parameters are required"), 400

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify(message="Invalid date format. Use YYYY-MM-DD"), 400

            previous_day = date - timedelta(days=1)

            previous_day_references = (
                db.session.query(data_product.reference)
                .filter(data_product.add_date >= previous_day, data_product.add_date < date)
                .all()
            )
            offset = (page - 1) * page_size

            new_products_query = data_product.query.filter(
                data_product.add_date >= date,
                data_product.add_date < date + timedelta(days=1),
                ~data_product.reference.in_([ref[0] for ref in previous_day_references]),
                data_product.store.ilike(f"%{store}%")
            )

            if category:
                new_products_query = new_products_query.filter(data_product.category.ilike(f"%{category}%"))
            if brand:
                new_products_query = new_products_query.filter(data_product.brand.ilike(f"%{brand}%"))

            total_records = new_products_query.count()

            new_products = new_products_query.offset(offset).limit(page_size).all()

            total_pages = ceil(total_records / page_size)
            current_page = page
            page_length = len(new_products)

            return jsonify({
                'current_page': current_page,
                'page_size': page_length,
                'total_pages': total_pages,
                'products': [{
                    'id': p.id,
                    'store': p.store,
                    'reference': p.reference,
                    'name': p.name,
                    'price': p.price,
                    'category': p.category,
                    'availability': p.availability,
                    'brand': p.brand,
                    'url': p.url,
                    'imageurl': p.imageurl,
                    'add_date': p.add_date
                } for p in new_products]
            })

        @self.app.route('/api/price_changes', methods=['GET'])
        def get_price_changes():
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            store_name = request.args.get('store')
            category = request.args.get('category')
            brand = request.args.get('brand')

            if not start_date or not end_date or not store_name:
                return jsonify({'error': 'Start date, end date, and store name are required.'}), 400

            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

            if start_date >= end_date:
                return jsonify({'error': 'Start date must be before end date.'}), 400

            subquery = db.session.query(
                data_product.reference,
                data_product.availability,
                data_product.brand,
                data_product.category,
                data_product.imageurl,
                data_product.name,
                data_product.url,
                data_product.add_date,
                func.group_concat(func.json_object('date', func.date(
                    data_product.add_date), 'value', data_product.price)).label('prices'),
                func.count(distinct(data_product.price)).label('price_count')
            ).filter(
                func.date(data_product.add_date).between(
                    start_date, end_date),
                data_product.store == store_name
            )

            if category:
                subquery = subquery.filter(data_product.category.like(f'%{category}%'))
            if brand:
                subquery = subquery.filter(data_product.brand.like(f'%{brand}%'))

            subquery = subquery.group_by(data_product.reference, data_product.name).having(func.count(distinct(func.date(data_product.add_date))) >= 2).order_by(data_product.add_date.desc()).subquery()

            query = db.session.query(
                subquery.c.availability,
                subquery.c.brand,
                subquery.c.category,
                subquery.c.imageurl,
                subquery.c.url,
                subquery.c.name,
                subquery.c.reference,
                subquery.c.prices
            ).filter(subquery.c.price_count > 1)

            result = [
                {
                    'availability': availability,
                    'brand': brand,
                    'category': category,
                    'imageurl': imageurl,
                    'url': url,
                    'name': name,
                    'reference': reference,
                    'prices':  json.loads("[" + prices + "]")
                }
                for availability, brand, category, imageurl, url, name, reference, prices in query.all()
            ]

            return jsonify(result)

        @self.app.route('/api/removed-products', methods=['GET'])
        def get_removed_products():
                date_str = request.args.get('date', default=None, type=str)
                store = request.args.get('store', default=None, type=str)
                category = request.args.get('category', default=None, type=str)
                brand = request.args.get('brand', default=None, type=str)
                page = request.args.get('page', default=1, type=int)
                page_size = request.args.get('page_size', default=10, type=int)

                if date_str is None or store is None:
                    return jsonify(message="Date and store parameters are required"), 400

                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return jsonify(message="Invalid date format. Use YYYY-MM-DD"), 400

                next_day = date + timedelta(days=1)

                current_day_references = (
                    db.session.query(data_product.reference)
                    .filter(data_product.add_date < next_day)
                    .all()
                )

                current_day_references_list = [ref[0] for ref in current_day_references]

                removed_products_query = data_product.query.filter(
                    data_product.add_date < next_day,
                    ~data_product.reference.in_(current_day_references_list),
                    data_product.store.ilike(f"%{store}%")
                )

                if category:
                    removed_products_query = removed_products_query.filter(data_product.category.ilike(f"%{category}%"))
                if brand:
                    removed_products_query = removed_products_query.filter(data_product.brand.ilike(f"%{brand}%"))

                offset = (page - 1) * page_size

                total_records = removed_products_query.count()

                removed_products = removed_products_query.offset(offset).limit(page_size).all()

                total_pages = ceil(total_records / page_size)
                current_page = page
                page_length = len(removed_products)

                return jsonify({
                    'current_page': current_page,
                    'page_size': page_length,
                    'total_pages': total_pages,
                    'products': [{
                        'id': p.id,
                        'store': p.store,
                        'reference': p.reference,
                        'name': p.name,
                        'price': p.price,
                        'category': p.category,
                        'availability': p.availability,
                        'brand': p.brand,
                        'url': p.url,
                        'imageurl': p.imageurl,
                        'add_date': p.add_date
                    } for p in removed_products]
                })