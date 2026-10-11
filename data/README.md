# 데이터 안내

분석 기간: 2026-09-23~2026-10-06. 수집 CSV를 고정해 사용하며, 영화-일 관측의 키는 `date, movieCd`다.

| 파일 | 역할 |
|---|---|
| kobis_daily_top10.csv | 일별 TOP10 140행, 영화 17편의 관객·순위·상영 규모 |
| cine21_movies.csv | 현재 박스오피스 및 기간 내 보완 영화 16편의 상세정보 |
| title_matching_audit.csv | 영화명·개봉일 연결 확인과 미매칭 기록 |
| kobis_movie_identity.csv | 영화 상세정보 대조 결과 |
| movie_daily_features.csv | 정확한 전일·전주 비교와 파생 지표 |
| candidate_sensitivity.csv | 기준 조합 48개별 후보 수 |
| post_open_persistence.csv | 개봉 이후 등장일수와 관측 가능한 달력 일수 |
| external_events.csv | 외부 사건의 날짜·시행 상태·수량·출처 |
| data_dictionary.csv | 열 정의와 분석상의 주의점 |
| source_manifest.json | 공개 CSV 20개 파일의 SHA-256 |

원래 일별 수집 당시의 API JSON·HTML은 남아 있지 않다. 저장 CSV로 계산을 재현할 수 있으나 원자료를 소급해 독립 검증한 것은 아니다. 새 수집 모드부터 원응답을 보존한다.

전문가 평론 원문 CSV는 공개하지 않는다. 공개 노트북의 저장 자료에서도 원문을 제외하고 점수·평가자 수를 보존했다. 배포 자료는 출처가 있는 제3자 자료이며 이 저장소가 별도 이용 허락을 부여하지 않는다. API 키는 포함하지 않는다.

TOP10 밖의 날짜는 미관측이며 관객 0명이 아니다. 외부 사건 표의 빈칸도 프로모션이 없었다는 뜻이 아니다. 영화명 결합의 한계, 제공량과 실제 관람량의 차이는 보고서에 설명했다.
