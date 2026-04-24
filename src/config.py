import os
from datetime import timezone, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path(__file__).parent.parent

# Finam API credentials
FINAM_API_KEY = os.getenv("FINAM_API_KEY")
FINAM_ACCOUNT_ID = os.getenv("FINAM_ACCOUNT_ID")

# Finam Arena API credentials
FINAM_ARENA_URL = "http://localhost:8000/v1"
FINAM_ARENA_API_KEY = os.getenv("FINAM_ARENA_API_KEY")
FINAM_ARENA_ACCOUNT_ID = os.getenv("FINAM_ARENA_ACCOUNT_ID")

# Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Moscow timezone (UTC+3)
MOSCOW_TZ = timezone(timedelta(hours=3))

# Agent
PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")
BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

STOCKS = {
    "ALRS@MISX": "АЛРОСА ао",
    "AFLT@MISX": "Аэрофлот",
    "GAZP@MISX": "ГАЗПРОМ ао",
    "SBER@MISX": "Сбербанк",
    "YDEX@MISX": "ЯНДЕКС",
    "MTSS@MISX": "МТС-ао",
    "X5@MISX": "КЦ ИКС 5",
    "FEES@MISX": "Россети",
    "SMLT@MISX": "Самолет ао",
    "FESH@MISX": "ДВМП ао",
}
