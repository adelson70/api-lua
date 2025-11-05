from flask import Blueprint, jsonify
from app.services.lua import get_fase_lua_hoje

lua_bp = Blueprint('lua', __name__)

@lua_bp.route('/hoje', methods=['GET'])
def fase_lua_hoje():
    fase_lua = get_fase_lua_hoje()
    return jsonify({"fase_lua": fase_lua})





