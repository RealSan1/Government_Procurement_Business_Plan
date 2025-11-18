"""
단위 테스트 (Unit Tests - Smoke Tests)
getQuery/*.py 함수들이 올바르게 임포트되고 호출 가능한지 검증합니다.

실행: pytest tests/test_unit.py -v
"""

import pytest
import os


class TestImports:
    """모듈 임포트 테스트 (기본 검증)"""
    def test_import_jobOpening(self):
        """getQuery.jobOpening 임포트 가능한지 확인"""
        try:
            from getQuery.jobOpening import fetch_jobs_ex, fetch_jobs_in, insert_job
            assert callable(fetch_jobs_ex)
            assert callable(fetch_jobs_in)
            assert callable(insert_job)
        except ImportError as e:
            pytest.fail(f"Failed to import jobOpening: {e}")

    def test_import_consult(self):
        """getQuery.consult 임포트 가능한지 확인"""
        try:
            from getQuery.consult import fetch_consults, apply_consult
            assert callable(fetch_consults)
            assert callable(apply_consult)
        except ImportError as e:
            pytest.fail(f"Failed to import consult: {e}")

    def test_import_major(self):
        """getQuery.major 임포트 가능한지 확인"""
        try:
            from getQuery.major import search_majors, get_major_detail_full
            assert callable(search_majors)
            assert callable(get_major_detail_full)
        except ImportError as e:
            pytest.fail(f"Failed to import major: {e}")

    def test_import_company(self):
        """getQuery.company 임포트 가능한지 확인"""
        try:
            from getQuery.company import companyInfo
            assert callable(companyInfo)
        except ImportError as e:
            pytest.fail(f"Failed to import company: {e}")

    def test_import_resources(self):
        """getQuery.resources 임포트 가능한지 확인"""
        try:
            from getQuery.resources import resources_list_data, get_resource_detail, create_resource
            assert callable(resources_list_data)
            assert callable(get_resource_detail)
            assert callable(create_resource)
        except ImportError as e:
            pytest.fail(f"Failed to import resources: {e}")


class TestFastAPIEndpoints:
    """FastAPI 엔드포인트 존재 여부 테스트"""

    def test_main_app_can_be_imported(self):
        """main.py의 FastAPI 앱 임포트 가능한지 확인"""
        try:
            from main import app
            assert app is not None
        except ImportError as e:
            pytest.fail(f"Failed to import FastAPI app: {e}")


class TestModuleStructure:
    """프로젝트 모듈 구조 검증"""

    def test_getQuery_is_package(self):
        """getQuery가 패키지인지 확인"""
        assert os.path.isdir('getQuery'), "getQuery 디렉토리 없음"

    def test_main_py_exists(self):
        """main.py 파일 존재 확인"""
        assert os.path.isfile('main.py'), "main.py 파일 없음"

    def test_templates_directory_exists(self):
        """templates 디렉토리 존재 확인"""
        assert os.path.isdir('templates'), "templates 디렉토리 없음"

    def test_static_directory_exists(self):
        """static 디렉토리 존재 확인"""
        assert os.path.isdir('static'), "static 디렉토리 없음"

    def test_required_getQuery_modules(self):
        """getQuery 필수 모듈 확인"""
        required_modules = ['jobOpening.py', 'consult.py', 'major.py', 'company.py', 'resources.py']
        for module in required_modules:
            path = os.path.join('getQuery', module)
            assert os.path.isfile(path), f"{module} 파일 없음"

    def test_required_templates(self):
        """필수 템플릿 파일 확인"""
        required_templates = [
            'index.html',
            'header.html',
            'footer.html',
            'intro.html',
            'consult.html',
        ]
        for template in required_templates:
            path = os.path.join('templates', template)
            assert os.path.isfile(path), f"{template} 템플릿 파일 없음"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
