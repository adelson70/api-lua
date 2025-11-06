import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')


def _get_json_path(ano: str) -> str:
    return os.path.join(DATA_DIR, f'{ano}.json')


def salvar_fases_ano(ano: str, fases_por_mes: dict) -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)

    json_path = _get_json_path(ano)

    with open(json_path, 'w', encoding='utf-8') as arquivo:
        json.dump(fases_por_mes, arquivo, ensure_ascii=False, indent=2)

    return fases_por_mes


def _carregar_fases_local(ano: str):
    json_path = _get_json_path(ano)

    if not os.path.exists(json_path):
        return None

    with open(json_path, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


def _normalizar_ano(referencia):
    if referencia is None:
        return None

    if isinstance(referencia, int):
        return str(referencia)

    texto = str(referencia).strip()

    if not texto:
        return None

    if '/' in texto:
        texto = texto.split('/')[-1]

    try:
        return str(int(texto))
    except (TypeError, ValueError):
        return None


def verificar_fases_ano(referencia):
    ano = _normalizar_ano(referencia)

    if ano is None:
        return None

    try:
        fases_locais = _carregar_fases_local(ano)

        if fases_locais:
            return fases_locais

        from app.utils.scrapper import scrape_fases_ano

        fases_por_mes = scrape_fases_ano(ano)

        if fases_por_mes:
            return salvar_fases_ano(ano, fases_por_mes)

        return None

    except Exception as e:
        print(f"Erro ao verificar as fases do ano: {e}")
        return None