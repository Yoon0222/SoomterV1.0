# SoomterV1.0
Soomter 프로젝트

## 🛠️ 프로젝트 서버 구조 및 아키텍처

### 🧱 인프라 구성
- **플랫폼**: AWS EC2 (Ubuntu 24.04)
- **웹 서버**: Nginx (Reverse Proxy, Docker 컨테이너로 구동)
- **애플리케이션 서버**: FastAPI (Docker 컨테이너로 구동)
- **데이터베이스**: MariaDB (Docker 컨테이너로 구동, 내부 네트워크로 연결)

### 🐳 Docker 구성
- `docker-compose.yml`을 통한 컨테이너 오케스트레이션
- 컨테이너 구성:
  - `fastapi`: 백엔드 API 서버
  - `nginx`: 프론트 Reverse Proxy
  - `mariadb`: 데이터 저장소

### 🔁 CI/CD 파이프라인
- **GitHub Actions** 기반 자동 배포
- `main` 브랜치에 Push → 서버에 SSH 접속 후:
  - 최신 코드 Pull
  - Docker 컨테이너 재빌드 및 재시작 (`docker-compose up --build -d`)
- SSH Key 인증 기반 보안 구성

### 🧩 사용 프레임워크 및 라이브러리
- **Python 3.11**
- **FastAPI**: RESTful API 서버 프레임워크
- **SQLAlchemy** / **Databases**: 비동기 ORM
- **Alembic**: 마이그레이션 관리
- **Uvicorn**: ASGI 서버
- **Pytest**, **pytest-asyncio**: 테스트 프레임워크
- **python-dotenv**: 환경변수 관리

### 🗂️ 디렉토리 구조 (예시)

SoomterV1.0/

├── app/

│ ├── main.py

│ ├── routers/

│ ├── models/

│ └── ...

├── Dockerfile

├── docker-compose.yml

├── .env

└── .github/

└── workflows/

└── deploy.yml

### 📝 기타 참고
- 모든 민감 정보(`.env`)는 `.gitignore`로 Git에서 제외
- 마이그레이션은 `alembic revision --autogenerate` 및 `alembic upgrade head` 명령 사용


