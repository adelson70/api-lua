import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')


def verificar_fases_ano(data_atual):
    json_path = os.path.join(DATA_DIR, f'{data_atual.split("/")[2]}.json')
    
    try:
        if not os.path.exists(json_path):
            print(f"Arquivo {json_path} não encontrado")
            return False
        
        with open(json_path, 'r') as file:
            print('Arquivo carregado com sucesso')
            return json.load(file)
        
    except Exception as e:
        print(f"Erro ao verificar as fases do ano: {e}")
        return None