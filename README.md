# `TEANAPS`: Text Analysis APIs
> ![teanaps_logo_1600x400](https://raw.githubusercontent.com/fingeredman/teanaps-documents/main/data/logo/teanaps_logo_1600x400.png)

> `TEANAPS`는 자연어 처리(NLP)와 텍스트 분석을 위한 `Python` 라이브러리 입니다. 텍스트 분석을 위해서는 `Python` 프로그래밍 뿐만아니라 다양한 자연어 처리 및 머신러닝 라이브러리 사용법 까지 배워야합니다(e.g., KoNLPy, NLTK, Gensim). 하지만 학습해야하는 내용이 적지않고 난이도도 높아 `Python` 프로그래밍에 충분히 익숙하지 않으신 분들은 접근하기가 쉽지 않습니다.  
`TEANAPS`는 자언어 처리와 텍스트 분석에 필요한 다양한 라이브러리를 하나의 인터페이스로 통합하고 `Google Colabotory`를 활용해 설치환경을 일원화하여, 텍스트 분석을 위한 사전 준비작업을 최소화하고 분석에 필요한 시간을 최소화 할 수 있도록 도와줍니다. 본 라이브러리를 활용하기 전 `Python` 기초문법과 텍스트 분석에 필요한 필수 사전지식을 먼저 학습하시기를 추천드리며, [`WIKI` 문서](https://github.com/fingeredman/teanaps/wiki#teanaps-text-analysis-apis)를 참조하시어 `TEANAPS`를 활용해보시길 권장드립니다. ([`TEANAPS` 소개자료](https://github.com/fingeredman/teanaps-documents/blob/main/introduction/teanaps_introduction_20210611_v1.3.pdf))

- 본 자료는 텍스트 분석을 활용한 연구 및 강의를 위한 목적으로 제작되었습니다.
- 본 자료를 강의 또는 연구 목적으로 활용하고자 하시는 경우 반드시 사전에 아래 메일주소로 연락주세요.
- 본 자료에 대한 <U>상업적 활용과 허가되지 않은 배포를 금지</U>합니다.
- 강의, 저작권, 출판, 특허, 공동저자에 관련해서는 문의 바랍니다.
- **Contact : ADMIN(admin@teanaps.com)**

---
## Notice! 

> - !메일확인 지연안내! 메일서버 오류로 2022년 11월 부터 12월 기간동안 수신된 관리자 메일 확인이 누락되었습니다. 늦었지만 확인되는대로 회신드리도록 하겠습니다. 양해 부탁드립니다.
> - `TEANAPS` 라이브러리가 `v0.9.700` 버전으로 업데이트 되었습니다. 기존 설치하신 분들은 반드시 업데이트 후 사용 바랍니다.
> - `Docker` 가상환경을 활용해 내 PC에서도 간단하게 `TEANAPS` 라이브러리를 활용해볼 수 있습니다. [**`Docker` 설치 가이드**](https://github.com/fingeredman/teanaps/wiki/INSTALL-GUIDE#docker-for-everyone)를 확인해보세요.  
> - [**`TEANAPS` WIKI**](https://github.com/fingeredman/teanaps/wiki#teanaps-text-analysis-apis-for-education)가 업로드 되었습니다. `TEANAPS` 라이브러리에 대한 자세한 설명과 활용 가이드를 확인해보세요.
> - `TEANAPS` 라이브러리 사용법 및 샘플코드는 [`API Documentation`](https://github.com/fingeredman/teanaps/wiki/ARCHITECTURE#teanaps-api-documentation)을 참조해주시기 바랍니다.
> - [`TEANAPS` Web Scrapper](https://github.com/fingeredman/teanaps-web-scrapper#teanaps-web-scrapper)로 텍스트 데이터를 직접 수집하고 `TEANAPS` 라이브러리를 활용해 분석해보세요.
> - `TEANAPS`를 활용한 실무/연구 프로젝트 **지원이 필요하신 분** 또는 **사례 공유가 가능하신 분**의 연락을 기다립니다.     
(***Contact : admin@teanaps.com***)  
> - 본 자료는 국내 대학강의 및 학회, 세미나에 교육 및 실습자료로 활용되고 있습니다. ([`Use Case` 살펴보기](https://github.com/fingeredman/teanaps/wiki/USE-CASES#teanaps-use-cases))

---
## What can you do with `TEANAPS`?
> ![what_can_you_do](https://raw.githubusercontent.com/fingeredman/teanaps-documents/main/data/sample_image/what_can_you_do.png)

> `#TEANAPS` `#티냅스` `#티냅스_라고_불러주세요` `#텍스트분석` `#text_analysis` `#TA` `#텍스트마이닝` `#text_mining` `#자연어처리` `#nlp` `#텍스트전처리` `#text_pre-processing` `#띄어쓰기_보정` `#불용어` `#stopwords` `#동의어` `#synonym` `#치환사전` `#replacement` `#언어식별` `#language_detection` `#임베딩` `#embedding` `#형태소분석` `#pos_tagging` `#개체명인식` `#named_entity` `#ner` `#구문분석` `#syntax_analysis` `#TF-IDF` `#감성분석` `#sentiment_analysis` `#긍부정` `#긍부정_키워드` `#클러스터링` `#문서군집화` `#text_clustering` `#문서분류` `#text_classification` `#문서유사도` `#text_similarity` `#네트워크분석` `#network_analysis` `#네트워크중심성` `#network_centrality` `#연관어분석` `#co-word_analysis` `#키워드추출` `#keyword_extraction` `#문서요약` `#text_summarization` `#docker` `#jupyter_notebook`
 
---
## Why `TEANAPS`?

- `TEANAPS`를 활용하면 <U>**분석코드를 최대 70% 까지 간소화**</U>할 수 있습니다. ([분석코드 살펴보기](https://github.com/fingeredman/teanaps/wiki/ARCHITECTURE#teanaps-api-documentation))
- `TEANAPS`는 최신 언어모델을 적용해 오픈소스 라이브러리 대비 <U>**높은 퍼포먼스**</U>를 제공합니다. ([성능평가 결과 살펴보기](https://github.com/fingeredman/teanaps/wiki/APPENDIX#appendix))
- `TEANAPS`는 분석결과를 효과적으로 표현하기 위한 <U>**다양한 시각화**</U> 를 제공합니다. ([시각화 기능 살펴보기](https://github.com/fingeredman/teanaps/wiki/VISUALIZATION#teanaps-api-documentation))
- `TEANAPS`는 <U>**OPEN API**</U>를 통해 다양한 환경에서 텍스트 분석을 지원합니다.
- `TEANAPS`는 텍스트 분석을 위한 <U>[**`WIKI` 문서**](https://github.com/fingeredman/teanaps/wiki#teanaps-text-analysis-apis), [강의/실습 자료](https://github.com/fingeredman/advanced-text-mining#advanced-text-mining)</U>를 무료로 제공합니다.
- `TEANAPS`는 다양한 도메인의 <U>**`프로젝트/연구`**</U>를 무료로 지원합니다.  
(***Contact : admin@teanaps.com***)  

---
<p align ="left">
<img src="https://img.shields.io/badge/http://teanaps.com-181717?style=flat-square&logo=GitHub&logoColor=white" />
<img src="https://img.shields.io/badge/admin@teanaps.com-4FAEBD?style=flat-square&logo=Gmail&logoColor=white" />
<img src="https://img.shields.io/badge/ⓒ 2022. TEANAPS all rights reserved.-4A4535?style=flat-square&logo=&logoColor=white" />
<img src="https://img.shields.io/badge/[상표등록번호] 제 40－1795866 호-85433A?style=flat-square&logo=&logoColor=white" />
