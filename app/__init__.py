from flask import Flask
from app.config import Config

from app.routes.lua.routes import lua_bp

from app.middleware.auth import auth_middleware

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(Config)

    # registra as rotas
    app.register_blueprint(lua_bp, url_prefix='/lua')

    # registra os middlewares
    auth_middleware(app)

    return app