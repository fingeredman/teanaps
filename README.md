# TEANAPS: Text Analysis APIs
> Text Analysis & Natural Language Processing API Packages for Education  

> 본 자료는 텍스트 마이닝(text mining)을 보다 간단히 접근할 수 있도록 도와주는 Python 패키지 입니다. Python 언어를 배운 후에도 텍스트 마이닝을 위해서는 다양한 외부 패키지들을 활용할 줄 알아야합니다. 하지만 배워야하는 외부 패키지들이 적지않아 Python에 충분익숙하지 않으신 분들은 접근하기가 쉽지 않습니다. 본 자료는 텍스트 마이닝과 관련된 외부 패키지들을 하나로 통합하고 Google Colabotory를 활용해 설치환경을 통일하여, 텍스트 마이닝을 위한 사전작업을 최소화하고 필요한 프로그래밍 코드를 최소화 할 수 있도록 도와줍니다. 본 패키지를 활용하기 전 Python 기초문법과 텍스트 마이닝에 필요한 필수 사전지식을 먼저 공부하시기를 추천드리며, "Install"과 "Tutorial"을 참조하시어 따라해보시길 권장드립니다.

- 본 패키지는 텍스트 마이닝을 활용한 연구 및 강의를 위한 목적으로 제작되었습니다.
- 본 패키지를 강의 또는 연구 목적으로 활용하고자 하시는 경우 꼭 아래 메일주소로 연락주세요.
- 본 패키지에 대한 허가되지 않은 배포를 금지합니다.
- 강의, 저작권, 출판, 특허, 공동저자에 관련해서는 문의 바랍니다.
- **Contact : 전병진(fingeredman@gmail.com)**

