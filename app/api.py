from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import PartnersSchema, ClientsSchema, PerksSchema, Partners, Clients, Perks
from app.db import db, ma
from app.config import SQLALCHEMY_DATABASE_URI


auth = HTTPBasicAuth()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    ma.init_app(app)
    return app


app = create_app()


@auth.get_user_roles
def get_user_roles(username):
    return user_data.get(username, {}).get("role")


@app.route("/admin")
@auth.login_required(role="admin")
def admins_only():
    return "Hello {}, you are an admin!".format(auth.current_user())


@app.route("/user")
@auth.login_required(role="user")
def users_only():
    return "Hello {}!".format(auth.current_user())


user_data = {
    "admin": {"password": generate_password_hash("admin"), "role": ["user", "admin"]},
    "user": {"password": generate_password_hash("user"), "role": ["user"]},
}


@auth.verify_password
def verify_password(username, password):
    if username in user_data and check_password_hash(
        user_data.get(username, {}).get("password"), password
    ):
        return username
    else:
        return False


partner_schema = PartnersSchema()
partners_schema = PartnersSchema(many=True)
client_schema = ClientsSchema()
clients_schema = ClientsSchema(many=True)
perk_schema = PerksSchema()
perks_schema = PerksSchema(many=True)


class PartnerManager(Resource):
    @staticmethod
    @auth.login_required(role="user")
    def get():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            partnerss = Partners.query.all()
            return jsonify(partners_schema.dump(partnerss))
        paartners = Partners.query.get(id)
        return jsonify(partner_schema.dump(paartners))

    @staticmethod
    @auth.login_required(role="admin")
    def post():
        name = request.json["name"]
        address = request.json["address"]
        email = request.json["email"]
        # date_added = request.json['date_added']

        partnerss = Partners(name, address, email)
        db.session.add(partnerss)
        db.session.commit()

        return jsonify({"Message": f"partner {partnerss.id} {name} inserted."})

    @staticmethod
    @auth.login_required(role="admin")
    def put():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            return jsonify({"Message": "Must provide the user ID"})

        partnerss = Partners.query.get(id)
        name = request.json["name"]
        address = request.json["address"]
        email = request.json["email"]
        ##date_added = request.json['date_added']

        partnerss.name = name
        partnerss.address = address
        partnerss.email = email
        ##partnerss.date_added = date_added

        db.session.commit()
        return jsonify({"Message": f"Partner {id} {name} altered."})

    @staticmethod
    @auth.login_required(role="admin")
    def delete():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            return jsonify({"Message": "Must provide the partner ID"})

        partnerss = Partners.query.get(id)
        db.session.delete(partnerss)
        db.session.commit()

        return jsonify({"Message": f"partner {str(id)} deleted."})


class ClientsManager(Resource):
    @staticmethod
    @auth.login_required(role="admin")
    def get():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            clientss = Clients.query.all()
            return jsonify(clients_schema.dump(clientss))
        cliients = Clients.query.get(id)
        return jsonify(client_schema.dump(cliients))

    @staticmethod
    @auth.login_required(role="admin")
    def put():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            return jsonify({"Message": "Must provide the user ID"})

        clientss = Clients.query.get(id)
        name = request.json["name"]
        address = request.json["address"]
        email = request.json["email"]
        ##date_added = request.json['date_added']

        clientss.name = name
        clientss.address = address
        clientss.email = email
        ##partnerss.date_added = date_added

        db.session.commit()
        return jsonify({"Message": f"Partner {id} {name} altered."})

    @staticmethod
    @auth.login_required(role="admin")
    def post():
        name = request.json["name"]
        address = request.json["address"]
        email = request.json["email"]

        clientss = Clients(name, address, email)
        db.session.add(clientss)
        db.session.commit()

        return jsonify({"Message": f"client {clientss.id} {name} inserted."})

    @staticmethod
    @auth.login_required(role="admin")
    def delete():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            return jsonify({"Message": "Must provide the client ID"})

        clientss = Clients.query.get(id)
        db.session.delete(clientss)
        db.session.commit()

        return jsonify({"Message": f"client {str(id)} deleted."})


class PerksManager(Resource):
    @staticmethod
    @auth.login_required(role="user")
    def get():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            perkss = Perks.query.all()
            return jsonify(perks_schema.dump(perkss))
        peerks = Perks.query.get(id)
        return jsonify(perk_schema.dump(peerks))

    @staticmethod
    @auth.login_required(role="admin")
    def post():
        name = request.json["name"]
        provider_id = request.json["provider_id"]
        quantity_available = request.json["quantity_available"]

        perkss = Perks(name, provider_id, quantity_available)
        db.session.add(perkss)
        db.session.commit()

        return jsonify({"Message": f"Perk {perkss.id} {name} inserted."})

    @staticmethod
    @auth.login_required(role="admin")
    def delete():
        try:
            id = request.args["id"]
        except Exception as _:
            id = None

        if not id:
            return jsonify({"Message": "Must provide the perk ID"})

        perkss = Perks.query.get(id)
        db.session.delete(perkss)
        db.session.commit()

        return jsonify({"Message": f"Perk {perkss.id} deleted."})


@app.route("/")
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())
