from db import get_conn
def companyInfo():
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT 기업명, 사업자등록번호, 업종명_상, 대표자, 지역명
                FROM 강소기업
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()