
from sanic import Sanic
from sanic_restful import Api

from ..routes.default import Api1, Api2, Api3, Api4, Api5
from ..routes.auth import SignUp, SignIn, RefreshToken


def init_app():
    app = Sanic(__name__)
    api = Api(app)
    api.add_resource(SignUp, '/signup')
    api.add_resource(SignIn, '/signin')
    api.add_resource(RefreshToken, '/refreshtoken')
    api.add_resource(Api1, '/api1')
    api.add_resource(Api2, '/api2')
    api.add_resource(Api3, '/api3')
    api.add_resource(Api4, '/api4')
    api.add_resource(Api5, '/api5')
    return app


def start_app():
    app = init_app()
    app.run(debug=True)
