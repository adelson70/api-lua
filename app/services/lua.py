import requests
from app.config import Config

from app.utils.datetime import get_data_atual

def get_fase_lua_hoje():
    try:
        url = Config.BASE_URL
        data_atual = get_data_atual()
        response = requests.get(url, headers={"User-Agent": Config.USER_AGENT})

        print('Fase da lua hoje: ', data_atual)
        
        return True

    except Exception as e:
        print(f"Erro ao obter a fase da lua hoje: {e}")
        return None
