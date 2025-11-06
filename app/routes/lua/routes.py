from flask import Blueprint, jsonify
from app.services.lua import get_fase_lua_hoje
from app.utils.response_formatter import make_response

lua_bp = Blueprint('lua', __name__)

@lua_bp.route('/hoje', methods=['GET'])
def fase_lua_hoje():
    fase_lua = get_fase_lua_hoje()
    return make_response(data=fase_lua, message="Fase da lua hoje obtida com sucesso")





