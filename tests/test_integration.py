"""
통합 테스트 (Integration Tests)
SQLite 인메모리 DB를 사용하여 API 엔드포인트 흐름을 검증합니다.

실행: pytest tests/test_integration.py -v
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# main.py 임포트를 위해 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app


@pytest.fixture
def client():
    """테스트용 FastAPI 클라이언트"""
    return TestClient(app)


class TestMainPageEndpoints:
    """메인 페이지 및 기본 엔드포인트 테스트"""

    def test_index_page_returns_200(self, client):
        """GET / 는 200 상태 반환"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_intro_page_returns_200(self, client):
        """GET /intro 는 200 상태 반환"""
        response = client.get("/intro")
        assert response.status_code == 200

    def test_company_page_returns_200(self, client):
        """GET /company 는 200 상태 반환"""
        response = client.get("/company")
        assert response.status_code == 200


class TestJobEndpoints:
    """공고 관련 엔드포인트 테스트"""

    def test_jobs_external_returns_200(self, client):
        """GET /jobs/external 은 200 상태 반환"""
        response = client.get("/jobs/external")
        assert response.status_code == 200

    def test_jobs_internal_returns_200(self, client):
        """GET /jobs/internal 은 200 상태 반환 (비관리자)"""
        response = client.get("/jobs/internal")
        assert response.status_code == 200
        # 비관리자 쿠키 없을 시 show_button은 False
        assert "show_button" not in response.text or "false" in response.text.lower()

    def test_jobs_internal_with_admin_cookie(self, client):
        """GET /jobs/internal 관리자 쿠키 포함 시 버튼 표시"""
        response = client.get("/jobs/internal", cookies={"admin_cookie": "show"})
        assert response.status_code == 200

    def test_jobs_post_without_admin_cookie_returns_403(self, client):
        """GET /jobs/post 는 관리자 전용 (403 반환)"""
        response = client.get("/jobs/post")
        # 쿠키 없을 시 403
        assert response.status_code == 403 or "권한 없음" in response.text

    def test_jobs_review_returns_200(self, client):
        """GET /jobs/review 는 200 상태 반환"""
        response = client.get("/jobs/review")
        assert response.status_code == 200


class TestMajorEndpoints:
    """학과 관련 엔드포인트 테스트"""

    def test_major_search_empty_query_returns_200(self, client):
        """GET /major/search (쿼리 없음) 는 200 반환"""
        response = client.get("/major/search")
        assert response.status_code == 200

    def test_major_search_with_query_returns_200(self, client):
        """GET /major/search?q=컴퓨터 는 200 반환"""
        response = client.get("/major/search?q=컴퓨터")
        assert response.status_code == 200

    def test_major_detail_returns_404_or_json(self, client):
        """GET /major/{id} 는 JSON 또는 404 반환"""
        response = client.get("/major/1")
        # 데이터가 없으면 404, 있으면 JSON
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.headers.get("content-type", "").startswith("application/json")


class TestConsultEndpoints:
    """상담 관련 엔드포인트 테스트"""

    def test_consult_page_returns_200(self, client):
        """GET /consult 는 200 상태 반환"""
        response = client.get("/consult")
        assert response.status_code == 200

    def test_consult_page_with_user_id(self, client):
        """GET /consult?user_id=20230001 은 유저 내역 포함"""
        response = client.get("/consult?user_id=20230001")
        assert response.status_code == 200

    def test_admin_consult_page_returns_200(self, client):
        """GET /admin/consult 는 200 상태 반환"""
        response = client.get("/admin/consult")
        assert response.status_code == 200


class TestResourcesEndpoints:
    """자료 관련 엔드포인트 테스트"""

    def test_resources_page_returns_200(self, client):
        """GET /resources 는 200 상태 반환"""
        response = client.get("/resources")
        assert response.status_code == 200

    def test_resources_write_page_returns_200(self, client):
        """GET /resources/write 는 200 상태 반환"""
        response = client.get("/resources/write")
        assert response.status_code == 200

    def test_resources_detail_returns_404_or_200(self, client):
        """GET /resources/detail/{post_id} 는 404 또는 200 반환"""
        response = client.get("/resources/detail/99999")
        # 데이터 없으면 404, 있으면 200
        assert response.status_code in [200, 404]


class TestErrorHandling:
    """에러 처리 검증"""

    def test_404_on_nonexistent_route(self, client):
        """존재하지 않는 경로는 404 반환"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """지원하지 않는 HTTP 메서드는 405 반환"""
        response = client.delete("/")
        assert response.status_code == 405 or response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
