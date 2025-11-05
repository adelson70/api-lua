import os

class Config:
    BASE_URL = os.getenv('BASE_URL', "https://portal.inmet.gov.br/paginas/luas")
    USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (compatible; ModularScraper/1.0)")
