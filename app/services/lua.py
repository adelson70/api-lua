import requests
from app.config import Config

# services
from app.utils.datetime import get_data_atual

# utils
from app.utils.scrapper import get_fase_lua_hoje_web

def get_fase_lua_hoje():
    try:
        data_atual = get_data_atual()
        fase_lua_hoje = get_fase_lua_hoje_web(data_atual)

        print('Fase da lua hoje: ', data_atual)
        print('Fase da lua hoje: ', fase_lua_hoje)
        
        return data_atual

    except Exception as e:
        print(f"Erro ao obter a fase da lua hoje: {e}")
        return None
