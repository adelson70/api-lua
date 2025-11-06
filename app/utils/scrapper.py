from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from requests import get

from app.config import Config

_MAPA_MESES = {
    'Jan': 1,
    'Fev': 2,
    'Mar': 3,
    'Abr': 4,
    'Mai': 5,
    'Jun': 6,
    'Jul': 7,
    'Ago': 8,
    'Set': 9,
    'Out': 10,
    'Nov': 11,
    'Dez': 12,
}


def _normalizar_espacos(texto: str) -> str:
    return ' '.join(texto.split())


def _extrair_evento(texto_data: str):
    try:
        partes = [p.strip() for p in texto_data.split('-') if p.strip()]

        if len(partes) < 2:
            return None

        parte_data = _normalizar_espacos(partes[0])
        hora_e_minuto = partes[1]

        dados_data = parte_data.split(' ')

        if len(dados_data) < 3:
            return None

        dia = int(dados_data[0])
        mes_nome = dados_data[1]
        ano = int(dados_data[2])

        if mes_nome not in _MAPA_MESES:
            return None

        hora_min = hora_e_minuto.split(':')

        if len(hora_min) < 2:
            return None

        hora = int(hora_min[0])
        minuto = int(hora_min[1])

        mes_numero = _MAPA_MESES[mes_nome]
        instante = datetime(ano, mes_numero, dia, hora, minuto)

        return {
            'dia': str(dia),
            'mes': str(mes_numero),
            'ano': str(ano),
            'instante': instante,
        }
    except Exception:
        return None


def _expandir_fases_por_dia(eventos: list, ano: int) -> dict:
    if not eventos:
        return {}

    eventos_ordenados = sorted(eventos, key=lambda item: item['instante'])
    fases_por_mes: dict[str, dict[str, str]] = {}

    data_inicio = datetime(ano, 1, 1).date()
    data_fim = datetime(ano, 12, 31).date()

    indice_evento = 0
    fase_corrente = eventos_ordenados[0]['fase']

    data_cursor = data_inicio

    while data_cursor <= data_fim:
        while indice_evento < len(eventos_ordenados) and eventos_ordenados[indice_evento]['instante'].date() <= data_cursor:
            fase_corrente = eventos_ordenados[indice_evento]['fase']
            indice_evento += 1

        if fase_corrente:
            chave_mes = str(data_cursor.month)
            chave_dia = str(data_cursor.day)
            fases_por_mes.setdefault(chave_mes, {})[chave_dia] = fase_corrente

        data_cursor += timedelta(days=1)

    return fases_por_mes


def scrape_fases_ano(ano: str):
    try:
        resposta = get(Config.BASE_URL, timeout=15)
        resposta.raise_for_status()
    except Exception as exc:
        print(f"Erro ao baixar fases da lua: {exc}")
        return None

    soup = BeautifulSoup(resposta.text, 'html.parser')
    tabela = soup.find('table')

    if tabela is None:
        print('Tabela de fases da lua não encontrada na página.')
        return None

    cabecalhos = [th.get_text(strip=True) for th in tabela.find_all('th')]

    fases_por_mes = {}

    eventos = []

    for linha in tabela.find_all('tr'):
        colunas = linha.find_all('td')

        if len(colunas) != len(cabecalhos):
            continue

        for indice, coluna in enumerate(colunas):
            texto_data = coluna.get_text(strip=True)

            if texto_data == '--':
                continue

            info_data = _extrair_evento(texto_data)

            if not info_data or info_data['ano'] != ano:
                continue

            fase = cabecalhos[indice]
            eventos.append({
                'instante': info_data['instante'],
                'fase': fase,
            })

    fases_por_mes = _expandir_fases_por_dia(eventos, int(ano))

    if not fases_por_mes:
        print(f'Nenhum dado de fases da lua encontrado para o ano {ano}.')
        return None

    return fases_por_mes


def get_fase_lua_hoje_web(data_atual: str):
    try:
        from app.utils.fase_local import verificar_fases_ano

        return verificar_fases_ano(data_atual)
    except Exception as e:
        print(f"Erro ao obter a fase da lua hoje: {e}")
        return None