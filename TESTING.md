# 테스트 가이드

이 문서는 프로젝트의 테스트 전략과 실행 방법을 설명합니다.

## 개요

세 가지 레벨의 테스트를 제공합니다:

1. **단위 테스트 (Unit Tests)**: `tests/test_unit.py`
   - `getQuery/*.py` 함수 로직 검증 (DB 모킹)
   - pytest + mock 사용
   
2. **통합 테스트 (Integration Tests)**: `tests/test_integration.py`
   - FastAPI 엔드포인트 흐름 검증
   - TestClient로 HTTP 요청/응답 검증
   
3. **E2E 테스트 (End-to-End Tests)**: `tests/test_e2e_selenium.py`
   - Selenium으로 실제 브라우저 동작 자동화
   - 주요 사용자 흐름: 메인/상담/자료/공고 등록/검수

---

## 로컬 환경 설정

### 1. 가상환경 생성 (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. 의존성 설치

```powershell
pip install -r requirements.txt
```

### 3. pytest 설정 확인

`pytest.ini`가 프로젝트 루트에 있어야 합니다.

---

## 테스트 실행 방법

### 단위 테스트만 실행

```powershell
pytest tests/test_unit.py -v
```

**예상 출력:**
```
tests/test_unit.py::TestJobOpening::test_fetch_jobs_ex_returns_list PASSED
tests/test_unit.py::TestJobOpening::test_insert_job_success PASSED
...
```

### 통합 테스트만 실행

```powershell
pytest tests/test_integration.py -v
```

**예상 출력:**
```
tests/test_integration.py::TestMainPageEndpoints::test_index_page_returns_200 PASSED
tests/test_integration.py::TestJobEndpoints::test_jobs_external_returns_200 PASSED
...
```

### E2E 테스트만 실행

**사전 요구:**
- 로컬에서 FastAPI 서버 실행:
  ```powershell
  # 다른 터미널에서
  uvicorn main:app --host 127.0.0.1 --port 8000
  ```

- Chrome 브라우저 설치 필요

**테스트 실행:**
```powershell
pytest tests/test_e2e_selenium.py -v -s
```

**예상 출력:**
```
tests/test_e2e_selenium.py::TestMainPageFlow::test_main_page_loads_successfully PASSED
✓ 메인 페이지 로드 성공: 대학일자리플러스센터
tests/test_e2e_selenium.py::TestMainPageFlow::test_navigate_to_intro PASSED
✓ 소개 페이지로 이동 성공
...
```

### 모든 테스트 실행

```powershell
pytest tests/ -v
```

### 특정 테스트 클래스만 실행

```powershell
pytest tests/test_unit.py::TestJobOpening -v
```

### 특정 테스트만 실행

```powershell
pytest tests/test_unit.py::TestJobOpening::test_fetch_jobs_ex_returns_list -v
```

### 커버리지 보고서 생성

```powershell
pytest tests/test_unit.py tests/test_integration.py --cov=getQuery --cov-report=html
# 생성된 htmlcov/index.html을 브라우저로 열기
```

### E2E 테스트 스크린샷 확인

E2E 테스트 실행 후 스크린샷과 HTML이 저장됩니다:

```powershell
# 파일 탐색기로 열기
Start-Process .\tests\_last_run
```

---

## GitHub Actions 자동화

### 1. 단위 & 통합 테스트 (.github/workflows/tests.yml)

**트리거:**
- `main`, `develop` 브랜치에 push
- Pull Request 생성

**동작:**
- Python 3.10, 3.11에서 테스트 실행
- 커버리지 보고서 생성
- Codecov에 업로드 (선택사항)

### 2. E2E 테스트 (.github/workflows/e2e.yml)

**트리거:**
- `main` 브랜치에 push
- Pull Request (main 대상)
- 매일 자정(UTC) 스케줄 실행

**동작:**
- Chrome + Selenium 설치
- FastAPI 서버 자동 시작
- E2E 테스트 실행
- 실패 시 스크린샷 저장
- HTML 리포트 생성

**아티팩트:**
- `selenium-screenshots/`: 실패한 테스트의 스크린샷
- `e2e-test-report.html`: 테스트 상세 리포트

---

## 테스트 마크 사용 (선택사항)

### 느린 테스트만 실행

```powershell
pytest tests/ -m slow -v
```

### 느린 테스트 제외

```powershell
pytest tests/ -m "not slow" -v
```

### 단위 테스트만 실행

```powershell
pytest tests/ -m unit -v
```

---

## 테스트 작성 가이드

### 1. 단위 테스트 추가

`tests/test_unit.py`에서:

```python
from unittest.mock import patch, MagicMock

class TestNewFeature:
    @patch('getQuery.newmodule.pymysql.connect')
    def test_new_function(self, mock_connect):
        # Mock DB connection
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [...]
        
        # Test
        from getQuery.newmodule import new_function
        result = new_function()
        
        # Assert
        assert result is not None
```

### 2. 통합 테스트 추가

`tests/test_integration.py`에서:

```python
def test_new_endpoint(self, client):
    """새 엔드포인트 테스트"""
    response = client.get("/new-endpoint")
    assert response.status_code == 200
    assert "expected content" in response.text
```

### 3. E2E 테스트 추가

`tests/test_e2e_selenium.py`에서:

```python
def test_new_user_flow(self, driver):
    """새 사용자 흐름 테스트"""
    driver.get(f"{BASE_URL}/")
    time.sleep(1)
    
    # 클릭, 입력 등
    element = driver.find_element(By.ID, "button-id")
    element.click()
    
    # 검증
    assert "success" in driver.page_source
```

---

## 토러블슈팅

### pytest를 찾을 수 없음

```powershell
pip install pytest
```

### TestClient 임포트 오류

```powershell
pip install httpx
```

### Selenium 드라이버 문제

```powershell
# webdriver-manager는 자동으로 Chrome 드라이버 다운로드
# 수동 설치:
# 1. Chrome 브라우저 설치
# 2. https://chromedriver.chromium.org 에서 드라이버 다운로드
# 3. PATH 환경변수에 추가
```

### 서버 연결 오류 (E2E)

```
ConnectionRefusedError: [Errno 111] Connection refused
```

**원인:** FastAPI 서버가 실행 중이지 않음  
**해결:**
```powershell
# 새 터미널에서
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 타임아웃 오류

E2E 테스트가 너무 느리면 `pytest.ini`의 `timeout` 값 증가:

```ini
timeout = 60  # 초 단위
```

---

## CI/CD 통합 확인

GitHub Actions 워크플로 상태는 다음에서 확인합니다:

1. GitHub 저장소 → **Actions** 탭
2. 워크플로 선택: `Unit & Integration Tests` 또는 `E2E Selenium Tests`
3. 최신 실행 클릭하여 로그 확인

---

## 성능 팁

### 테스트 병렬 실행 (pytest-xdist)

```powershell
pip install pytest-xdist
pytest tests/ -n auto  # CPU 코어 수만큼 병렬 실행
```

### 실패한 테스트만 재실행

```powershell
pytest tests/ --lf  # last-failed
pytest tests/ --ff  # failed-first
```

### 테스트 결과 캐시 삭제

```powershell
pytest tests/ --cache-clear
```

---

## 참고 자료

- [pytest 공식 문서](https://docs.pytest.org/)
- [FastAPI 테스트](https://fastapi.tiangolo.com/tutorial/testing/)
- [Selenium 문서](https://www.selenium.dev/documentation/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

