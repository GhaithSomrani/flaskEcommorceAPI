from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class data_product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(255))
    reference = db.Column(db.String(255))
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category = db.Column(db.String(255))
    availability = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    url = db.Column(db.String(255))
    imageurl = db.Column(db.String(255), index=True)
    add_date = db.Column(db.DateTime, index=True)


class data_store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    link = db.Column(db.String(255))
    imageurl = db.Column(db.String(255))
