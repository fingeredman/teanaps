# TEANAPS API Tutorial (TBU)

---
## ACCESS TOKEN
- API 사용자 인증을 위해 ACCESS TOKEN을 유저단위로 발급하여 사용합니다.
- API 호출시 관리자 문의를 통해 발급받은 ACCESS TOKEN을 요청 파라미터에 같이 전송해주셔야 합니다. 
- ACCESS TOKEN 발급은 관리자 이메일(fingeredman@gmail.com)을 통해 문의 바랍니다.

---
## TEANAPS API 리스트
> TEANAPS API는 TEANAPS 패키지의 기능을 OPEN API 형태로 제공합니다. 일부 기능은 패키지와 API가 제공하는 결과에 차이가 있을 수 있습니다. 모든 API는 비로그인 방식의 OPEN API로, 호출시 관리자 문의를 통해 발급받은 ACCESS TOKEN을 같이 전송해주셔야 합니다. 

| API ID  | 호출방식        | 응답형식 | 역할                        | 요청 URL              |
|---------|-----------------|----------|-----------------------------|-----------------------|
| T001-01 | HTTP (GET/POST) | JSON     | API 응답체크                | /v1/ping              |
| T002-01 | HTTP (POST)     | JSON     | 형태소 태그 태깅            | /v1/tag/pos           |
| T002-02 | HTTP (POST)     | JSON     | 형태소 및 개체명 태그 태깅  | /v1/tag/ner           |
| T002-03 | HTTP (POST)     | JSON     | 구문분석 트리 파싱          | /v1/tag/syntax        |

---
## API 호출 예시
- 다음은 TEANAPS 형태소분석 API를 호출하는 Python 코드입니다.  
- API 호출방식은 예외를 두는 경우를 제외하고 POST 방식을 사용합니다.
- API 요청 결과값은 JSON 형식으로 응답합니다.

Python Code (Request):
```python
import requests

URL = "http://api.teanaps.com"
VERSION = "/v1"
ACCESS_TOKEN = "req_to_admin"
URL_PATTERN = "/tag/pos"
data = {
    "access_token": ACCESS_TOKEN,
    "sentence": "아버지가 방에 들어가신다."
} 

url = URL + VERSION + URL_PATTERN
r = requests.post(url, data=data)
j = r.json()
print(j)
```

Output (Response):
```python
{
  'code': 200,
  'result': [
    {
      'location': [0, 3],
      'pos_tag': 'NNG',
      'word': '아버지'
    },
    {
      'location': [3, 4],
      'pos_tag': 'JKS',
      'word': '가'
    },
    ...
    {
      'location': [11, 13],
      'pos_tag': 'EP+EF',
      'word': '신다'
    },
    {
      'location': [13, 14],
      'pos_tag': 'SF',
      'word': '.'
    }
  ]
}
```

---
## API 호출 가이드
### 텍스트 전처리 (Text Pre-processing)
#### 1. 형태소분석 (POS Tagging)
##### 요청 파라미터 (Request Parameter)
> ACCESS TOKEN을 파라미터에 담아 POST 방식으로 요청합니다.  

| 파라미터     | 필수 | 유형 | 설명          | 샘플                      |
|--------------|------|------|---------------|---------------------------|
| access_token | V    | str  | ACCESS TOKEN  | req_to_admin              |
| sentence     | V    | str  | 태깅 요청문장 | 아버지가 방에 들어가신다. |

##### 응답 파라미터 (Response Parameter)
> 응답은 JSON 형식으로 응답코드(code)와 응답결과(result)로 구성됩니다.  

| 파라미터   | 유형 | 설명         | 샘플       |
|------------|------|--------------|------------|
| code       | list | 응답코드     | 200        |
| result     | list | 응답결과     | []         |
| ㄴindex    | int  | 단어 인덱스  | 0, 1, 2, … |
| ㄴword     | str  | 단어         | 아버지     |
| ㄴpos_tag  | str  | 형태소태그   | NNG        |
| ㄴlocation | list | 문장 내 좌표 | [0, 3]     |

---
## Update History
> 2019.10.26. 초안입력  
