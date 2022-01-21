import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    address = db.Column(db.String(32))
    email = db.Column(db.String(32))
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, address, email):
        self.name = name
        self.address = address
        self.email = email


class PartnersSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "address", "email", "date_added")


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    address = db.Column(db.String(32))
    email = db.Column(db.String(32))

    def __init__(self, name, address, email):
        self.name = name
        self.address = address
        self.email = email


class Perks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("partners.id"))
    quantity_available = db.Column(db.Integer, nullable=False)

    def __init__(self, name, provider_id, quantity_available):
        self.name = name
        self.provider_id = provider_id
        self.quantity_available = quantity_available


class ClientsSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "address", "email")


class PerksSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "provider_id", "quantity_available")
