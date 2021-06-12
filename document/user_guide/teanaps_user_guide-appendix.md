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
- [`TEANAPS` OPEN API](./teanaps_user_guide-rest_api.md#teanaps-user-guide)
- [Tutorial](./teanaps_user_guide-tutorial.md#teanaps-user-guide)
- [Use Cases](./teanaps_user_guide-references_journal_project.md#teanaps-user-guide)
- Appendix

---
## Appendix

### `TEANAPS` 성능평가 결과
- 형태소 분리 및 품사태깅

    - 특징
      - `TEANAPS`의 형태소 분리(tokenizing) 기능은 <U>고유명사(인물, 장소, 상품명 등)를 하나의 형태소로 매우 잘 구분</U>합니다.
      - `TEANAPS`의 형태소 분리 및 품사태깅(PoS tagging) 속도는 <U>`Okt`에 비해 300~400% 빠르며</U>, 이는 공개된 형태소분석기 중 가장 빠른 <U>`MeCab`의 약 80% 수준 속도</U>입니다.

    - 처리속도 비교
      > ![validation_pos](../data/sample_image/validation_pos.png)

	- 출력 결과 비교
      > **Input \:**    
      > "*<U>손흥민</U>(28)이 <U>4경기</U> 연속 골이자 자신의 시즌 <U>14호</U> 골을 작렬하며 <U>잉글랜드</U> 프로축구 <U>토트넘 홋스퍼</U>를 <U>잉글랜드축구협회</U>(FA)컵 16강에 올려놨다.*"


      > | Token             | MeCab with `TEANAPS`| MeCab           | Okt             | KKMA       |
      > |-------------------|---------------------|-----------------|-----------------|------------|
      > | 손흥민(28)이        | 손흥민/NNP/PS         |  손흥민/NNP      | 손흥민/Noun       | 손/NNG      |
      > |                   |                     |                 |                 | 흥/NNG     |
      > |                   |                     |                 |                 | 민/NNG     |
      > |                   | (/SW                |  (/SW           | (/Punctuation   | (/SS       |
      > |                   | 28/NNP/QT           |  28/NNP         | 28/Number       | 28/NR      |
      > |                   | )/SW                |  )/SW           | )/Punctuation   | )/SS       |
      > |                   | 이/JKS              |  이/JKS          | 이/Noun         | 이/MDT      |
      > | 4경기 연속 골이자     | 4경기/NNP/QT         |  4/SN           | 4/Number        | 4/NR       |
      > |                   |                     |  경기/NNG        | 경기/Noun        | 경기/NNG    |
      > |                   | 연속/NNG             |  연속/NNG        | 연속/Noun        | 연속/NNG    |
      > |                   | 골/NNG              |  골/NNG          | 골/Noun         | 골/NNG      |
      > |                   | 이/VCP              |  이/VCP          | 이자/Noun        | 이/JKS      |
      > |                   | 자/EC               |  자/EC           |                 | 자/VV       |
      > |                   |                    |                  |                 | 아/ECS     |
      > | 자신의             | 자신/NNG             |  자신/NNG         | 자신/Noun        | 자신/NNG    |
      > |                   | 의/JKG              |  의/JKG          | 의/Josa          | 의/JKG     |
      > | 시즌 14호 골을      | 시즌/NNG             |  시즌/NNG         | 시즌/Noun        | 시즌/NNG    |
      > |                   | 14호/NNP/QT         |  14/SN          | 14/Number        | 14/NR     |
      > |                   |                     |  호/NNB         | 호/Noun          | 호/NNM      |
      > |                   | 골/NNG              |  골/NNG          | 골/Noun          | 골/NNG     |
      > |                   | 을/JKO              |  을/JKO          | 을/Josa          | 을/JKO     |
      > | 작렬하며            | 작렬/NNG             |  작렬/NNG        | 작렬/Noun         | 작렬/NNG    |
      > |                   | 하/XSV              |  하/XSV          | 하며/Verb        | 하/XSV      |
      > |                   | 며/EC               |  며/EC           |                 | 며/ECE      |
      > | 잉글랜드            | 잉글랜드/NNP/LC       |  잉글랜드/NNP      | 잉글랜드/Noun     | 잉/MAG      |
      > |                   |                    |                  |                 | 글/NNG      |
      > |                   |                    |                  |                 | 랜드/NNG    |
      > | 프로축구            | 프로/NNG             |  프로/NNG        | 프로축구/Noun      | 프로/NNG    |
      > |                   | 축구/NNG             |  축구/NNG        |                 | 축구/NNG    |
      > | 토트넘 홋스퍼를       | 토트넘 홋스퍼/NNP/OG   |  토트넘/NNP       | 토트넘/Noun       | 토트/NNG    |
      > |                   |                     |                 |                 | 넘/NNB     |
      > |                   |                     |  홋스퍼를/UN      | 홋스퍼/Noun       | 홋스퍼/UN   |
      > |                   | 를/JKO              |                  | 를/Josa         | 를/JKO     |
      > | 잉글랜드축구협회(FA)컵 | 잉글랜드축구협회/NNP/OG |  잉글랜드/NNP      | 잉글랜드/Noun     | 잉/MAG     |
      > |                   |                    |                  |                 | 글/NNG     |
      > |                   |                    |                  |                 | 랜드/NNG    |
      > |                   |                    |  축구/NNG         | 축구/Noun        | 축구/NNG    |
      > |                   |                    |  협회/NNG         | 협회/Noun        | 협회/NNG    |
      > |                   | (/SW               |  (/SW            | (/Punctuation   | (/SS       |
      > |                   | FA/NNP/OG          |  FA/OL           | FA/Alpha        | FA/OL      |
      > |                   | )/SW               |  )/SW            | )/Punctuation   | )/SS       |
      > |                   | 컵/NNG              |  컵/NNG          | 컵/Noun         | 컵/NNG      |
      > | 16강에             | 16강/NNP/QT         |  16/SN          | 16/Number       | 16/NR       |
      > |                  |                     |  강/NNG          | 강/Noun          | 강/NNG      |
      > |                  | 에/JKB               |  에/JKB          | 에/Josa         | 에/JKM       |
      > | 올려놨다.           | 올려놨/VV+EP         |  올려놨/VV+EP     | 올려놨다/Verb      | 올리/VV     |
      > |                  |                      |                 |                 | 어/ECS      |
      > |                  |                      |                 |                 | 놓/VV       |
      > |                  |                      |                 |                 | 았/EPT      |
      > |                  | 다/EF                |  다/EF           |                 | 다/EFN      |
      > |                  | ./SW                |  ./SW           | ./Punctuation    | ./SF       |

- 개체명인식

    - 특징
      - `TEANAPS`의 개체명인식(NER) 기능은 <U>고유명사(인물, 장소, 상품명 등)를 인식하고 분류</U>하는 성능이 매우 뛰어납니다.
      - `TEANAPS` 개체명인식 모델 학습 결과, Validation 셋에 대해 <U>약 97.8%의 인식률</U>을 보입니다.
      - 학습데이터 도메인 제한으로 개체명 구간이 정상 인식되었으나 분류가 알수없음(UN)인 경우가 발생할 수 있습니다.
    - 개체명인식 모델 학습결과
      > ![validation_ner](../data/sample_image/validation_ner.png)

	- 출력 결과 샘플
      > **Input 1 \:**  
      > "*TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다.*"  
      > **>>** "*<TEANAPS\:UN>는 텍스트 마이닝을 위한 <Python\:UN> 패키지 입니다.*"  
      > ![validation_ner_ex1](../data/sample_image/validation_ner_ex1.png)
     
      > **Input 2 \:**  
      > "*영국 매체 스카이 스포츠는 25일 맨유 미드필더 폴 포그바가 여름 이적시장 실패 후, 1월 레알 마드리드로 이적할 수 있다고 전했다.*"  
      > **>>** "*<영국\:LC> 매체 <스카이 스포츠\:UN>는 <25일\:DT> <맨유\:OG> 미드필더 <폴 포그바\:PS>가 여름 이적시장 실패 후, <1월\:DT> <레알 마드리드\:OG>로 이적할 수 있다고 전했다.*"  
      > ![validation_ner_ex2](../data/sample_image/validation_ner_ex2.png)

      > **Input 3 \:**  
      > "*최근 코로나 바이러스의 여파로 연세대학교 제 768회 졸업식이 취소되었음을 알려드립니다.*"  
      > **>>** "*최근 <코로나 바이러스\:UN>의 여파로 <연세대학교\:OG> <제 768회\:QT> 졸업식이 취소되었음을 알려드립니다.*"  
      > ![validation_ner_ex3](../data/sample_image/validation_ner_ex3.png)

      > **Input 4 \:**  
      > "*오늘 출시된 V60 ThinkQ는 LG전자의 핵심 제품입니다.*"  
      > **>>** "*오늘 출시된 <V60 ThinkQ\:UN>는 <LG전자\:OG>의 핵심 제품입니다.*"    
      > ![validation_ner_ex4](../data/sample_image/validation_ner_ex4.png)

      > **Input 5 \:**  
      > "*충청북도 청주는 교육의 도시입니다.*"  
      > **>>** "*<충청북도\:LC> <청주\:LC>는 교육의 도시입니다.*"  
      > ![validation_ner_ex5](../data/sample_image/validation_ner_ex5.png)

### `TEANAPS` 형태소 품사태그표
- `TEANAPS` 형태소 분석기의 형태소 품사태그는 `세종말뭉치 품사태그`를 기본으로 하여 아래와 같이 통일하여 사용합니다.  

    > | 구분        | 품사                       | `TEANAPS` | 세종 | MeCab     | Okt                                                   | KKMA                           |
    > |-------------|----------------------------|---------|------|-----------|-------------------------------------------------------|--------------------------------|
    > | 체언        | 일반명사                   | NNG     | NNG  | NNG       | Noun                                                  | NNG                            |
    > |             | 고유명사                   | NNP     | NNP  | NNP       | ProperNoun                                            | NNP                            |
    > |             | 의존명사                   | NNB     | NNB  | NNB, NNBC |                                                       | NNB, NNM                       |
    > |             | 수사                       | NR      | NR   | NR        | Number                                                | NR                             |
    > |             | 대명사                     | NP      | NP   | NP        |                                                       | NP                             |
    > | 용언        | 동사                       | VV      | VV   | VV        | Verb                                                  | VV                             |
    > |             | 형용사                     | VA      | VA   | VA        | Adjective                                             | VA                             |
    > |             | 보조용언                   | VX      | VX   | VX        |                                                       | VXV, VXA                       |
    > |             | 긍정지정사                 | VCP     | VCP  | VCP       |                                                       | VCP                            |
    > |             | 부정지정사                 | VCN     | VCN  | VCN       |                                                       | VCN                            |
    > | 관형사      | 관형사                     | MM      | MM   | MM        | Determiner, Modifier                                  | MDT, MDN                       |
    > | 부사        | 일반부사                   | MAG     | MAG  | MAG       | Adverb                                                | MAG                            |
    > |             | 접속부사                   | MAJ     | MAJ  | MAJ       | Adverb                                                | MAC                            |
    > | 감탄사      | 감탄사                     | IC      | IC   | IC        | Exclamation                                           | IC                             |
    > | 조사        | 주격조사                   | JKS     | JKS  | JKS       | Josa                                                  | JKS                            |
    > |             | 보격조사                   | JKC     | JKC  | JKC       | Josa                                                  | JKC                            |
    > |             | 관형격조사                 | JKG     | JKG  | JKG       | Josa                                                  | JKG                            |
    > |             | 목적격조사                 | JKO     | JKO  | JKO       | Josa                                                  | JKO                            |
    > |             | 부사격조사                 | JKB     | JKB  | JKB       | Josa                                                  | JKM                            |
    > |             | 호격조사                   | JKV     | JKV  | JKV       | Josa                                                  | JKI                            |
    > |             | 인용격조사                 | JKQ     | JKQ  | JKQ       | Josa                                                  | JKQ                            |
    > |             | 접속조사                   | JC      | JC   | JC        | Conjunction                                           | JC                             |
    > |             | 보조사                     | JX      | JX   | JX        |                                                       | JX                             |
    > | 선어말 어미 | 선어말어미                 | EP      | EP   | EP        | PreEomi                                               | EPH, EPT,  EPP                 |
    > | 어말 어미   | 종결어미                   | EF      | EF   | EF        | Emoi                                                  | EFN, EFQ,  EFO, EFA,  EFI, EFR |
    > |             | 연결어미                   | EC      | EC   | EC        | Emoi                                                  | ECE, ECD,  ECS                 |
    > |             | 명사형 전성어미            | ETN     | ETN  | ETN       | Emoi                                                  | ETN                            |
    > |             | 관형형 전성어미            | ETM     | ETM  | ETM       | Emoi                                                  | ETD                            |
    > | 접두사      | 체언접두사                 | XPN     | XPN  | XPN       | VerbPrefix                                            | XPV                            |
    > | 접미사      | 명사파생접미사             | XSN     | XSN  | XSN       | Suffix                                                | XSN                            |
    > |             | 부사파생접미사             | XSM     |      |           | Suffix                                                | XSM                            |
    > |             | 동사파생접미사             | XSV     | XSV  | XSV       | Suffix                                                |                                |
    > |             | 형용사파생접미사           | XSA     | XSA  | XSA       | Suffix                                                |                                |
    > |             | 기타접미사                 | XSO     |      |           | Suffix                                                | XSO                            |
    > | 어근        | 어근                       | XR      | XR   | XR        |                                                       | XR                             |
    > | 부호        | 마침표, 물음표, 느낌표     | SW      | SF   | SF        | Punctuation                                           | SF                             |
    > |             | 쉼표, 가웃뎃점, 콜론, 빗금 | SW      | SP   | SC        | CashTagOthers                                         | SP                             |
    > |             | 따옴표, 괄호표, 줄표       | SW      | SS   | SSO, SSC  | CashTagOthers                                         | SS                             |
    > |             | 줄임표                     | SW      | SE   | SE        | CashTagOthers                                         | SE                             |
    > |             | 물결표, 숨김표, 빠짐표     | SW      | SO   | SY        | CashTagOthers                                         | SO                             |
    > |             | 기타기호                   | SW      | SW   | SY        | CashTagOthers,  Hashtag,  ScreenName,  KoreanParticle | SW                             |
    > | 불능        | 명사형추정범주             | UN      | NF   |           | Unknown                                               |                                |
    > |             | 용언추정범주               | UN      | NV   |           | Unknown                                               |                                |
    > |             | 분석불능범주               | UN      | NA   |           | Unknown                                               |                                |
    > | 기타        | 외국어                     | OL      | SL   | SL        | AlphaForeign                                          | OL                             |
    > |             | 한자                       | OL      | SH   | SH        | AlphaForeign                                          | OH                             |
    > |             | 숫자                       | SN      | SN   | SN        |                                                       | ON                             |

### `TEANAPS` 개체명 태그표
- `TEANAPS` 개체명 인식기의 개체명 태그는 총 16종으로 구분됩니다. 
- 개체명 태그의 종류 및 구분은 [정보통신단체표준(TTAS)](http://committee.tta.or.kr/data/standard_view.jsp?nowPage=32&pk_num=TTAK.KO-10.0852&nowSu=318&rn=1)을 따릅니다.

    > |    | 구분                | 태그 | 설명                                                                |
    > |----|--------------------|----|---------------------------------------------------------------------|
    > | 1  | 사람(Person)        | PS | 사람 이름                                                             |
    > | 2  | 분야(Study Field)   | FD | 정치/경제/사회/과학/사회과학/의학/예술/철학 등 학문, 학파                        |
    > | 3  | 이론(Theory)        | TR | 이론, 법칙, 원리, 사상, 진단법, 처방, 예술양식, 사조, 학설, 체계, 방식            |
    > | 4  | 인공물(Artifacts)   | AF | 문화재, 토목/건축, 교통수단, 작품, 서적, 악기, 무기, 상품, 공연                  |
    > | 5  | 기관(Organization)  | OG | 기관/단체, 업체, 회사/기업, 종파                                           |
    > | 6  | 장소(Location)      | LC | 국가, 행정구역, 도시, 강, 호수, 바다, 섬, 대륙, 명소, 천체                      |
    > | 7  | 문명(Civilization)  | CV | 문명, 문화, 종족, 스포츠, 도구, 제도, 언어, 양식, 음식/음료, 직업, 인간관계, 상, 법  |
    > | 8  | 날짜(Date)          | DT | 기간, 절기, 날짜, 달, 년, 계절, 시대                                       |
    > | 9  | 시간(Time)          | TI | 시간, 기간, 시각, 분, 초                                                 |
    > | 10 | 수량(Quantity)      | QT | 수량, 나이, 크기, 넓이, 인원수, 무게, 비율, 속도, 온도, 부피, 순서, 금액, 우편번호   |
    > | 11 | 사건(Event)         | EV | 사회운동, 선언, 전쟁, 혁명, 스포츠 행사, 축제, 사건/사고                         |
    > | 12 | 동물(Animal)        | AM | 동물, 곤충, 조류, 어류, 포유류, 양서류, 파충류, 분류명, 신체부위                  |
    > | 13 | 식물(Plant)         | PT | 꽃, 풀, 나무, 과일, 열매, 식물 유형, 식물 부위                                |
    > | 14 | 물질(Meterial)      | MT | 원소, 금속, 암석, 화학물질                                                |
    > | 15 | 용어(Term)          | TM | 색, 방향, 기후, 모양/형태, 증상, 약품, 용어, URL, 이메일 주소, 모델, 부품, 프로젝트  |
    > | 16 | 알 수 없음           | UN | 특정 개체명 분류에 해당하지 않는 단어                                         |

## References
- Install KoNLPy in colaboratory [(Link)](https://github.com/konlpy/konlpy/issues/188#issuecomment-383550386)  
- MeCab PoS tagger for Mac/Linux [(Link)](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)  
- MeCab PoS tagger for Windows [(Link)](https://cleancode-ws.tistory.com/97)  
- KoBERT [(Link)](https://github.com/sktbrain/kobert)  
- Pytorch-BERT-CRF-NER [(Link)](https://github.com/eagle705/pytorch-bert-crf-ner)  
- Korean Sentence Splitter [(Link)](https://github.com/hyunwoongko/kss?fbclid=IwAR2G4Ym3OwQOeouTokpjTMXo49vpZGuF5mYS7GUsmTSpKehXvDrCqSj-Zhk#korean-sentence-splitter) 

<br><br>
---
<center>ⓒ 2021. TEANAPS all rights reserved.</center>