import requests
import xml.etree.ElementTree as ET
import os, db
from dotenv import load_dotenv

load_dotenv("apikey.env")

conn = db.get_conn()

API_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo216L01.do"
API_KEY = os.getenv("강소API")

params = {
    "authKey": API_KEY,
    "returnType": "XML",
    "startPage": 5,
    "display": 100  # 가져올 데이터 개수
}

try:
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    response.encoding = 'utf-8'
    xml_data = response.text

    root = ET.fromstring(xml_data)

    with conn.cursor() as cur:
        for item in root.findall(".//smallGiant"):
            try:
                상시근로자수 = item.findtext("alwaysWorkerCnt")
                if 상시근로자수 is not None:
                    상시근로자수 = int(상시근로자수)
                else:
                    상시근로자수 = 0

                data = {
                    "선정연도": item.findtext("selYear"),
                    "강소기업브랜드명": item.findtext("sgBrandNm"),
                    "기업명": item.findtext("coNm"),
                    "사업자등록번호": item.findtext("busiNo"),
                    "대표자": item.findtext("reperNm"),
                    "업종코드_상": item.findtext("superIndTpCd"),
                    "업종명_상": item.findtext("superIndTpNm"),
                    "업종코드_중": item.findtext("indTpCd"),
                    "업종명_중": item.findtext("indTpNm"),
                    "지역코드": item.findtext("regionCd"),
                    "지역명": item.findtext("regionNm"),
                    "주소": item.findtext("coAddr"),
                    "주요생산품목": item.findtext("coMainProd"),
                    "상시근로자수": 상시근로자수,
                    "강소기업브랜드코드": item.findtext("smlgntCoClcd")
                }

                sql = """
                    INSERT IGNORE INTO 강소기업
                    (선정연도, 강소기업브랜드명, 기업명, 사업자등록번호, 대표자,
                     업종코드_상, 업종명_상, 업종코드_중, 업종명_중,
                     지역코드, 지역명, 주소, 주요생산품목, 상시근로자수,
                     강소기업브랜드코드)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cur.execute(sql, tuple(data.values()))
            except Exception as e:
                print(f"데이터 삽입 실패: {data.get('기업명')}, 오류: {e}")

    conn.commit()
    print("강소기업 데이터 삽입 완료!")

except Exception as e:
    print(f"API 호출 또는 파싱 실패: {e}")

finally:
    conn.close()
