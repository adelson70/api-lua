from flask import Flask
from app.config import Config

from app.routes.lua.routes import lua_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(lua_bp, url_prefix='/lua')

    return app