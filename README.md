# 비품 대여 서비스 예제

사내 비품(노트북, 프로젝터, 카메라 등)의 대여를 관리하는 API다. 『Claude Code로 완성하는 AI 에이전트 하네스』의 예제 저장소로, 회의실 예약 서비스와 같은 조직이 운영하는 두 번째 서비스를 가정한다.

## 실행

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
pytest
```

## API

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | /items | 비품 목록 |
| POST | /items | 비품 등록 |
| GET | /rentals | 대여 목록(`item_id`로 비품별 조회) |
| POST | /rentals | 대여 신청 |
| POST | /rentals/{id}/return | 반납(대여한 사람만, `X-User-Email` 헤더로 요청자 확인) |

## 라이선스

MIT
