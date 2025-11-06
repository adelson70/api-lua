from flask import Flask
from flasgger import Swagger
from app.config import Config

# importando as rotas
from app.routes.lua.routes import lua_bp

# importando os middlewares
from app.middleware.auth import auth_middleware

# impoertando configs do swagger
from app.swagger.swagger import swagger_config

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(Config)

    # registra as rotas
    app.register_blueprint(lua_bp, url_prefix='/lua')

    # registra os middlewares
    auth_middleware(app)

    # configura o swagger
    Swagger(app, config=swagger_config)

    return app