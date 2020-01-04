# `TEANAPS` User Guide

---
## Contents
- [Install `TEANAPS`](./document/teanaps_user_guide-install_teanaps.md)
- [API Documents](./document/teanaps_user_guide-api_documents.md)
- [Tutorial](./document/teanaps_user_guide-tutorial.md)
- [References](./document/teanaps_user_guide-references_journal_project.md)
- [Journal & Project](./document/teanaps_user_guide-references_journal_project.md)
- [Appendix](./document/teanaps_user_guide-appendix.md)

---
## Appendix

### `TEANAPS` 형태소 품사태그표
- `TEANAPS` 형태소 분석기의 형태소 품사태그는 `세종말뭉치 품사태그`를 기본으로 하여 아래와 같이 통일하여 사용합니다.  

| 구분        | 품사                       | TEANAPS | 세종 | MeCab     | Okt                                                   | KKMA                           |
|-------------|----------------------------|---------|------|-----------|-------------------------------------------------------|--------------------------------|
| 체언        | 일반명사                   | NNG     | NNG  | NNG       | Noun                                                  | NNG                            |
|             | 고유명사                   | NNP     | NNP  | NNP       | ProperNoun                                            | NNP                            |
|             | 의존명사                   | NNB     | NNB  | NNB, NNBC |                                                       | NNB, NNM                       |
|             | 수사                       | NR      | NR   | NR        | Number                                                | NR                             |
|             | 대명사                     | NP      | NP   | NP        |                                                       | NP                             |
| 용언        | 동사                       | VV      | VV   | VV        | Verb                                                  | VV                             |
|             | 형용사                     | VA      | VA   | VA        | Adjective                                             | VA                             |
|             | 보조용언                   | VX      | VX   | VX        |                                                       | VXV, VXA                       |
|             | 긍정지정사                 | VCP     | VCP  | VCP       |                                                       | VCP                            |
|             | 부정지정사                 | VCN     | VCN  | VCN       |                                                       | VCN                            |
| 관형사      | 관형사                     | MM      | MM   | MM        | Determiner, Modifier                                  | MDT, MDN                       |
| 부사        | 일반부사                   | MAG     | MAG  | MAG       | Adverb                                                | MAG                            |
|             | 접속부사                   | MAJ     | MAJ  | MAJ       | Adverb                                                | MAC                            |
| 감탄사      | 감탄사                     | IC      | IC   | IC        | Exclamation                                           | IC                             |
| 조사        | 주격조사                   | JKS     | JKS  | JKS       | Josa                                                  | JKS                            |
|             | 보격조사                   | JKC     | JKC  | JKC       | Josa                                                  | JKC                            |
|             | 관형격조사                 | JKG     | JKG  | JKG       | Josa                                                  | JKG                            |
|             | 목적격조사                 | JKO     | JKO  | JKO       | Josa                                                  | JKO                            |
|             | 부사격조사                 | JKB     | JKB  | JKB       | Josa                                                  | JKM                            |
|             | 호격조사                   | JKV     | JKV  | JKV       | Josa                                                  | JKI                            |
|             | 인용격조사                 | JKQ     | JKQ  | JKQ       | Josa                                                  | JKQ                            |
|             | 접속조사                   | JC      | JC   | JC        | Conjunction                                           | JC                             |
|             | 보조사                     | JX      | JX   | JX        |                                                       | JX                             |
| 선어말 어미 | 선어말어미                 | EP      | EP   | EP        | PreEomi                                               | EPH, EPT,  EPP                 |
| 어말 어미   | 종결어미                   | EF      | EF   | EF        | Emoi                                                  | EFN, EFQ,  EFO, EFA,  EFI, EFR |
|             | 연결어미                   | EC      | EC   | EC        | Emoi                                                  | ECE, ECD,  ECS                 |
|             | 명사형 전성어미            | ETN     | ETN  | ETN       | Emoi                                                  | ETN                            |
|             | 관형형 전성어미            | ETM     | ETM  | ETM       | Emoi                                                  | ETD                            |
| 접두사      | 체언접두사                 | XPN     | XPN  | XPN       | VerbPrefix                                            | XPV                            |
| 접미사      | 명사파생접미사             | XSN     | XSN  | XSN       | Suffix                                                | XSN                            |
|             | 부사파생접미사             | XSM     |      |           | Suffix                                                | XSM                            |
|             | 동사파생접미사             | XSV     | XSV  | XSV       | Suffix                                                |                                |
|             | 형용사파생접미사           | XSA     | XSA  | XSA       | Suffix                                                |                                |
|             | 기타접미사                 | XSO     |      |           | Suffix                                                | XSO                            |
| 어근        | 어근                       | XR      | XR   | XR        |                                                       | XR                             |
| 부호        | 마침표, 물음표, 느낌표     | SW      | SF   | SF        | Punctuation                                           | SF                             |
|             | 쉼표, 가웃뎃점, 콜론, 빗금 | SW      | SP   | SC        | CashTagOthers                                         | SP                             |
|             | 따옴표, 괄호표, 줄표       | SW      | SS   | SSO, SSC  | CashTagOthers                                         | SS                             |
|             | 줄임표                     | SW      | SE   | SE        | CashTagOthers                                         | SE                             |
|             | 물결표, 숨김표, 빠짐표     | SW      | SO   | SY        | CashTagOthers                                         | SO                             |
|             | 기타기호                   | SW      | SW   | SY        | CashTagOthers,  Hashtag,  ScreenName,  KoreanParticle | SW                             |
| 불능        | 명사형추정범주             | UN      | NF   |           | Unknown                                               |                                |
|             | 용언추정범주               | UN      | NV   |           | Unknown                                               |                                |
|             | 분석불능범주               | UN      | NA   |           | Unknown                                               |                                |
| 기타        | 외국어                     | OL      | SL   | SL        | AlphaForeign                                          | OL                             |
|             | 한자                       | OL      | SH   | SH        | AlphaForeign                                          | OH                             |
|             | 숫자                       | SN      | SN   | SN        |                                                       | ON                             |

