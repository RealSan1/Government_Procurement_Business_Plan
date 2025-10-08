import os
import psycopg2
from psycopg2.extras import RealDictCursor

# render 배포시
def get_conn():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        cursor_factory=RealDictCursor
    )


# import os
# from dotenv import load_dotenv
# import psycopg2
# from psycopg2.extras import RealDictCursor

# # db.env 파일 로드
# load_dotenv(dotenv_path="apikey.env") 

# def get_conn():
#     return psycopg2.connect(
#         os.getenv("DATABASE_URL"), 
#         cursor_factory=RealDictCursor
#     )
