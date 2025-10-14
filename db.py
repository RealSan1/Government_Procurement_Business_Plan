import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# 개발 시
# load_dotenv("apikey.env")
# DB_USER = os.getenv("DATABASE_USER")
# DB_PASS = os.getenv("DATABASE_PASSWORD")
# DB_HOST = os.getenv("DATABASE_URL")
# DB_NAME = os.getenv("DATABASE_NAME")

# 배포 시 (기본값 설정)
DB_USER = os.environ.get("DATABASE_USER", "root")
DB_PASS = os.environ.get("DATABASE_PASSWORD", "")
DB_HOST = os.environ.get("DATABASE_URL", "localhost")
DB_NAME = os.environ.get("DATABASE_NAME", "welfare")


def get_conn():
    """MySQL 데이터베이스 연결"""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True
    )
