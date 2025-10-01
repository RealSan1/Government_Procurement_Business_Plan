import requests
import xml.etree.ElementTree as ET
import db, os
from dotenv import load_dotenv

load_dotenv("apikey.env")
conn = db.get_conn()

API_KEY = os.getenv("학과API")

MAJOR_LIST_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo213L01.do"
MAJOR_DETAIL_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo213D01.do"

try:
    with conn.cursor() as cur:
        # 1️⃣ 학과 목록 가져오기
        params = {
            "authKey": API_KEY,
            "returnType": "XML",
            "target": "MAJORCD",
            "srchType": "A"
        }
        res = requests.get(MAJOR_LIST_URL, params=params)
        res.encoding = "utf-8"
        root = ET.fromstring(res.text)

        majors = []
        for item in root.findall(".//majorList"):
            majors.append({
                "학과구분코드": item.findtext("majorGb"),
                "계열ID": item.findtext("empCurtState1Id"),
                "학과ID": item.findtext("empCurtState2Id"),
                "학과명": item.findtext("knowSchDptNm"),
                "세부학과명": item.findtext("knowDtlSchDptNm")
            })

        print(f"총 {len(majors)}개 학과 목록 불러옴.")

        # 2️⃣ 학과별 상세정보 호출
        for major in majors:
            detail_params = {
                "authKey": API_KEY,
                "returnType": "XML",
                "target": "MAJORDTL",
                "majorGb": major["학과구분코드"],
                "empCurtState1Id": major["계열ID"],
                "empCurtState2Id": major["학과ID"]
            }

            response = requests.get(MAJOR_DETAIL_URL, params=detail_params)
            response.encoding = "utf-8"
            root = ET.fromstring(response.text)

            majorSum = root
            if majorSum is None:
                print(f"❌ 상세 없음 → {major['학과명']} ({major['학과ID']})")
                continue

            # ✅ API 반환값의 ID 사용
            계열ID = majorSum.findtext("knowDptId")
            학과ID = majorSum.findtext("knowSchDptId")

            # 학과상세정보 저장
            cur.execute("""
                INSERT IGNORE INTO 학과상세정보
                (계열ID, 학과ID, 계열명, 학과명, 학과소개, 적성흥미)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                계열ID,
                학과ID,
                majorSum.findtext("knowDptNm"),
                majorSum.findtext("knowSchDptNm"),
                majorSum.findtext("schDptIntroSum"),
                majorSum.findtext("aptdIntrstCont")
            ))

            # 학과상세ID 정확히 가져오기
            cur.execute("""
                SELECT 학과상세ID FROM 학과상세정보 
                WHERE 계열ID=%s AND 학과ID=%s
            """, (계열ID, 학과ID))
            row = cur.fetchone()
            if not row:
                print(f"⚠️ 학과상세ID 조회 실패: {majorSum.findtext('knowSchDptNm')} ({학과ID})")
                continue
            학과상세ID = row["학과상세ID"]
            print(학과상세ID)

            # 관련학과
            for rel in majorSum.findall(".//relSchDptList/knowDtlSchDptNm"):
                cur.execute("INSERT IGNORE INTO 학과상세_관련학과 (학과상세ID, 관련학과명) VALUES (%s,%s)",
                            (학과상세ID, rel.text))

            # 주요교과목
            for subj in majorSum.findall(".//mainSubjectList/mainEdusbjCont"):
                cur.execute("INSERT IGNORE INTO 학과상세_주요교과목 (학과상세ID, 교과목) VALUES (%s,%s)",
                            (학과상세ID, subj.text))

            # 개설대학
            for univ in majorSum.findall(".//schDptList"):
                cur.execute("""
                    INSERT IGNORE INTO 학과상세_개설대학 (학과상세ID, 대학교구분, 대학교명, 대학URL)
                    VALUES (%s,%s,%s,%s)
                """, (
                    학과상세ID,
                    univ.findtext("univGbnNm"),
                    univ.findtext("univNm"),
                    univ.findtext("univUrl")
                ))

            # 관련직업
            for job in majorSum.findall(".//relAdvanJobsList/knowJobNm"):
                cur.execute("INSERT IGNORE INTO 학과상세_관련직업 (학과상세ID, 관련직업명) VALUES (%s,%s)",
                            (학과상세ID, job.text))

            # 모집현황
            for recr in majorSum.findall(".//recrStateList"):
                cur.execute("""
                    INSERT IGNORE INTO 학과상세_모집현황
                    (학과상세ID, 입학정원, 지원자수, 졸업인원, 대학교구분, 연도)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """, (
                    학과상세ID,
                    recr.findtext("enscMxnp"),
                    recr.findtext("enscSpnb"),
                    recr.findtext("grdnNmpr"),
                    recr.findtext("univGbnNm"),
                    recr.findtext("year")
                ))

            conn.commit()
            print(f"✅ 저장 완료: {major['학과명']} ({major['학과ID']})")


    print("🎉 모든 학과 상세정보 저장 완료!")

finally:
    conn.close()