### `TEANAPS` 개체명 태그표
- `TEANAPS` 개체명 인식기의 개체명 태그는 총 16종으로 구분됩니다. 
- 개체명 태그의 종류 및 구분은 [정보통신단체표준(TTAS)](http://committee.tta.or.kr/data/standard_view.jsp?nowPage=32&pk_num=TTAK.KO-10.0852&nowSu=318&rn=1)을 따릅니다.

|    | 구분                    | 태그   | 설명                                                                |
|----|------------------------|------|---------------------------------------------------------------------|
| 1  | 사람(Person)            | PS   | 사람 이름                                                             |
| 2  | 분야(Study Field)       | FD   | 정치/경제/사회/과학/사회과학/의학/예술/철학 등 학문, 학파                        |
| 3  | 이론(Theory)            | TR   | 이론, 법칙, 원리, 사상, 진단법, 처방, 예술양식, 사조, 학설, 체계, 방식            |
| 4  | 인공물(Artifacts)        | AF   | 문화재, 토목/건축, 교통수단, 작품, 서적, 악기, 무기, 상품, 공연                  |
| 5  | 기관(Organization)      | OG   | 기관/단체, 업체, 회사/기업, 종파                                           |
| 6  | 장소(Location)          | LC   | 국가, 행정구역, 도시, 강, 호수, 바다, 섬, 대륙, 명소, 천체                      |
| 7  | 문명(Civilization)      | CV   | 문명, 문화, 종족, 스포츠, 도구, 제도, 언어, 양식, 음식/음료, 직업, 인간관계, 상, 법  |
| 8  | 날짜(Date)              | DT   | 기간, 절기, 날짜, 달, 년, 계절, 시대                                       |
| 9  | 시간(Time)              | TI   | 시간, 기간, 시각, 분, 초                                                 |
| 10 | 수량(Quantity)          | QT   | 수량, 나이, 크기, 넓이, 인원수, 무게, 비율, 속도, 온도, 부피, 순서, 금액, 우편번호   |
| 11 | 사건(Event)             | EV   | 사회운동, 선언, 전쟁, 혁명, 스포츠 행사, 축제, 사건/사고                         |
| 12 | 동물(Animal)            | AM   | 동물, 곤충, 조류, 어류, 포유류, 양서류, 파충류, 분류명, 신체부위                  |
| 13 | 식물(Plant)             | PT   | 꽃, 풀, 나무, 과일, 열매, 식물 유형, 식물 부위                                |
| 14 | 물질(Meterial)          | MT   | 원소, 금속, 암석, 화학물질                                                |
| 15 | 용어(Term)              | TM   | 색, 방향, 기후, 모양/형태, 증상, 약품, 용어, URL, 이메일 주소, 모델, 부품, 프로젝트  |
| 16 | 알 수 없음               | UN   | 특정 개체명 분류에 해당하지 않는 단어                                         |
