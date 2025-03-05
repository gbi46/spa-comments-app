import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

MYSQL_ROOT_PASSWORD=os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE=os.getenv('MYSQL_DATABASE')
MYSQL_USER=os.getenv('MYSQL_USER')
MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
