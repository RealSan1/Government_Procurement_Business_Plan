import csv
import db
from datetime import datetime

# DB 연결
conn = db.get_conn()
cur = conn.cursor()

def to_date(s):
    return datetime.strptime(s.strip(), "%Y.%m.%d").date()

def insert_job(job_name):
    """직무 삽입 (중복 방지, PostgreSQL 방식)"""
    cur.execute("""
        INSERT INTO 직무 (직무명) VALUES (%s)
        ON CONFLICT (직무명) DO NOTHING
        RETURNING 직무id;
    """, (job_name,))
    result = cur.fetchone()
    if result:
        직무ID = result["직무id"]
    else:
        cur.execute("SELECT 직무id FROM 직무 WHERE 직무명=%s", (job_name,))
        직무ID = cur.fetchone()["직무id"]
    conn.commit()
    return 직무ID

def insert_recruit(row):
    start_date = to_date(row["공고기간"].split("~")[0])
    end_date = to_date(row["공고기간"].split("~")[1])

    people = row["채용인원"].replace("명", "").strip()
    people = int(people) if people.isdigit() else 0

    cur.execute("""
        INSERT INTO 채용공고
        (제목, 기관명, 고용형태, 대체인력여부, 채용구분, 공고시작일, 공고마감일, 학력정보,
         근무지, 채용인원, 원문url, 등록일, 상태)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING 공고id;
    """, (
        row["제목"], row["기관명"], row["고용형태"], row["대체인력여부"], row["채용구분"],
        start_date, end_date,
        row["학력정보"], row["근무지"], people,
        row["원문URL"], to_date(row["등록일"]), row["상태"]
    ))
    공고ID = cur.fetchone()["공고id"]
    conn.commit()
    return 공고ID

def process_csv(file_path):
    with open(file_path, "r", encoding="cp949") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            # 채용공고 삽입
            공고ID = insert_recruit(row)

            # 직무 분리 ('.' '/' 기준)
            jobs = []
            for token in row["표준직무(NCS)"].replace("/", ".").split("."):
                token = token.strip()
                if token:
                    jobs.append(token)

            # 직무 삽입 및 매핑
            for job in set(jobs):
                직무ID = insert_job(job)
                cur.execute("""
                    INSERT INTO 채용_직무 (공고id, 직무id)
                    VALUES (%s,%s)
                    ON CONFLICT DO NOTHING;
                """, (공고ID, 직무ID))
                conn.commit()

# 실행
process_csv("채용공고목록_2025-09-19.csv")
conn.close()
