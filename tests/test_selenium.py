from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def test_index_title():
    """로컬 서버의 루트 페이지(`http://127.0.0.1:8000/`) 타이틀에
    '대학일자리플러스센터'가 포함되어 있는지 확인합니다.

    주의: 이 테스트를 실행하려면 로컬에서 FastAPI 서버(`uvicorn main:app`)가
    포트 8000으로 실행 중이어야 하고, Chrome 브라우저를 사용할 수 있어야 합니다.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get("http://127.0.0.1:8000/")
        # 렌더링 대기 (간단한 대기; 필요 시 더 정교한 대기 사용)
        time.sleep(0.5)
        # 진단 자료: 스크린샷과 페이지 HTML 저장
        out_dir = os.path.join(os.path.dirname(__file__), "_last_run")
        os.makedirs(out_dir, exist_ok=True)
        screenshot_path = os.path.join(out_dir, "index.png")
        html_path = os.path.join(out_dir, "index.html")
        try:
            driver.save_screenshot(screenshot_path)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"DIAG: screenshot saved -> {screenshot_path}")
            print(f"DIAG: page html saved -> {html_path}")
        except Exception as e:
            print("DIAG: failed to save diagnostics:", e)

        # 페이지 요약 정보 출력
        print("DIAG: current_url=", driver.current_url)
        print("DIAG: title=", driver.title)
        # h3 요소(카드 제목 등)를 몇 개 출력
        h3_texts = [el.text for el in driver.find_elements(By.TAG_NAME, "h3")]
        print("DIAG: found h3 count=", len(h3_texts))
        for i, t in enumerate(h3_texts[:5]):
            print(f"DIAG: h3[{i}] -> {t}")

        assert "대학일자리플러스센터" in driver.title
    finally:
        driver.quit()


if __name__ == "__main__":
    import sys, traceback

    try:
        print("RUN: test_index_title()")
        test_index_title()
        print("OK: test_index_title passed")
        sys.exit(0)
    except AssertionError as e:
        print("FAIL: AssertionError -", e)
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        sys.exit(2)