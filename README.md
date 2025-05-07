# Valley Telegram Bot

텔레그램 봇을 통한 포인트 적립 및 광고 시청 시스템

## 기능

- 사용자/그룹 등록 및 관리
- 포인트 시스템
  - 광고 시청을 통한 포인트 획득
  - 일일 포인트 획득 제한
  - 개인/그룹별 포인트 관리
- 다국어 지원
  - 한국어/영어 지원
  - 사용자/그룹별 언어 설정
- 광고 시스템
  - 랜덤 광고 표시
  - 광고 시청 기록 관리
  - 포인트 자동 지급

## 프로젝트 구조

```
valley/
├── bot.py              # 봇 메인 실행 파일
├── requirements.txt    # 프로젝트 의존성
├── messages/          # 다국어 메시지
│   ├── ko_texts.py    # 한국어 메시지
│   └── en_texts.py    # 영어 메시지
├── model/             # 데이터베이스 모델
│   └── init/         # 데이터베이스 초기화
│       └── 01_create_tables.sql
└── handler/          # 봇 핸들러
    └── button_handlers.py
```

## 설치 및 실행

1. 의존성 설치
```bash
pip install -r requirements.txt
```

2. 데이터베이스 설정
- PostgreSQL 데이터베이스 생성
- `model/init/01_create_tables.sql` 실행

3. 환경 변수 설정
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

4. 봇 실행
```bash
python bot.py
```

## 데이터베이스 구조

### users
- 사용자 정보 및 언어 설정 저장

### groups
- 그룹 정보 및 언어 설정 저장

### points
- 사용자/그룹별 포인트 관리

### ads
- 광고 내용 및 활성화 상태 관리

### ad_view_logs
- 광고 시청 기록 및 포인트 획득 내역

## 사용 방법

1. 봇 시작
```
/start
```

2. 포인트 확인
```
/points
```

3. 광고 시청
- AD 버튼 클릭
- 하루에 한 번 포인트 획득 가능

4. 언어 설정
- Language 버튼 클릭
- 한국어/영어 선택

## 라이선스

MIT License 