---
## Install
- install.ipynb 파일을 참조해주세요.
- 링크를 통해 설치용 노트북 파일을 Google Colabotory로 열 수 있습니다. [(Link)](https://colab.research.google.com/github/fingeredman/teanaps/blob/master/install.ipynb)
- 로컬 환경에 철치가 필요하신 경우, [teanaps_install.py](https://colab.research.google.com/github/fingeredman/teanaps/blob/master/teanaps_setup.py) 파일을 참고 바랍니다.
- Windows 운영체제에서 일부 기능에 제한이 있을 수 있습니다.

---
## Tutorial
- 본 패키지를 활용한 텍스트 마이닝 강의자료를 참고해주세요. [(Link)](https://github.com/fingeredman/text-mining-for-practice)

### 형태소분석 (POS Tagging)
> 형태소분석을 위한 기본코드는 아래와 같습니다. 한국어 문장은 Okt 영어 문장은 NLTK 형태소분석기를 기본으로 사용합니다. 언어는 별도로 지정하지 않으며 입력된 문장을 보고 스스로 판단해 입력문장에 맞는 한국어/영어 형태소분석기를 선택합니다.  

Python Code:
```python
from teanaps.nlp import SyntaxAnalyzer

sentence = "자연어처리(NLP)는 텍스트 분석을 위한 기반기술 입니다."

sa = SyntaxAnalyzer()

result = sa.parse(sentence)
print(result)
```
Output:
```python
[('자연어', 'NNG', (0, 3)), ('처리', 'NNG', (3, 5)), ('(', 'SW', (5, 6)), ('nlp', 'SL', (6, 9)), (')', 'SW', (9, 10)), ('는', 'VV', (10, 11)), ('텍스트', 'NNG', (12, 15)), ('분석', 'NNG', (16, 18)), ('을', 'JC', (18, 19)), ('위', 'NNG', (20, 21)), ('한', 'JC', (21, 22)), ('기반', 'NNG', (23, 25)), ('기술', 'NNG', (25, 27)), ('입니다', 'VA', (28, 31)), ('.', 'SW', (31, 32))]
```
> TEANAPS는 4가지 형태소분석기를 지원합니다. 한국어 형태소분석기는 MeCab/KKMA/Okt, 영어 형태소분석기는 NLTK를 사용하며 아래 코드와 같이 한국어 문장에 대해 어떤 형태소분석기를 사용할지를 지정할 수 있습니다. 형태소분석기 미지정시 Okt 형태소분석기가 기본으로 사용됩니다. 단, 지원하는 모든 형태소분석기의 형태소 태그는 통일하여 사용합니다. 형태소분석기의 기본입력은 일반 문장(String)이며, 출력은 형태소, 태그, 형태소의 원문위치가 포함된 튜플(Tuple)의 리스트(List)입니다.  

```python
sa.set_tagger("mecab") 

result = sa.parse(sentence)
print(result)
```
Output:
```python
[('자연어', 'NNG', (0, 3)), ('처리', 'NNG', (3, 5)), ('(', 'SS', (5, 6)), ('nlp', 'SL', (6, 9)), (')', 'SS', (9, 10)), ('는', 'JX', (10, 11)), ('텍스트', 'NNG', (12, 15)), ('분석', 'NNG', (16, 18)), ('을', 'JKO', (18, 19)), ('위한', 'VV+ETM', (20, 22)), ('기반', 'NNG', (23, 25)), ('기술', 'NNG', (25, 27)), ('입니다', 'VCP+EF', (28, 31)), ('.', 'SF', (31, 32))]
```
> 형태소 품사태그는 세종말뭉치 품사태그를 기본으로 하여 아래와 같이 통일합니다.  

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
| 부호        | 마침표, 물음표, 느낌표     | SF      | SF   | SF        | Punctuation                                           | SF                             |
|             | 쉼표, 가웃뎃점, 콜론, 빗금 | SP      | SP   | SC        | CashTagOthers                                         | SP                             |
|             | 따옴표, 괄호표, 줄표       | SS      | SS   | SSO, SSC  | CashTagOthers                                         | SS                             |
|             | 줄임표                     | SE      | SE   | SE        | CashTagOthers                                         | SE                             |
|             | 물결표, 숨김표, 빠짐표     | SO      | SO   | SY        | CashTagOthers                                         | SO                             |
|             | 기타기호                   | SW      | SW   | SY        | CashTagOthers,  Hashtag,  ScreenName,  KoreanParticle | SW                             |
| 불능        | 명사형추정범주             | UN      | NF   |           | Unknown                                               |                                |
|             | 용언추정범주               | UN      | NV   |           | Unknown                                               |                                |
|             | 분석불능범주               | UN      | NA   |           | Unknown                                               |                                |
| 기타        | 외국어                     | OL      | SL   | SL        | AlphaForeign                                          | OL                             |
|             | 한자                       | OL      | SH   | SH        | AlphaForeign                                          | OH                             |
|             | 숫자                       | SN      | SN   | SN        |                                                       | ON                             |

### 개체명인식 (NER Tagging)
> 개체명인식을 위한 기본코드는 아래와 같습니다. 개체명인식의 기본 입력은 형태소 단위로 구분된 문장 리스트(List)이며, 출력은 그 중 개체명으로 인식된 부분만 개체명, 태그, 개체명의 원문위치가 포함된 튜플(Tuple)의 리스트(List)로 반환합니다.  

Python Code:
```python
from teanaps.nlp import SyntaxAnalyzer

tokenize_sentence = [('자연어', 'NNG', (0, 3)), ('처리', 'NNG', (3, 5)), ('(', 'SS', (5, 6)), 
                     ('nlp', 'SL', (6, 9)), (')', 'SS', (9, 10)), ('는', 'JX', (10, 11)), 
                     ('텍스트', 'NNG', (12, 15)), ('분석', 'NNG', (16, 18)), ('을', 'JKO', (18, 19)), 
                     ('위한', 'VV+ETM', (20, 22)), ('기반', 'NNG', (23, 25)), 
                     ('기술', 'NNG', (25, 27)), ('입니다', 'VCP+EF', (28, 31)), ('.', 'SF', (31, 32))
                    ]
access_token = "##########"

sa = SyntaxAnalyzer()

result = sa.ner(tokenize_sentence, access_token)
print(result)
```
Output:
```python
[('분석', 'CVL', (16, 18)), ('기술', 'TRM', (25, 27))]
```
> 개체명 태그는 총 14종으로 구분됩니다.  

|    | 구분                    | 태그 | 설명                                    |
|----|-------------------------|------|-----------------------------------------|
| 1  | 사람(Person)            | PER  | 인물명(가장인물 포함), 연예인 그룹명 등 |
| 2  | 분야(Field)             | FLD  | 학문, 이론, 법칙, 기술 등               |
| 3  | 인공물(Artifacts Works) | AFW  | 사람에 의해 생성된 대상                 |
| 4  | 기관(Organization)      | ORG  | 기관, 단체, 회의, 모임 등               |
| 5  | 장소(Location)          | LOC  | 장소, 지역, 행정구역 등                 |
| 6  | 문명(Civilization)      | CVL  | 문명, 문화 등                           |
| 7  | 날짜(Data)              | DAT  | 날짜                                    |
| 8  | 시간(Time)              | TIM  | 시간                                    |
| 9  | 숫자(Number)            | NUM  | 숫자                                    |
| 10 | 사건(Event)             | EVT  | 사건, 사고, 행사, 이벤트, 기념일        |
| 11 | 동물(Animal)            | ANM  | 사람을 제외한 동물                      |
| 12 | 식물(Plant)             | PLT  | 식물                                    |
| 13 | 물질(Meterial)          | MAT  | 금속, 암석, 화합물 등                   |
| 14 | 용어(Term)              | TRM  | 전문용어, 일반용어, 신조어 등           |
| 15 | 알 수 없음              | UNK  | 특정 개체명 분류에 해당하지 않는 단어   |
> TEANAPS에서 지원하는 개체명인식기가 지원하지 않는 개체명에 대해 아래와 같이 추가로 개체명과 개체명 태그를 추가할 수 있습니다.  

Python Code:
```python
sa.set_ner_lexicon([("자연어처리", "TRM"), ("기반기술", "NNG")])

result = sa.ner(tokenize_sentence, access_token)
print(result)
```
Output:
```python
[('자연어처리', 'TRM', (0, 5)), ('분석', 'CVL', (16, 18)), ('기반기술', 'NNG', (23, 27)), ('기술', 'TRM', (25, 27))]
```
> 개체명 사전을 별도로 구축하기 어려운 경우, 아래와 같이 문서가 저장된 텍스트 파일을 입력파일로 하여 파일 안의 개체명을 자동으로 추출해 개체명 사전에 추가할 수 있습니다.  

Python Code:
```python
path = 'teanaps/data/article_sample.txt'

sa.train_lexicon(path)

result = sa.ner(tokenize_sentence, access_token)
print(result)
```
Output:
```python
[('자연어처리', 'TRM', (0, 5)), ('분석', 'CVL', (16, 18)), ('기반기술', 'NNG', (23, 27)), ('기술', 'TRM', (25, 27))]
```
---
## Release history
> 2019.07.12. teanaps v0.0.1  
> 2019.08.21. teanaps v0.0.2  
> 2019.09.22. teanaps v0.0.3  

---
## References
- Install KoNLPy in colaboratory [(Link)](https://github.com/konlpy/konlpy/issues/188#issuecomment-383550386)  

---
## Update History
> 2019.06.12. 기본 구성 입력  
> 2019.07.12. teanaps v0.0.1 업데이트  
> 2019.08.21. teanaps v0.0.2 업데이트, install.ipynb 업로드  
> 2019.08.24. install.ipynb 업데이트  
> 2019.09.22. teanaps v0.0.3 업데이트  
