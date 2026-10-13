
import os
from pathlib import Path
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).resolve().parent
ENV_FILE = CONFIG_DIR / "cren.env"

load_dotenv(ENV_FILE, override=True)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "Car2Insights")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

print(DB_PASSWORD)
if not DB_PASSWORD:
    raise ValueError(
        f"DB_PASSWORD is empty. Check this file: {ENV_FILE}"
    )
