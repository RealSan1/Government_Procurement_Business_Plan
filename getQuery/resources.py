from db import get_conn

# 1. 목록 조회
def resources_list_data():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 번호, 제목, 카테고리, 작성일시, 공지여부
                FROM 자료실게시글 
                WHERE 1=1
                ORDER BY 공지여부 DESC, 작성일시 DESC
            """)
            return cur.fetchall()
    finally:
        conn.close()

# 2. 상세 조회
def get_resource_detail(post_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM 자료실게시글 WHERE 번호 = %s", (post_id,))
            return cur.fetchone()
    finally:
        conn.close()

# 3. 글 작성 처리
def create_resource(제목: str, 내용: str | None, 카테고리: str, 공지여부: bool = False):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO 자료실게시글 (제목, 내용, 카테고리, 공지여부)
                VALUES (%s, %s, %s, %s)
            """, (제목, 내용 or None, 카테고리, 공지여부))
        conn.commit()
    finally:
        conn.close()