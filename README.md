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
> TEANAPS는 4가지 형태소분석기를 지원합니다. 한국어 형태소분석기는 MeCab/KKMA/Okt, 영어 형태소분석기는 NLTK를 사용하며 아래 코드와 같이 한국어 문장에 대해 어떤 형태소분석기를 사용할지를 지정할 수 있습니다. 형태소분석기 미지정시 Okt 형태소분석기가 기본으로 사용됩니다. 단, 지원하는 모든 형태소분석기의 형태소 태그는 통일하여 사용합니다.  

```python
sa.set_tagger("mecab") 

result = sa.parse(sentence)
print(result)
```
Output:
```python
[('자연어', 'NNG', (0, 3)), ('처리', 'NNG', (3, 5)), ('(', 'SS', (5, 6)), ('nlp', 'SL', (6, 9)), (')', 'SS', (9, 10)), ('는', 'JX', (10, 11)), ('텍스트', 'NNG', (12, 15)), ('분석', 'NNG', (16, 18)), ('을', 'JKO', (18, 19)), ('위한', 'VV+ETM', (20, 22)), ('기반', 'NNG', (23, 25)), ('기술', 'NNG', (25, 27)), ('입니다', 'VCP+EF', (28, 31)), ('.', 'SF', (31, 32))]
```

### 개체명인식 (NER Tagging)
> 개체명인식을 위한 기본코드는 아래와 같습니다. 개체명인식의 기본 입력은 형태소 단위로 구분된 문장 리스트(List)이며, 출력은 그 중 개체명으로 인식된 부분만 리스트로 반환합니다. 개체명 태그는 총 14종으로 구분됩니다.  

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
[['분석', 'CVL', (16, 18)], ['기술', 'TRM', (25, 27)]]
```
> TEANAPS에서 지원하는 개체명인식기가 지원하지 않는 개체명에 대해 아래와 같이 추가로 개체명과 개체명 태그를 추가할 수 있습니다.  

Python Code:
```python
sa.set_ner_lexicon([("자연어처리", "TRM"), ("기반기술", "NNG")])

result = sa.ner(tokenize_sentence, access_token)
print(result)
```
Output:
```python
[['자연어처리', 'TRM', (0, 5)], ['분석', 'CVL', (16, 18)], ['기반기술', 'NNG', (23, 27)], ['기술', 'TRM', (25, 27)]]
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
[['자연어처리', 'TRM', (0, 5)], ['분석', 'CVL', (16, 18)], ['기반기술', 'NNG', (23, 27)], ['기술', 'TRM', (25, 27)]]
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
