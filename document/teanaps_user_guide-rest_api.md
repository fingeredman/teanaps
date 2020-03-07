# `TEANAPS` User Guide

---
## Contents
- [Install `TEANAPS`](./teanaps_user_guide-install_teanaps.md#teanaps-user-guide)
- [API Documentation](./teanaps_user_guide-api_documentation-handler.md#teanaps-user-guide)
  - [Handler](./teanaps_user_guide-api_documentation-handler.md#teanaps-user-guide)
  - [NLP](./teanaps_user_guide-api_documentation-nlp.md#teanaps-user-guide)
  - [Text Analysis](./teanaps_user_guide-api_documentation-text_analysis.md#teanaps-user-guide)
  - [Visualization](./teanaps_user_guide-api_documentation-visualization.md#teanaps-user-guide)
  - [Machine Learning](./teanaps_user_guide-api_documentation-machine-learning.md#teanaps-user-guide)
- `TEANAPS` OPEN API
- [Tutorial](./teanaps_user_guide-tutorial.md#teanaps-user-guide)
- [References](./teanaps_user_guide-references_journal_project.md#teanaps-user-guide)
- [Journal & Project](./teanaps_user_guide-references_journal_project.md#teanaps-user-guide)
- [Appendix](./teanaps_user_guide-appendix.md#teanaps-user-guide)

---
## `TEANAPS` OPEN API

### ACCESS TOKEN 발급
- 무분별한 API 사용 방지을 위해 `ACCESS TOKEN`을 발급을 통해 API 접근권한을 부여합니다.
- API 호출시 관리자 문의를 통해 발급받은 `ACCESS TOKEN`을 HTTP Header에 같이 전송해주셔야 합니다. 
- `ACCESS TOKEN` 발급은 관리자 이메일(fingeredman@gmail.com)로 아래 내용을 포함해 문의 바랍니다.

  - 이름 : 홍길동
  - 소속 : 회사/대학교/연구소/그룹 등
  - 사용목적 : "~ 분석 및 구축 프로젝트" 수행시 감성분석 활용 등

### `TEANAPS` OPEN API List

> `TEANAPS` OPEN API는 `TEANAPS`에서 지원하는 텍스트 분석 기능을 REST API로 제공합니다. 모든 API는 비로그인 방식의 OPEN API로, 호출시 관리자 문의를 통해 발급받은 `ACCESS TOKEN`을 HTTP Header에 같이 전송해주셔야 합니다. 

- 기본정보

  > | API ID  | 호출방식        | 응답형식 | 역할                        | 요청 URL              |
  > |---------|--------------|--------|----------------------------|----------------------|
  > | T01-01 | HTTP (POST) | JSON | [API 응답체크](./teanaps_user_guide-rest_api.md#t01-01-api-응답체크) | http://api.teanaps.com/v1/alive |
  > | T02-01 | HTTP (POST) | JSON | [형태소분석](./teanaps_user_guide-rest_api.md#t02-01-형태소분석) | http://api.teanaps.com/v1/nlp/pos |
  > | T02-02 | HTTP (POST) | JSON | [개체명인식](./teanaps_user_guide-rest_api.md#t02-02-개체명인식) | http://api.teanaps.com/v1/nlp/ner |
  > | T03-01 | HTTP (POST) | JSON | [감성분석](./teanaps_user_guide-rest_api.md#t03-01-감성분석) | http://api.teanaps.com/v1/text_analysis/sentiment |

### 상세정보

#### [T01-01] API 응답체크
> REST API 동작여부와 ACCESS TOKEN의 유효성을 확인합니다.  

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | api_status | str | API 상태 | free |
  > | access_token_info | list | ACCESS TOKEN 상태 | |
  > | ㄴcreated_at | str | 생성일자 | 2019-06-01 |
  > | ㄴexpiration_in | str | 생성일자 | 2019-09-06 |

- 호출예시

    > Python Code (Request):
    > ```python
    > import requests
    > 
    > URL = "http://api.teanaps.com"
    > VERSION = "/v1"
    > URL_PATTERN = "/alive"
    > ACCESS_TOKEN = "req_to_admin"
    > headers = {
    >     "access_token": ACCESS_TOKEN
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, headers=headers)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'api_condition'
    >   'access_token_info': {
    >     'created_at': '2019-06-01',
    >     'expiration_in': '2019-09-06',
    >   }
    > }
    > ```

#### [T02-01] 형태소분석
> 문장을 형태소분석하고 그 결과를 반환합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | sentence | V | str | 한국어 또는 영어로 구성된 문장. 최대 128자. | 손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다. |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | pos_list | list | 형태소분석 결과 | |
  > | ㄴpos | str | 형태소 | 손흥민 |
  > | ㄴpos_tag | str | 품사 태그 | NNP |
  > | ㄴner_tag | str | 개체명 태그 | PS |
  > | ㄴlocation | list | 형태소 위치 | [0, 3] |

- 호출예시

    > Python Code (Request):
    > ```python
    > import requests
    > 
    > URL = "http://api.teanaps.com"
    > VERSION = "/v1"
    > URL_PATTERN = "/nlp/pos"
    > ACCESS_TOKEN = "req_to_admin"
    > headers = {
    >     "access_token": ACCESS_TOKEN
    > } 
    > data = {
    >     "sentence": "손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다."
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, headers=headers, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'pos_list': [
    >     {
    >       'pos': '손흥민',
    >       'pos_tag': 'NNP',
    >       'ner_tag': 'PS',
    >       'location': [0, 3]
    >     },
    >     {
    >       'pos': '은',
    >       'pos_tag': 'JX',
    >       'ner_tag': 'UN',
    >       'location': [3, 4]
    >     },
    >     ...
    >     {
    >       'pos': '다',
    >       'pos_tag': 'EF',
    >       'ner_tag': 'UN',
    >       'location': [30, 31]
    >     },
    >     {
    >       'pos': '.',
    >       'pos_tag': 'SW',
    >       'ner_tag': 'UN',
    >       'location': [31, 32]
    >     }
    >   ]
    > }
    > ```

#### [T02-02] 개체명인식
> 문장에서 개체명을 인식하고 그 결과를 반환합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | sentence | V | str | 한국어 또는 영어로 구성된 문장. 최대 128자. | 손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다. |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | ner_list | list | 형태소분석 결과 | |
  > | ㄴentity | str | 개체명 | 손흥민 |
  > | ㄴner_tag | str | 개체명 태그 | PS |
  > | ㄴlocation | list | 개체명 위치 | [0, 3] |

- 호출예시

    > Python Code (Request):
    > ```python
    > import requests
    > 
    > URL = "http://api.teanaps.com"
    > VERSION = "/v1"
    > URL_PATTERN = "/nlp/ner"
    > ACCESS_TOKEN = "req_to_admin"
    > headers = {
    >     "access_token": ACCESS_TOKEN
    > } 
    > data = {
    >     "sentence": "손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다."
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, headers=headers, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'ner_list': [
    >     {
    >       'entity': '손흥민',
    >       'ner_tag': 'PS',
    >       'location': [0, 3]
    >     },
    >     {
    >       'entity': '2015년',
    >       'ner_tag': 'DT',
    >       'location': [5, 10]
    >     },
    >     {
    >       'entity': '레버쿠젠',
    >       'ner_tag': 'OG',
    >       'location': [11, 15]
    >     },
    >     {
    >       'entity': '토트넘 핫스퍼',
    >       'ner_tag': 'OG',
    >       'location': [18, 25]
    >     }
    >   ]
    > }
    > ```

#### [T03-01] 감성분석
> 문장의 감성수준을 긍정 또는 부정으로 분류하고 그 결과를 반환합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | sentence | V | str | 한국어 또는 영어로 구성된 문장. 최대 128자. | 손흥민이 이번 퇴장으로 1년 동안 3번째 퇴장을 기록했다. |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | sentiment | str | 감성수준 | negative |
  > | sentiment_score | dict | | |
  > | ㄴpositive | float | 긍정 스코어 | 0.0339 |
  > | ㄴnegative | float | 부정 스코어 | 0.9634 |

- 호출예시

    > Python Code (Request):
    > ```python
    > import requests
    > 
    > URL = "http://api.teanaps.com"
    > VERSION = "/v1"
    > URL_PATTERN = "/text_analysis/sentiment"
    > ACCESS_TOKEN = "req_to_admin"
    > headers = {
    >     "access_token": ACCESS_TOKEN
    > } 
    > data = {
    >     "sentence": "손흥민이 이번 퇴장으로 1년 동안 3번째 퇴장을 기록했다."
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, headers=headers, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'sentiment': 'negative',
    >   'sentiment_score': {
    >     'positive': 0.0339,
    >     'negative': 0.9634
    >   }
    > }
    > ```

#### 응답코드

- 공통 응답코드입니다.

  > | 응답코드 |  메시지         | 설명        |
  > |--------|---------------|---------------|
  > | 200 | 응답성공 | |
  > | 301 | Invalid ACCESS TOKEN | ACCESS TOKEN이 유효하지 않습니다. |

<br><br>
---
<center>ⓒ 2020. FINGEREDMAN all rights reserved.</center>