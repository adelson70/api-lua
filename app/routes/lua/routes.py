from flask import Blueprint, request
from app.services.lua import get_fase_lua_hoje, get_fases_lua_ano, get_fases_lua_mes
from app.utils.response_formatter import make_response
from flasgger import swag_from

lua_bp = Blueprint('lua', __name__)

@lua_bp.route('/hoje', methods=['GET'])
@swag_from('specs/lua-hoje.yml')
def fase_lua_hoje():
    fase_lua = get_fase_lua_hoje()
    return make_response(data=fase_lua, message="Fase da lua hoje obtida com sucesso")

@lua_bp.route('/mes', methods=['GET'])
@swag_from('specs/lua-fases-mes.yml')
def fases_lua_mes():
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)

    fases_lua = get_fases_lua_mes(mes=mes, ano=ano)

    if fases_lua is None:
        return make_response(
            data=None,
            message="Fases da lua do mês não encontradas para os parâmetros informados",
            status="error",
            code=404,
        )

    return make_response(
        data=fases_lua,
        message="Fases da lua do mês obtidas com sucesso",
    )

@lua_bp.route('/ano', methods=['GET'])
@swag_from('specs/lua-fases-ano.yml')
def fases_lua_ano():
    ano = request.args.get('ano', type=int)

    fases_lua = get_fases_lua_ano(ano=ano)

    if fases_lua is None:
        return make_response(
            data=None,
            message="Fases da lua do ano não encontradas",
            status="error",
            code=404,
        )

    return make_response(
        data=fases_lua,
        message="Fases da lua do ano obtidas com sucesso",
    )