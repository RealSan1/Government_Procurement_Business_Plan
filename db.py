import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],  # Render 환경 변수에서 가져옴
        cursor_factory=RealDictCursor
    )
