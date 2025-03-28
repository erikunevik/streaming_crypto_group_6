import os
from dotenv import load_dotenv

load_dotenv()

EXCHANGERATEAPI_KEY = os.getenv("CURRENCY_KEY")

COINMARKET_API = os.getenv("API_KEY")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")