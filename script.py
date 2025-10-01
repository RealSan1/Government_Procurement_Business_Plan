import csv
import pymysql

from datetime import datetime

def to_date(s):
    return datetime.strptime(s.strip(), "%Y.%m.%d").date()


# DB 연결
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="rootpw",
    db="jobplus",
    charset="utf8mb4"
)
cur = conn.cursor()

def insert_job(job_name):
    """직무 삽입 (중복 방지)"""
    cur.execute("INSERT IGNORE INTO 직무 (직무명) VALUES (%s)", (job_name,))
    conn.commit()
    cur.execute("SELECT 직무ID FROM 직무 WHERE 직무명=%s", (job_name,))
    return cur.fetchone()[0]

def insert_recruit(row):
    from datetime import datetime
    
    def to_date(s):
        return datetime.strptime(s.strip(), "%Y.%m.%d").date()

    start_date = to_date(row["공고기간"].split("~")[0])
    end_date = to_date(row["공고기간"].split("~")[1])

    people = row["채용인원"].replace("명", "").strip()
    people = int(people) if people.isdigit() else 0

    cur.execute("""
        INSERT INTO 채용공고 
        (제목, 기관명, 고용형태, 대체인력여부, 채용구분, 공고시작일, 공고마감일, 학력정보,
         근무지, 채용인원, 원문URL, 등록일, 상태)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row["제목"], row["기관명"], row["고용형태"], row["대체인력여부"], row["채용구분"],
        start_date, end_date,
        row["학력정보"], row["근무지"], people,
        row["원문URL"], to_date(row["등록일"]), row["상태"]
    ))
    conn.commit()
    return cur.lastrowid


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
            for job in set(jobs):  # 중복 제거
                직무ID = insert_job(job)
                cur.execute("INSERT IGNORE INTO 채용_직무 (공고ID, 직무ID) VALUES (%s,%s)", (공고ID, 직무ID))
                conn.commit()

# 실행 https://www.alio.go.kr/information/informationRecruitList.do
process_csv("채용공고목록_2025-09-19.csv")
conn.close()
