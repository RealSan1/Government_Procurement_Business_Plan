import os
import pymysql
from pymysql.cursors import DictCursor

# 개발 시
# load_dotenv("apikey.env")
# DB_USER = os.getenv("DATABASE_USER")
# DB_PASS = os.getenv("DATABASE_PASSWORD")
# DB_HOST = os.getenv("DATABASE_HOST")
# DB_NAME = os.getenv("DATABASE_NAME")

# 배포 시 (기본값 설정)

for var in ["DATABASE_USER", "DATABASE_PASSWORD", "DATABASE_HOST", "DATABASE_NAME"]:
    value = os.environ.get(var)
    if value:
        print(f"{var} is set ✅")
    else:
        print(f"{var} is NOT set ❌")

        
DB_USER = os.environ.get("DATABASE_USER", "")
DB_PASS = os.environ.get("DATABASE_PASSWORD", "")
DB_HOST = os.environ.get("DATABASE_HOST", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")

def get_conn():
    """MySQL 데이터베이스 연결"""
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
