from db import get_conn
from typing import List, Dict


def apply_consult(학번, 상담유형, 상담사id, 메모=None):
    if 상담사id == "undefined":
        상담사id = None
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO 상담신청 (학번, 상담유형, 상담사id, 메모)
                VALUES (%s, %s, %s, %s)
            """, (학번, 상담유형, 상담사id, 메모))
        conn.commit()
    finally:
        conn.close()


def get_consultants() -> List[Dict]:
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT 상담사id, 이름 FROM 상담사')
            return cur.fetchall()
    finally:
        conn.close()


def fetch_user_consults(학번: str) -> List[Dict]:
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT c.학번, s.이름 AS 상담사명, c.상담유형, c.신청일시, 
                       c.메모, c.상태, c.처리시간
                FROM 상담신청 c
                JOIN 상담사 s ON c.상담사id = s.상담사id
                WHERE c.학번 = %s
                ORDER BY c.신청일시 DESC
            """
            cur.execute(sql, (학번,))
            return cur.fetchall()
    finally:
        conn.close()


def get_student_consults(학번):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM 상담신청 WHERE 학번=%s", (학번,))
            return cur.fetchall()
    finally:
        conn.close()


def assign_consult(상담id, 상담사id, 상담일시=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE 상담신청
                SET 상태='승인', 상담사id=%s, 상담일시=%s
                WHERE 상담신청id=%s
            """, (상담사id, 상담일시, 상담id))
        conn.commit()
    finally:
        conn.close()


def fetch_consults() -> List[Dict]:
    """상담 신청 목록 조회"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT 상담신청id, 학번, 상태, 상담유형, 메모, 신청일시
                FROM 상담신청
                WHERE 상태 = '신청'
            """
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()


def update_consult_status(consult_id: int, status: str):
    """상담 상태 변경"""
    conn = get_conn()
    try:
        if status == 'success':
            num = '승인'
        else:
            num = '거절'
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE 상담신청 SET 상태=%s WHERE 상담신청id=%s',
                (num, consult_id)
            )
            conn.commit()
    finally:
        conn.close()


def assign_consultant(consult_id: int, consultant_id: int):
    """상담자 배정"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE 상담신청 SET 상담사id=%s WHERE 상담신청id=%s',
                (consultant_id, consult_id)
            )
            conn.commit()
    finally:
        conn.close()
