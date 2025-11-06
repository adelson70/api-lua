from datetime import datetime

from app.utils.datetime import get_data_atual, get_ano_atual
from app.utils.fase_local import verificar_fases_ano

# utils
from app.utils.scrapper import get_fase_lua_hoje_web

MESES_POR_NUMERO = {
    1: "janeiro",
    2: "fevereiro",
    3: "marco",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}

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

def _normalizar_dias(fases_por_dia: dict) -> dict:
    try:
        dias_ordenados = sorted(
            ((str(int(dia)), fase) for dia, fase in fases_por_dia.items()),
            key=lambda item: int(item[0]),
        )
        return {dia: fase for dia, fase in dias_ordenados}
    except Exception:
        return fases_por_dia


def get_fases_lua_ano():
    try:
        data_atual = get_data_atual()
        ano_atual = int(get_ano_atual())

        fases_por_mes = verificar_fases_ano(data_atual)

        if not fases_por_mes:
            return None

        meses_nomeados = {}

        for mes_numero, fases_por_dia in fases_por_mes.items():
            try:
                indice_mes = int(mes_numero)
            except (TypeError, ValueError):
                indice_mes = None

            nome_mes = MESES_POR_NUMERO.get(indice_mes, str(mes_numero))
            meses_nomeados[nome_mes] = _normalizar_dias(fases_por_dia)

        return {
            "ano": ano_atual,
            "meses": meses_nomeados,
        }

    except Exception as e:
        print(f"Erro ao obter as fases da lua: {e}")
        return None