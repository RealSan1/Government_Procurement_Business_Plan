from db import get_conn

conn = get_conn()
def fetch_jobs():
    """
    진행중인 채용공고 + 직무 정보 반환
    """
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT 
                    c.공고ID,
                    c.제목,
                    c.기관명,
                    c.고용형태,                    
                    j.직무명,
                    c.근무지,
                    c.채용구분,
                    c.원문URL,
                    DATE_FORMAT(c.공고마감일, '%Y-%m-%d') AS 공고마감일
                FROM 채용공고 c
                JOIN 채용_직무 cj ON c.공고ID = cj.공고ID
                JOIN 직무 j ON cj.직무ID = j.직무ID
                WHERE c.상태 = '진행중'
                ORDER BY c.공고마감일 ASC;
            """
            cur.execute(sql)
            rows = cur.fetchall()
        return rows
    except Exception as e:
        raise e
