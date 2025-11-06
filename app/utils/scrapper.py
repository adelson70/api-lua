from bs4 import BeautifulSoup
from requests import get
from app.config import Config
from app.utils.fase_local import verificar_fases_ano

def get_fase_lua_hoje_web(data_atual):
    try:
        # primeiro verifica se as fases foram baixadas e estão locais na maquina
        fases_ano = verificar_fases_ano(data_atual)
        
        if fases_ano:
            return fases_ano
        
        url = Config.BASE_URL
        html_content = get(url)

        # pegando tabela das fases da lua
        soup = BeautifulSoup(html_content.text, 'html.parser')
        table = soup.find('table')
        print('Table: ', table)

        # pegando fases
        fases = [fase.text for fase in table.find_all('th')]
        print('Fases: ', fases)
        
        # print('Response: ', response.text)
        return html_content

    except Exception as e:
        print(f"Erro ao obter a fase da lua hoje: {e}")
        return None