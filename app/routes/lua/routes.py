from flask import Blueprint
from app.services.lua import get_fase_lua_hoje, get_fases_lua_ano
from app.utils.response_formatter import make_response
from flasgger import swag_from

lua_bp = Blueprint('lua', __name__)

@lua_bp.route('/hoje', methods=['GET'])
@swag_from('specs/lua-hoje.yml')
def fase_lua_hoje():
    fase_lua = get_fase_lua_hoje()
    return make_response(data=fase_lua, message="Fase da lua hoje obtida com sucesso")

@lua_bp.route('/fases', methods=['GET'])
@swag_from('specs/lua-fases-ano.yml')
def fases_lua_ano():
    fases_lua = get_fases_lua_ano()
    return make_response(data=fases_lua, message="Fases da lua do ano obtidas com sucesso")