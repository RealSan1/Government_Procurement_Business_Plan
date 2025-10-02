from db import get_conn

def fetch_jobs():
    """
    진행중인 채용공고 + 직무 정보 반환 (PostgreSQL 버전)
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT 
                    c.공고id,
                    c.제목,
                    c.기관명,
                    c.고용형태,
                    j.직무명,
                    c.근무지,
                    c.채용구분,
                    c.원문url,
                    TO_CHAR(c.공고마감일, 'YYYY-MM-DD') AS 공고마감일
                FROM 채용공고 c
                JOIN 채용_직무 cj ON c.공고id = cj.공고id
                JOIN 직무 j ON cj.직무id = j.직무id
                WHERE c.상태 = '진행중'
                ORDER BY c.공고마감일 ASC;
            """
            cur.execute(sql)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()
