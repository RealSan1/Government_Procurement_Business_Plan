from db import get_conn


def search_majors(keyword: str, limit: int = 20):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 학과상세ID, 학과명, 학과소개, 적성흥미
                FROM 학과상세정보
                WHERE 학과명 LIKE %s
                LIMIT %s
            """, (f"%{keyword}%", limit))
            return cur.fetchall()
    finally:
        conn.close()


def get_major_detail_full(major_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 학과상세ID, 학과명, 학과소개, 적성흥미
                FROM 학과상세정보
                WHERE 학과상세ID=%s
            """, (major_id,))
            info = cur.fetchone()
            if not info:
                return None

            cur.execute("""
                SELECT 교과목 FROM 학과상세_주요교과목
                WHERE 학과상세ID=%s
            """, (major_id,))
            subjects = [row['교과목'] for row in cur.fetchall()]

            cur.execute("""
                SELECT 관련학과명 FROM 학과상세_관련학과
                WHERE 학과상세ID=%s
            """, (major_id,))
            related_majors = [row['관련학과명'] for row in cur.fetchall()]

            cur.execute("""
                SELECT 관련직업명 FROM 학과상세_관련직업
                WHERE 학과상세ID=%s
            """, (major_id,))
            related_jobs = [row['관련직업명'] for row in cur.fetchall()]

        return {
            "info": info,
            "subjects": subjects,
            "related_majors": related_majors,
            "related_jobs": related_jobs
        }
    finally:
        conn.close()
