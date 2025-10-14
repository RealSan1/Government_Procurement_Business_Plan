import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# 개발 환경이면 .env 파일 로드
if os.path.exists(".env"):
    load_dotenv(".env")

DB_USER = os.environ.get("DATABASE_USER", "")
DB_PASS = os.environ.get("DATABASE_PASSWORD", "")
DB_HOST = os.environ.get("DATABASE_HOST", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=3306,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True
    )
