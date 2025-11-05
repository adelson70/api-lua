import requests
from bs4 import BeautifulSoup
from app.config import Config
from datetime import datetime

def get_fase_lua_hoje():
    try:
        url = Config.BASE_URL
        response = requests.get(url, headers={"User-Agent": Config.USER_AGENT})
        
        print(response.text)
        
        return True

    except Exception as e:
        print(f"Erro ao obter a fase da lua hoje: {e}")
        return None
