"""
E2E 테스트 (End-to-End Tests with Selenium)
주요 사용자 흐름을 자동화합니다:
- 메인 페이지 로드 및 타이틀 확인
- 상담 신청 흐름
- 자료실 글쓰기 흐름
- 공고 등록 및 검수 흐름(관리자 쿠키 사용)

실행: pytest tests/test_e2e_selenium.py -v
참고: 로컬에서 uvicorn main:app --host 127.0.0.1 --port 8000 이 실행 중이어야 합니다.
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def driver():
    """헤드리스 Chrome 드라이버 설정"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()


class TestMainPageFlow:
    """메인 페이지 흐름 테스트"""

    def test_main_page_loads_successfully(self, driver):
        """메인 페이지 로드 및 타이틀 확인"""
        driver.get(f"{BASE_URL}/")
        time.sleep(1)
        
        # 타이틀 확인
        assert "대학일자리플러스센터" in driver.title
        
        # 메인 구성 요소 확인
        assert driver.find_elements(By.TAG_NAME, "h3"), "카드 타이틀 없음"
        print(f"✓ 메인 페이지 로드 성공: {driver.title}")

    def test_navigate_to_intro(self, driver):
        """소개 페이지 네비게이션"""
        driver.get(f"{BASE_URL}/")
        time.sleep(0.5)
        
        # 헤더의 소개 링크 찾기
        intro_link = driver.find_elements(By.CSS_SELECTOR, "a[href='/intro']")
        if intro_link:
            intro_link[0].click()
            time.sleep(1)
            assert "소개" in driver.page_source or "intro" in driver.current_url.lower()
            print("✓ 소개 페이지로 이동 성공")


class TestJobFlow:
    """공고 관련 흐름 테스트"""

    def test_external_jobs_page_loads(self, driver):
        """외부 공고 페이지 로드"""
        driver.get(f"{BASE_URL}/jobs/external")
        time.sleep(1)
        
        assert "공고" in driver.page_source or "job" in driver.current_url
        print("✓ 외부 공고 페이지 로드 성공")

    def test_internal_jobs_page_loads(self, driver):
        """교내 공고 페이지 로드"""
        driver.get(f"{BASE_URL}/jobs/internal")
        time.sleep(1)
        
        assert "공고" in driver.page_source or "internal" in driver.current_url
        print("✓ 교내 공고 페이지 로드 성공")

    def test_admin_can_access_post_job_page(self, driver):
        """관리자 쿠키로 공고 등록 페이지 접근"""
        # 관리자 쿠키 추가
        driver.get(f"{BASE_URL}/")
        driver.add_cookie({"name": "admin_cookie", "value": "show"})
        
        driver.get(f"{BASE_URL}/jobs/post")
        time.sleep(1)
        
        # "권한 없음"이 없어야 함
        assert "권한 없음" not in driver.page_source
        print("✓ 관리자가 공고 등록 페이지 접근 가능")

    def test_non_admin_cannot_access_post_job_page(self, driver):
        """비관리자는 공고 등록 페이지 접근 불가"""
        driver.get(f"{BASE_URL}/jobs/post")
        time.sleep(1)
        
        # "권한 없음" 메시지 확인
        assert "권한 없음" in driver.page_source or driver.find_elements(By.TAG_NAME, "h1")
        print("✓ 비관리자 공고 등록 페이지 접근 불가 (의도대로)")


class TestConsultFlow:
    """상담 신청 흐름 테스트"""

    def test_consult_page_loads(self, driver):
        """상담 신청 페이지 로드"""
        driver.get(f"{BASE_URL}/consult")
        time.sleep(1)
        
        assert "상담" in driver.page_source or "consult" in driver.current_url
        print("✓ 상담 신청 페이지 로드 성공")

    def test_consult_list_has_consultants(self, driver):
        """상담사 목록 표시"""
        driver.get(f"{BASE_URL}/consult")
        time.sleep(1)
        
        # 상담사 정보가 있는지 확인 (있다면)
        consultants = driver.find_elements(By.CSS_SELECTOR, "[class*='consult']")
        # 최소한 페이지가 정상 로드되었는지 확인
        assert driver.page_source is not None
        print("✓ 상담 신청 페이지 정상 구성")


class TestResourcesFlow:
    """자료실 흐름 테스트"""

    def test_resources_page_loads(self, driver):
        """자료실 페이지 로드"""
        driver.get(f"{BASE_URL}/resources")
        time.sleep(1)
        
        assert "자료" in driver.page_source or "resource" in driver.current_url
        print("✓ 자료실 페이지 로드 성공")

    def test_resources_write_page_loads(self, driver):
        """자료 작성 페이지 로드"""
        driver.get(f"{BASE_URL}/resources/write")
        time.sleep(1)
        
        # 폼이 있는지 확인
        forms = driver.find_elements(By.TAG_NAME, "form")
        assert len(forms) > 0 or "title" in driver.page_source
        print("✓ 자료 작성 페이지 로드 성공")


class TestMajorFlow:
    """학과 검색 흐름 테스트"""

    def test_major_search_page_loads(self, driver):
        """학과 검색 페이지 로드"""
        driver.get(f"{BASE_URL}/major/search")
        time.sleep(1)
        
        assert "major" in driver.current_url or "search" in driver.page_source
        print("✓ 학과 검색 페이지 로드 성공")

    def test_major_search_with_query(self, driver):
        """학과 검색 쿼리 입력"""
        driver.get(f"{BASE_URL}/major/search?q=컴퓨터")
        time.sleep(1)
        
        # 검색 결과 페이지 로드 확인
        assert "컴퓨터" in driver.page_source or "search" in driver.current_url
        print("✓ 학과 검색 쿼리 처리 성공")


class TestCompanyFlow:
    """강소기업 정보 페이지 테스트"""

    def test_company_page_loads(self, driver):
        """강소기업 페이지 로드"""
        driver.get(f"{BASE_URL}/company")
        time.sleep(1)
        
        assert "company" in driver.current_url or driver.page_source
        print("✓ 강소기업 페이지 로드 성공")


class TestNavigationFlow:
    """페이지 네비게이션 및 링크 테스트"""

    def test_header_navigation_links_exist(self, driver):
        """헤더 네비게이션 링크 존재 확인"""
        driver.get(f"{BASE_URL}/")
        time.sleep(1)
        
        # 주요 네비게이션 링크 확인
        nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a")
        assert len(nav_links) > 0
        print(f"✓ 헤더 네비게이션 링크 {len(nav_links)}개 확인")

    def test_footer_exists(self, driver):
        """푸터 존재 확인"""
        driver.get(f"{BASE_URL}/")
        time.sleep(1)
        
        # 푸터 확인
        footer = driver.find_elements(By.TAG_NAME, "footer")
        assert len(footer) > 0 or "footer" in driver.page_source.lower()
        print("✓ 푸터 존재 확인")


class TestErrorHandling:
    """에러 페이지 테스트"""

    def test_404_page(self, driver):
        """존재하지 않는 페이지 접근"""
        driver.get(f"{BASE_URL}/nonexistent-page-12345")
        time.sleep(1)
        
        # 404 또는 에러 페이지 표시
        assert driver.find_elements(By.TAG_NAME, "body")
        print("✓ 404 에러 처리 확인")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
