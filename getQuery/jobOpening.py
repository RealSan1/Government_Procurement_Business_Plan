from db import get_conn
from datetime import datetime
from psycopg2.extras import RealDictCursor

def fetch_jobs_ex():
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

def fetch_jobs_in():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 공고ID, 제목, 회사명, 표준직무, 고용형태, 대체인력여부,
                       채용구분, 공고기간, 학력정보, 근무지, 채용인원, 회사URL, 승인여부
                FROM 내부_채용공고
                WHERE 승인여부='승인'
                ORDER BY 등록일시 DESC
            """)
            return cur.fetchall()
    finally:
        conn.close()

def insert_job(
    title: str,
    company: str,
    job_categories: str,
    employment_type: str,
    substitute: str,
    recruit_type: str,
    period: str,
    education: str,
    location: str,
    num_recruits: str,
    url: str
):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO 내부_채용공고
                (제목, 회사명, 표준직무, 고용형태, 대체인력여부, 채용구분,
                공고기간, 학력정보, 근무지, 채용인원, 회사URL, 승인여부)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                title, company, job_categories, employment_type, substitute, recruit_type,
                period, education, location, num_recruits, url, '대기'  # 승인 전 '대기'
            ))
        conn.commit()
    finally:
        conn.close()

def update_job_status(job_id: int, status: str):
    """
    공고 승인/거절 처리
    status: '승인' or '거절'
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE 내부_채용공고
                SET 승인여부 = %s
                WHERE 공고ID = %s
            """, (status, job_id))
        conn.commit()
    finally:
        conn.close()

def fetch_pending_jobs():
    """
    검수 대기 공고 조회
    """
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM 내부_채용공고 WHERE 승인여부 = '대기' ORDER BY 등록일시 DESC")
            return cur.fetchall()
    finally:
        conn.close()

