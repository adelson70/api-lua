from datetime import datetime

from app.utils.datetime import get_data_atual, get_ano_atual, get_mes_atual
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


def _coletar_ano(ano):
    if ano is None:
        try:
            return int(get_ano_atual())
        except (TypeError, ValueError):
            return None

    try:
        return int(ano)
    except (TypeError, ValueError):
        return None


def _coletar_mes(mes):
    if mes is None:
        try:
            return int(get_mes_atual())
        except (TypeError, ValueError):
            return None

    try:
        mes_int = int(mes)
    except (TypeError, ValueError):
        return None

    if 1 <= mes_int <= 12:
        return mes_int

    return None


def _montar_resposta_mes(ano: int, mes: int, fases_por_dia: dict):
    return {
        "ano": ano,
        "mes": mes,
        "nome_mes": MESES_POR_NUMERO.get(mes, str(mes)),
        "fases": _normalizar_dias(fases_por_dia),
    }


def get_fases_lua_ano(ano=None):
    try:
        ano_int = _coletar_ano(ano)

        if ano_int is None:
            return None

        fases_por_mes = verificar_fases_ano(ano_int)

        if not fases_por_mes:
            return None

        meses_nomeados = {}

        for mes_numero, fases_por_dia in sorted(
            fases_por_mes.items(), key=lambda item: int(item[0])
        ):
            try:
                indice_mes = int(mes_numero)
            except (TypeError, ValueError):
                indice_mes = None

            nome_mes = MESES_POR_NUMERO.get(indice_mes, str(mes_numero))
            meses_nomeados[nome_mes] = _normalizar_dias(fases_por_dia)

        return {
            "ano": ano_int,
            "meses": meses_nomeados,
        }

    except Exception as e:
        print(f"Erro ao obter as fases da lua: {e}")
        return None


def get_fases_lua_mes(mes=None, ano=None):
    try:
        mes_int = _coletar_mes(mes)
        ano_int = _coletar_ano(ano)

        if mes_int is None or ano_int is None:
            return None

        fases_por_mes = verificar_fases_ano(ano_int)

        if not fases_por_mes:
            return None

        fases_por_dia = fases_por_mes.get(str(mes_int))

        if not fases_por_dia:
            return None

        return _montar_resposta_mes(ano_int, mes_int, fases_por_dia)

    except Exception as e:
        print(f"Erro ao obter as fases da lua do mes: {e}")
        return None

