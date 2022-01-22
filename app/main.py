from flask_restful import Api
from app.api import app, PerksManager, ClientsManager, PartnerManager, UserManager




api = Api(app)
api.add_resource(UserManager, "/api/users")
api.add_resource(PerksManager, "/api/perks")
api.add_resource(ClientsManager, "/api/clients")
api.add_resource(PartnerManager, "/api/partners")

