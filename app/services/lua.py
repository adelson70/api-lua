from datetime import datetime

from app.utils.datetime import get_data_atual

# utils
from app.utils.scrapper import get_fase_lua_hoje_web

def get_fase_lua_hoje():
    try:
        data_atual = get_data_atual()
        fases_ano = get_fase_lua_hoje_web(data_atual)

        if not fases_ano:
            return None

        dia, mes, ano = data_atual.split('/')
        chave_mes = str(int(mes))
        chave_dia = str(int(dia))

        fase_do_dia = fases_ano.get(chave_mes, {}).get(chave_dia)

        resposta = {
            'dia': int(dia),
            'mes': int(mes),
            'ano': int(ano),
            'fase': fase_do_dia,
            'timestamp': datetime.now().isoformat(),
        }

        if fase_do_dia is None:
            resposta['detalhes'] = fases_ano

        return resposta

    except Exception as e:
        print(f"Erro ao obter a fase da lua hoje: {e}")
        return None
