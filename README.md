# URL Shortener

## Description

긴 URL을 짧게 단축하여 사용하고, 단축된 URL을 통해 원본 URL로 리디렉션하는 기능을 제공하는 URL 단축 서비스를 구축.
FastAPI를 이용하여 서버를 구현하고, MySQL 데이터베이스를 사용하여 데이터를 저장.

## 주요 기능
1. URL 단축 생성 

        ● 엔드포인트: POST /shorten  
        ● 요청 본문: {"url": "<original_url>", "expires_at": "<optional_expiration_date>"}  
        ● 응답 본문: {"short_url": "<shortened_url>"}  
        ● 입력받은 긴 URL을 고유한 단축 키로 변환하고 데이터베이스에 저장.  
   
2. URL 리디렉션

        ● 엔드포인트: GET /{short_key}  
        ● 단축된 URL을 통해 원본 URL로 리디렉션.  
        ● 조회 수를 증가.  
   
3. URL 통계 조회

        ● 엔드포인트: GET /stats/{short_key}  
        ● 단축 URL의 조회 수를 반환.  
        ● 응답 본문: {"short_key": "<short_key>", "click_count": <count>}  

## Databese
        ● MySQL을 사용하여 URL과 단축 키 매핑을 저장.  
        ● 데이터베이스 모델은 SQLAlchemy와 Alembic을 사용하여 관리.  
           ● Model  
              ● URL: 원본 URL, 단축 키, 생성일, 만료일, 클릭 수를 저장.  

## Mysql의 선택이유

 ● 가볍고 안정적이며 빠른 처리속도, 확장성또한 높다

## 설치 및 실행 방법 
환경 설정(windows 기준)  

● 가상 환경 설정:
```bash
python -m venv .venv
source .venv\Scripts\activate
```
● 패키지 설치:  
```bash
pip install -r requirements.txt
```
데이터베이스 설정  

● MySQL 데이터베이스 생성 및 설정:  
```sql
CREATE DATABASE url_shortener_db;
CREATE USER 'url_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON url_shortener_db.* TO 'url_user'@'localhost';
FLUSH PRIVILEGES;
```
환경 변수 설정

● .env 파일을 프로젝트 루트에 생성 후 설정:  
```env
DATABASE_URL="mysql+mysqlconnector://url_user:password@localhost/url_shortener_db"
```
데이터베이스 마이그레이션  

● Alembic을 이용하여 데이터베이스 스키마를 설정:  
```bash
alembic upgrade head
```
서버 실행  

● FastAPI 서버 실행:  
```bash
uvicorn app.main:app --reload
```
API 문서 확인  

● 브라우저에서 Swagger UI 확인: http://127.0.0.1:8000/docs  

API 사용 예시  

1. URL 단축
```bash
curl -X POST "http://127.0.0.1:8000/shorten" -H "Content-Type: application/json" -d "{\"url\": \"https://example.com\"}"
```

2. 단축된 URL 리디렉션
```bash
curl -L "http://127.0.0.1:8000/XVTbde"
```

3. URL 통계 조회
```bash
curl "http://127.0.0.1:8000/stats/XVTbde"
```

## 테스트 코드  
![image](https://github.com/user-attachments/assets/f5a3fdaf-cca8-41e3-8266-06a46b6cd846)  
![image](https://github.com/user-attachments/assets/3962ff76-2d16-439c-bc53-1f2e79a480ba)
리디렉션된 단축url 접속 후 카운트 1 증가  
![image](https://github.com/user-attachments/assets/8b738f21-96c5-4375-9fc6-7221c65fa9bd)














      
