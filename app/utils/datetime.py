from datetime import datetime

def get_data_atual():
    return datetime.now().strftime("%d/%m/%Y")

def get_ano_atual():
    return datetime.now().strftime("%Y")

def get_mes_atual():
    return datetime.now().strftime("%m")