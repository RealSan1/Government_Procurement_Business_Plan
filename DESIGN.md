**프로젝트 개요**
- **이름**: 대학일자리플러스센터 (FastAPI + Jinja2)
- **목표**: 공고 조회·등록(관리자), 상담 신청·관리, 학과/강소기업/자료 제공
- **언어/런타임**: Python 3.10+, FastAPI, Uvicorn

**아키텍처 개요**
- **웹 서버**: FastAPI (라우팅 + 템플릿 렌더링)
- **템플릿**: Jinja2 (`templates/`)
- **정적 파일**: `static/` (이미지, CSS, JS)
- **데이터베이스**: MySQL/MariaDB 권장 (개발은 SQLite 사용 가능)
- **배포 옵션**: Docker + Gunicorn/Uvicorn, 또는 systemd 서비스(uvicorn)

**주요 엔드포인트 정리**
- **GET `/`**: `index.html` (메인 페이지)
- **GET `/intro`**: 소개 페이지
- **GET `/jobs/external`**: 외부 공고 리스트
- **GET `/jobs/internal`**: 교내 공고 리스트 (관리자 버튼: `admin_cookie`로 표시)
- **GET `/jobs/post`**: 공고 등록 폼 (관리자 전용)
- **POST `/jobs/post`**: 공고 등록
- **GET `/jobs/review`**: 검수 페이지 (대기중 공고)
- **POST `/jobs/approve`**, **POST `/jobs/reject`**: 승인/거절
- **GET `/major/search?q=`**: 학과 검색
- **GET `/major/{id}`**: 학과 상세 (JSON)
- **GET `/consult`**: 상담 신청 페이지 (상담사 목록, 학생 내역 optional)
- **POST `/consult/apply`**: 상담 신청 (JSON)
- **GET `/admin/consult`**: 관리자 상담 목록
- **POST `/admin/consults/{consult_id}/{action}`**: 상담 승인/거절
- **GET `/resources`**, **GET `/resources/detail/{post_id}`**, **GET/POST `/resources/write`**: 자료실
- **GET `/company`**: 강소기업 목록

**권한/인증 설계**
- 현재 요구: 회원가입/로그인 없음. 관리 작업(공고 등록/승인, 상담관리)은 간단한 `admin_cookie`로 구분되어 있음.
- 권장 개선: 운영 환경에서는 환경변수 기반 관리자 비밀번호(간단 토큰) 또는 OAuth/세션을 도입하여 `admin_cookie` 우회 위험 제거.

**DB 스키마 제안 (요약)**
- **jobs**
  - `id` INT PK AUTO_INCREMENT
  - `title`, `company`, `job_categories`, `employment_type`, `substitute`, `recruit_type`, `period`, `education`, `location`, `num_recruits`, `url`
  - `status` ENUM('대기','승인','거절') DEFAULT '대기'
  - `created_at`, `updated_at`
  - 인덱스: `status`, `company`, FULLTEXT(`title`)
- **consults**
  - `id`, `student_id`(학번), `consult_type`, `consultant_id`, `memo`, `status`, `created_at`
  - 인덱스: `student_id`, `status`
- **consultants**: `id`, `name`, `department`, `contact`
- **majors**: `id`, `name`, `description`, `college`, `detail_json`
- **companies**: `id`, `name`, `description`, `website`, `tags`
- **resources**: `id`, `title`, `content`, `category`, `is_notice`, `author`, `created_at`, `views`

**API (샘플)**
- **POST `/jobs/post`**
  - Request: form-data 또는 JSON
  - Response: `200 { "success": true, "job_id": <id> }` 또는 에러 코드
- **POST `/consult/apply`**
  - Request JSON: `{ "학번": "20231234", "상담유형": "취업", "상담사id": 5, "메모": "..." }`
  - Response: `200 { "message": "상담 신청 완료" }`
- **GET `/major/{id}`**
  - Response: `200` JSON 상세 또는 `404 { "error": "학과 정보가 없습니다." }`

**템플릿/프론트엔드 책임**
- `index.html`: 메인 콘텐츠(슬라이더, 카드). 서버는 카드 데이터(공고 요약)를 제공.
- `jobs/post.html`: 클라이언트 검증과 서버 검증 모두 필요(필수 필드 확인)
- `jobs/review.html`: 승인/거절 인터랙션은 AJAX 권장
- `consult.html`: 상담 신청은 AJAX 또는 JSON POST
- `resources/write.html`: 작성 후 서버에서 리다이렉트

**테스트 계획**
- 단위: `getQuery/*.py` 함수 로직 모킹(pymysql 또는 ORM을 모킹)
- 통합: 스테이징 DB 또는 SQLite로 API 흐름 검증
- E2E: Selenium으로 주요 흐름(메인 로드, 상담 신청, 자료 등록, 공고 등록·승인) 자동화
- CI: GitHub Actions로 `pytest` 실행, E2E는 별도 워크플로(셀레니움 허용 런너 또는 Selenium Grid)


**보안·운영 가이드**
- 입력 검증: 파라미터화된 쿼리 또는 ORM 사용(SQL 주입 방지)
- 관리자 권한: 현재 `admin_cookie` 취약, 운영시 토큰/비밀번호 기반 인증으로 대체
- 로그: 접근/에러/감사 로그 수집(중요 이벤트: 승인/거절 기록)
- 백업: DB 일별 스냅샷, 정적 파일 정기 백업
- CORS: 현재 `allow_origins=["*"]`는 개발용, 운영 환경에서는 도메인 제한

**운영 체크리스트 (빠른 항목)**
- DB 마이그레이션 준비(예: `alembic`)  
- 정적 파일·이미지 저장 위치(로컬 vs S3) 결정  
- 관리자 인증(간단 토큰) 도입 여부 결정  
- CI에서 테스트 자동화 설정

**파일과 추가 작업 제안**
- `DESIGN.md` (현재 파일) 저장됨. 추가로 원하시면 아래를 생성합니다:
  - `alembic` 초기 설정 + 마이그레이션 스크립트 템플릿
  - 간단한 관리자 인증(환경변수 TOKEN 체크) 패치
  - Dockerfile 및 docker-compose.yml 스켈레톤

---
