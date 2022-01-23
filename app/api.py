import email
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import (
    PartnersSchema,
    ClientsSchema,
    PerksSchema,
    UsersSchema,
    Partners,
    Clients,
    Perks,
    Users,
)
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
def get_user_roles(useremail):
    if Users.query.get(useremail).is_admin:
        return "admin"
    else:
        return "user"


@auth.verify_password
def verify_password(useremail, password):
    user = Users.query.get(useremail)
    if user and check_password_hash(user.password, password):
        return useremail
    else:
        return False


@app.route("/admin")
@auth.login_required(role="admin")
def admins_only():
    return "Hello {}, you are an admin!".format(auth.current_user())


@app.route("/user")
@auth.login_required()
def users_only():
    return "Hello {}!".format(auth.current_user())


partner_schema = PartnersSchema()
partners_schema = PartnersSchema(many=True)
client_schema = ClientsSchema()
clients_schema = ClientsSchema(many=True)
perk_schema = PerksSchema()
perks_schema = PerksSchema(many=True)
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


class UserManager(Resource):
    @staticmethod
    @auth.login_required(role="admin")
    def get():

        email = request.args.get("email")
        if not email:
            userss = Users.query.all()
            return jsonify(users_schema.dump(userss))
        uusers = Users.query.get(id)
        return jsonify(user_schema.dump(uusers))

    @staticmethod
    @auth.login_required(role="admin")
    def post():
        name = request.json["name"]
        password = request.json["password"]
        is_admin = request.json["is_admin"]
        email = request.json["email"]

        userss = Users(
            name=name,
            password=generate_password_hash(password),
            is_admin=is_admin,
            email=email,
        )
        db.session.add(userss)
        db.session.commit()

        return jsonify({"Message": f"user {name} inserted."})

    @staticmethod
    @auth.login_required(role="admin")
    def put():
        email = request.args.get("email")
        if not email:
            return jsonify({"Message": "Must provide the user email"})

        userss = Users.query.get(email)
        name = request.json["name"]
        password = request.json["password"]
        is_admin = request.json["is_admin"]
        email = request.json["email"]

        userss.name = name
        userss.password = generate_password_hash(password)
        userss.is_admin = is_admin
        userss.email = email

        db.session.commit()
        return jsonify({"Message": f"User {name} altered."})

    @staticmethod
    @auth.login_required(role="admin")
    def delete():

        email = request.args.get("email")

        if not email:
            return jsonify({"Message": "Must provide the user email"})

        userss = Users.query.get(email)
        if userss:
            db.session.delete(userss)
            db.session.commit()
            return jsonify({"Message": "User deleted."})
        else:
            return jsonify({"Message": "user not found"})


class PartnerManager(Resource):
    @staticmethod
    @auth.login_required
    def get():

        id = request.args.get("id")
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

        partnerss = Partners(name, address, email)
        db.session.add(partnerss)
        db.session.commit()

        return jsonify({"Message": f"partner {partnerss.id} {name} inserted."})

    @staticmethod
    @auth.login_required(role="admin")
    def put():
        id = request.args.get("id")
        if not id:
            return jsonify({"Message": "Must provide the partner ID"})

        partnerss = Partners.query.get(id)
        name = request.json["name"]
        address = request.json["address"]
        email = request.json["email"]

        partnerss.name = name
        partnerss.address = address
        partnerss.email = email

        db.session.commit()
        return jsonify({"Message": f"Partner {id} {name} altered."})

    @staticmethod
    @auth.login_required(role="admin")
    def delete():

        id = request.args.get("id")

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
        id = request.args.get("id")

        if not id:
            clientss = Clients.query.all()
            return jsonify(clients_schema.dump(clientss))
        cliients = Clients.query.get(id)
        return jsonify(client_schema.dump(cliients))

    @staticmethod
    @auth.login_required(role="admin")
    def put():

        id = request.args.get("id")

        if not id:
            return jsonify({"Message": "Must provide the cLient ID"})

        clientss = Clients.query.get(id)
        name = request.json["name"]
        address = request.json["address"]
        email = request.json["email"]

        clientss.name = name
        clientss.address = address
        clientss.email = email

        db.session.commit()
        return jsonify({"Message": f"Client {id} {name} altered."})

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

        id = request.args.get("id")

        if not id:
            return jsonify({"Message": "Must provide the client ID"})

        clientss = Clients.query.get(id)
        db.session.delete(clientss)
        db.session.commit()

        return jsonify({"Message": f"client {str(id)} deleted."})


class PerksManager(Resource):
    @staticmethod
    @auth.login_required
    def get():
        id = request.args.get("id")

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
        id = request.args.get("id")

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
