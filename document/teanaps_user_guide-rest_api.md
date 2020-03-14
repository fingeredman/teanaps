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
- 무분별한 API 사용을 방지하고자 `ACCESS TOKEN` 발급을 통해 API 접근권한을 관리합니다.
- API 호출시 관리자 문의를 통해 발급받은 `ACCESS TOKEN`을 BODY에 포함해 요청해야 합니다. 
- `ACCESS TOKEN` 발급은 관리자 이메일(fingeredman@gmail.com)로 아래 내용을 포함해 문의 바랍니다.

  - 이름 : 홍길동
  - 소속 : 회사/대학교/연구소/그룹 등
  - 사용목적 : "~ 분석/구축 프로젝트" 수행시 감성분석 활용 등

### `TEANAPS` OPEN API List

> `TEANAPS` OPEN API는 `TEANAPS`에서 지원하는 텍스트 분석 기능을 REST API로 제공합니다. 모든 API는 비로그인 방식의 OPEN API로, 호출시 관리자 문의를 통해 발급받은 `ACCESS TOKEN`을 BODY에 포함해 전송해주셔야 합니다. 

- 기본 요청 URL : http://api.teanaps.com/
- API 버전 : v1 (2019.7.12 ~)

  > | API ID  | 호출방식        | 응답형식 | 역할                        | 요청 URL              | 평균응답속도 |
  > |---------|--------------|--------|----------------------------|----------------------|-----------|
  > | T01-01 | HTTP (POST) | JSON | [API 응답체크](./teanaps_user_guide-rest_api.md#t01-01-api-응답체크) | /alive | 0.029s |
  > | T02-01 | HTTP (POST) | JSON | [형태소분석](./teanaps_user_guide-rest_api.md#t02-01-형태소분석) | /nlp/pos | 0.154s |
  > | T02-02 | HTTP (POST) | JSON | [개체명인식](./teanaps_user_guide-rest_api.md#t02-02-개체명인식) | /nlp/ner | 0.150s |
  > | T03-01 | HTTP (POST) | JSON | [감성분석](./teanaps_user_guide-rest_api.md#t03-01-감성분석) | /text_analysis/sentiment | 0.676s |

    > Notes :  
    > - 평균응답속도는 무선 네트워크 환경에서 API를 요청하고 응답을 받는데 까지 걸리는 시간을 의미하며, 해당 시험결과는 1,000회 연속 API요청에 대한 응답속도의 평균입니다.

### 상세정보

#### [T01-01] API 응답체크
> REST API 동작여부와 ACCESS TOKEN의 유효성을 확인합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | access_token | V | str | ACCESS TOKEN | ODMFKGLDICK20190601132625 |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | api_condition | str | API 상태 | free |
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
    > data = {
    >     "access_token": "ODMFKGLDICK20190601132625"
    > } 
    >
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'api_condition': 'free',
    >   'access_token_info': {
    >     'access_token': 'ODMFKGLDICK20190601132625',
    >     'created_at': '2019-06-01',
    >     'expiration_in': '2019-09-06'
    >   }
    > }
    > ```

#### [T02-01] 형태소분석
> 문장을 형태소분석하고 그 결과를 반환합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | access_token | V | str | ACCESS TOKEN | ODMFKGLDICK20190601132625 |
  > | sentence | V | str | 한국어 또는 영어로 구성된 문장. 최대 128자. | 손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다. |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | sentence | str | 요청문장 | 손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다. |
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
    > data = {
    >     "access_token": "ODMFKGLDICK20190601132625",
    >     "sentence": "손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다."
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'sentence': '손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다.',
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

    > Notes :  
    > - `TEANAPS` 형태소분석 API의 품사태그는 세종말뭉치 품사태그를 기본으로 사용합니다. 품사태그표는 [Appendix](./teanaps_user_guide-appendix.md#teanaps-형태소-품사태그표)를 참고해주세요.
    > - `TEANAPS` 형태소분석 API의 성능 및 특징은 [성능평가 결과](./teanaps_user_guide-appendix.md#teanaps-성능평가-결과)를 참고해주세요.


#### [T02-02] 개체명인식
> 문장에서 개체명을 인식하고 그 결과를 반환합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | access_token | V | str | ACCESS TOKEN | ODMFKGLDICK20190601132625 |
  > | sentence | V | str | 한국어 또는 영어로 구성된 문장. 최대 128자. | 손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다. |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | sentence | str | 요청문장 | 손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다. |
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
    > data = {
    >     "access_token": "ODMFKGLDICK20190601132625",
    >     "sentence": "손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다."
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'sentence': '손흥민은 2015년 레버쿠젠에서 토트넘 핫스퍼로 이적했다.',
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

    > Notes :  
    > - `TEANAPS` 개체명인식 API의 개체명 태그는 총 16종으로 구분됩니다. 태그 종류 및 구분은 [정보통신단체표준 (TTAS)](http://committee.tta.or.kr/data/standard_view.jsp?nowPage=32&pk_num=TTAK.KO-10.0852&nowSu=318&rn=1)을 따릅니다.
    > - 개체명 태그표는 [Appendix](./teanaps_user_guide-appendix.md#teanaps-개체명-태그표)를 참고해주세요.
    > - `TEANAPS` 개체명인식 API의 성능 및 특징은 [성능평가 결과](./teanaps_user_guide-appendix.md#teanaps-성능평가-결과)를 참고해주세요.

#### [T03-01] 감성분석
> 문장의 감성수준을 긍정 또는 부정으로 분류하고 그 결과를 반환합니다.  

- 요청 파라미터 (Request Parameter)

  > | 파라미터        |  필수 |  유형 |  설명          | 샘플                       |
  > |--------------|------|------|---------------|---------------------------|
  > | access_token | V | str | ACCESS TOKEN | ODMFKGLDICK20190601132625 |
  > | sentence | V | str | 한국어 또는 영어로 구성된 문장. 최대 128자. | 손흥민이 이번 퇴장으로 1년 동안 3번째 퇴장을 기록했다. |

- 응답 파라미터 (Response Parameter)

  > | 파라미터      |  유형 |  설명         | 샘플        |
  > |------------|------|--------------|------------|
  > | code | int | 응답코드 | 200 |
  > | sentence | str | 요청문장 | 손흥민은 이번 퇴장으로 1년 동안 3번째 퇴장을 기록했다. |
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
    > data = {
    >     "access_token": "ODMFKGLDICK20190601132625",
    >     "sentence": "손흥민은 이번 퇴장으로 1년 동안 3번째 퇴장을 기록했다."
    > } 
    > 
    > url = URL + VERSION + URL_PATTERN
    > r = requests.post(url, data=data)
    > j = r.json()
    > print(j)
    > ```

    > Output (Response):
    > ```python
    > {
    >   'code': 200,
    >   'sentence': '손흥민은 이번 퇴장으로 1년 동안 3번째 퇴장을 기록했다.',
    >   'sentiment': 'negative',
    >   'sentiment_score': {
    >     'positive': 0.0339,
    >     'negative': 0.9634
    >   }
    > }
    > ```

#### 응답코드

- 공통 응답코드입니다.

  > | Code |  Message         | DESC         |
  > |------|------------------|---------------|
  > | 200 | Success | 요청이 정상 처리되었습니다. |
  > | 401 | Incorrect request | 요청 파라미터가 잘못되었습니다. |
  > | 402 | Invalid ACCESS TOKEN | ACCESS TOKEN이 유효하지 않습니다. |


<br><br>
---
<center>ⓒ 2020. FINGEREDMAN all rights reserved.</center>