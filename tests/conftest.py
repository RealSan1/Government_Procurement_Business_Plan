import pytest

# 테스트 환경에서 실제 MySQL 접속을 막기 위한 더미 커넥션
class _DummyCursor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, *args, **kwargs):
        # 실행은 무시
        self._last = (args, kwargs)

    def fetchall(self):
        return []

    def fetchone(self):
        return None


class _DummyConn:
    def cursor(self, *args, **kwargs):
        return _DummyCursor()

    def commit(self):
        pass

    def close(self):
        pass


@pytest.fixture(autouse=True)
def patch_db_get_conn(monkeypatch):
    """모든 테스트에서 `db.get_conn`을 더미 커넥션으로 치환합니다."""
    import db
    # 패키지 내부에서 `from db import get_conn`로 가져온 모듈 심볼도 덮어씌웁니다.
    monkeypatch.setattr(db, "get_conn", lambda: _DummyConn())
    try:
        import getQuery.consult as consult_mod
        monkeypatch.setattr(consult_mod, "get_conn", lambda: _DummyConn())
    except Exception:
        pass
    try:
        import getQuery.jobOpening as job_mod
        monkeypatch.setattr(job_mod, "get_conn", lambda: _DummyConn())
    except Exception:
        pass
    try:
        import getQuery.company as company_mod
        monkeypatch.setattr(company_mod, "get_conn", lambda: _DummyConn())
    except Exception:
        pass
    try:
        import getQuery.resources as resources_mod
        monkeypatch.setattr(resources_mod, "get_conn", lambda: _DummyConn())
    except Exception:
        pass
    try:
        import getQuery.major as major_mod
        monkeypatch.setattr(major_mod, "get_conn", lambda: _DummyConn())
    except Exception:
        pass
    yield
