# `TEANAPS` User Guide

---
## Contents
- [Install `TEANAPS`](./teanaps_user_guide-install_teanaps.md)
- [API Documents](./teanaps_user_guide-api_documents.md)
- [Tutorial](./teanaps_user_guide-tutorial.md)
- [References](./teanaps_user_guide-references_journal_project.md)
- [Journal & Project](./teanaps_user_guide-references_journal_project.md)
- [Appendix](./teanaps_user_guide-appendix.md)

---
## API Documents

### `TEANAPS` Architecture
[FileHandler](#1-teanapshandler)
[FileHandler](https://github.com/fingeredman/teanaps/blob/master/document/teanaps_user_guide-api_documents.md#1-teanapshandler)
> ```
> teanaps
>      ∟ handler
>             ∟ FileHandler
>             ∟ MessageHandler
>             ∟ QueueHandler
>      ∟ nlp
>             ∟ MorphologicalAnalyzer
>             ∟ NamedEntityRecognizer
>             ∟ SyntaxAnalyzer
>             ∟ Processing.py
>      ∟ text_analysis
>             ∟ TfidfCalculator
>             ∟ DocumentClustering
>             ∟ TopicClustering
>             ∟ CoWordCalculator
>             ∟ SentimentAnalysis
>             ∟ DocumentSummarizer
>             ∟ KeyphraseExtraction
>      ∟ visualization
>             ∟ GraphVisualizer
>             ∟ TextVisualizer
>      ∟ machine_learning
>             ∟ Regression
>             ∟ Classification
>             ∟ Clustering
> ```

### Methods
#### 1. `teanaps.handler`
##### 1.1. `teanaps.handler.FileHandler`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.handler import FileHandler
> 
> fh = FileHandler()
> ```

- `teanaps.handler.FileHandler.fh.save_data(file_name, data)`
  - 데이터(변수, Pandas Dataframe 등)을 바이너리 파일로 저장합니다.
  - Parameters
    - *file_name (str) : 저장할 파일 경로 및 파일명. 최대 128자.*
    - *data (all) : 저장할 데이터가 저장된 변수명.*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > from sklearn.datasets import fetch_california_housing
    > import pandas as pd
    > 
    > data = fetch_california_housing()
    > df = pd.DataFrame(data['data'], columns = data['feature_names'])
    > fh.save_data("california_housing", df)
    > ```

- `teanaps.handler.FileHandler.fh.load_data(file_name)`
  - 데이터(변수, Pandas Dataframe 등)가 저장된 바이너리 파일을 불러와 그 결과를 반환합니다.
  - Parameters
    - *file_name (str) : 저장할 파일 경로 및 파일명. 최대 128자.*
  - Returns
    - *data (all) : 저장할 데이터가 저장된 변수명.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > #from sklearn.datasets import fetch_california_housing
    > #import pandas as pd
    > 
    > #data = fetch_california_housing()
    > #df = pd.DataFrame(data['data'], columns = data['feature_names'])
    > #fh.save_data("california_housing", df)
    > df = fh.load_data("california_housing")
    > print(type(df))
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > pandas.core.frame.DataFrame
    > ```

##### 1.2. `teanaps.handler.MessageHandler`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.handler import MessageHandler
> 
> webhook_url = "https://hooks.slack.com/services/TNLDWA5B7/BNNKYJ7JS/GZ0~"
> mh = MessageHandler(webhook_url)
> ```

> Notes :  
> - `MessageHandler`는 `Slack` 메신저를 통해 메시지를 발송합니다.
> - `webhook_url`은 `Slack` 회원가입 후 [Slack API Webhook URL](https://api.slack.com/messaging/webhooks) 페이지에서 발급 가능합니다.

- `teanaps.nlp.MessageHandler.send_slack_msg(message)`
  - `Webhook URL`에 연결된 `Slack`으로 메시지를 발송합니다.
  - Parameters
    - *message (str) : 한국어 또는 영어로 구성된 문장.*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > message = "슬랙으로 메시지를 발송합니다."
    > mh.send_slack_msg(message)
    > ```

##### 1.3. `teanaps.handler.QueueHandler`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.handler import QueueHandler
> 
> thread_count = 3
> qh = QueueHandler(thread_count)
> ```

> Notes :  
> - `QueueHandler`는 `thread_count`의 수 만큼 요청된 함수를 동시에 순차적으로 처리합니다.

- `teanaps.nlp.QueueHandler.add_lambda(function, parmeter_dict)`
  - 수행할 작업들이 저장된 큐 (Queue)에 작업을 추가합니다.`Webhook URL`에 연결된 `Slack`으로 메시지를 발송합니다.
  - Parameters
    - *function (function) : 특정 작업을 수행하는 함수.*
    - *parmeter_dict (dict) : `function` 함수의 입력변수를 포함하는 딕셔너리.*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > import time
    > 
    > def sample_function(parmeter_dict):
    >     print_list = parmeter_dict["print_list"]
    >     for i in print_list:
    >         print(i, end="")
    >         time.sleep(1)
    >     result = {
    >         "request_id": parmeter_dict["request_id"], 
    >         "result": "complete."
    >     }
    >     return result
    > 
    > for i in range(3):
    >     parmeter_dict = {
    >         "request_id" : i,
    >         "print_list": ["a", "b", "c", "d"]
    >     }
    >     qh.add_lambda(sample_function, parmeter_dict)
    > ```
	> Output (in Jupyter Notebook) :
    > ```python
    > aaabbbcccddd
    > done : 2 lamda left.
    > 
    > done : 1 lamda left.
    > 
    > done : 0 lamda left.
    > ```

- `teanaps.nlp.QueueHandler.get_result()`
  - 수행할 작업들이 저장된 큐 (Queue)에 작업을 추가합니다.`Webhook URL`에 연결된 `Slack`으로 메시지를 발송합니다.
  - Parameters
    - *None*
  - Returns
    - *result_dict (dict) : 큐에서 수행된 작업에서 반환한 값을 포함하는 딕셔너리.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > #for i in range(3):
    > #    parmeter_dict = {
    > #        "request_id" : i,
    > #        "print_list": ["a", "b", "c", "d"]
    > #    }
    > #    qh.add_lambda(sample_function, parmeter_dict)
    >
    > result = qh.get_result()
    > print(result)
    > ```
	> Output (in Jupyter Notebook) :
    > ```python
    > {1: 'complete.', 2: 'complete.', 0: 'complete.'}
    > ```

#### 2. `teanaps.nlp`
##### 2.1. `teanaps.nlp.MorphologicalAnalyzer`  

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.nlp import MorphologicalAnalyzer
>
> ma = MorphologicalAnalyzer()
> ```

> Notes :  
> - import시 최초 1회 경고메시지 (Warnning)가 출력될 수 있습니다. 무시하셔도 좋습니다.

- `teanaps.nlp.MorphologicalAnalyzer.parse(sentence)`
  - 문장을 형태소 분석하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *result (list) : (형태소, 품사, 단어위치) 구조의 Tuple을 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > result = ma.parse(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > [('teanaps', 'OL', (0, 7)), ('는', 'JX', (7, 8)), ('텍스트', 'NNG', (9, 12)), ('마이닝', 'NNP', (13, 16)), ('을', 'JKO', (16, 17)), ('위한', 'VV+ETM', (18, 20)), ('python', 'OL', (21, 27)), ('패키지', 'NNG', (28, 31)), ('입니다', 'VCP+EF', (32, 35)), ('.', 'SW', (35, 36))]
    > ```

- `teanaps.nlp.MorphologicalAnalyzer.set_tagger(tagger)`
  - 형태소 분석기를 선택합니다. 형태소 분석기는 `MeCab`, `Okt (Twitter)`, `Kkma`, `NLTK` 총 4가지를 지원합니다. 형태소 분석기를 선택하지 않으면 기본으로 한국어는 `OKt`, 영어는 `NLTK` 형태소 분석기를 사용합니다.
  - Parameters
    - *tagger (str) : 형태소 분석기 {"okt", mecab", "kkma"} 중 하나 입력*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > ma.set_tagger("okt")
    > # or ma.set_tagger("mecab")
    > # or ma.set_tagger("kkma")
    > ```

##### 2.2. `teanaps.nlp.NamedEntityRecognizer `

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.nlp import NamedEntityRecognizer
>
> ner = NamedEntityRecognizer(model_path="/model")
> ```

> Notes :  
> - 모델 파일을 별도로 [다운로드](https://drive.google.com/open?id=1qZ5qttjvRhHiQesECRQc6JgB4_kAcVBr)하여 파일 경로를 `model_path` 변수에 포함해야합니다.
> - import시 최초 1회 경고메시지 (Warnning)가 출력될 수 있습니다. 무시하셔도 좋습니다.

- `teanaps.nlp.NamedEntityRecognizer.parse(sentence)`
  - 문장에서 개체명을 인식하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *result (list) : (개체명, 개체명 태그, 개체명위치) 구조의 Tuple을 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > result = ner.parse(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > [('teanaps', 'ORG', (0, 7)), ('python', 'CVL', (0, 27))]
    > ```

    > Notes :  
    > - `TEANAPS`의 개체명 태그는 [총 16종](http://)으로 구분됩니다. 태그 종류 및 구분은 [정보통신단체표준(TTAS)](http://committee.tta.or.kr/data/standard_view.jsp?nowPage=32&pk_num=TTAK.KO-10.0852&nowSu=318&rn=1)을 따릅니다.

- `teanaps.nlp.NamedEntityRecognizer.parse_sentence(sentence)`
  - 문장에서 개체명을 인식하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *result (str) : 표준 개체명 태그 형식으로 개체명 태깅된 문장.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > result = ner.parse_sentence(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > "<TEANAPS:ORG>는 텍스트 마이닝을 위한 <python:CVL> 패키지 입니다."
    > ```

- `teanaps.nlp.NamedEntityRecognizer.draw_weight(sentence)`
  - 문장에서 개체로 인식된 형태소에 대한 가중치를 히스토그램으로 출력합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *plotly graph (graph object) : 문장에서 개체로 인식된 부분에 대한 가중치 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > result = ner.draw_weight(sentence)
    > ```
    > Output (in Jupyter Notebook) :  
    > ![sentence_weight_histogram](../data/sample_image/sentence_weight_histogram.png)

- `teanaps.nlp.NamedEntityRecognizer.draw_sentence_weight(sentence)`
  - 문장에서 개체로 인식된 형태소에 대한 가중치를 text attention 그래프로 출력합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *plotly graph (graph object) : 문장에서 개체로 인식된 부분에 대한 가중치 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > result = ner.draw_weight(sentence)
    > ```
    > Output (in Jupyter Notebook) :  
    > ![sentence_weight](../data/sample_image/sentence_weight.png)

##### 2.3. `teanaps.nlp.SyntaxAnalyzer`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.nlp import SyntaxAnalyzer
>
> sa = SyntaxAnalyzer()
> ```

> Notes :  
> - import시 최초 1회 경고메시지 (Warnning)가 출력될 수 있습니다. 무시하셔도 좋습니다.

- `teanaps.nlp.SyntaxAnalyzer.parse(ma_result, ner_result)`
  - 형태소 분석과 개체명 인식 결과를 바탕으로 문장 구조를 파악하고 그 결과를 반환합니다.
  - Parameters
    - *ma_result (list) : (형태소, 품사, 단어위치) 구조의 Tuple을 포함하는 리스트. `teanaps.nlp.ma.parse`참고.*
    - *ner_result (list) : (개체명, 개체명 태그, 개체명위치) 구조의 Tuple을 포함하는 리스트. `teanaps.nlp.ner.parse`참고.*
  - Returns
    - *result (list) : (형태소, 개체명, 개체명 태그, 개체명위치) 구조의 Tuple을 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > #sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > #ma_result = [('teanaps', 'OL', (0, 7)), ('는', 'JX', (7, 8)), ('텍스트', 'NNG', (9, 12)), ('마이닝', 'NNP', (13, 16)), ('을', 'JKO', (16, 17)), ('위한', 'VV+ETM', (18, 20)), ('python', 'OL', (21, 27)), ('패키지', 'NNG', (28, 31)), ('입니다', 'VCP+EF', (32, 35)), ('.', 'SW', (35, 36))]
    > #ner_result = [('teanaps', 'ORG', (0, 7)), ('python', 'CVL', (0, 27))]
    > result = sa.syntax(ma_result, ner_result)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > [('teanaps', 'NNP', 'ORG', (0, 7)), ('는', 'JX', 'UNK', (7, 8)), ('텍스트', 'NNG', 'UNK', (9, 12)), ('마이닝', 'NNP', 'UNK', (13, 16)), ('을', 'JKO', 'UNK', (16, 17)), ('위한', 'VV+ETM', 'UNK', (18, 20)), ('python', 'NNP', 'CVL', (0, 27)), ('패키지', 'NNG', 'UNK', (28, 31)), ('입니다', 'VCP+EF', 'UNK', (32, 35)), ('.', 'SW', 'UNK', (35, 36))]
    > ```

- `teanaps.nlp.SyntaxAnalyzer.get_sentence_tree(sentence, sa_result)`
  - 형태소 분석과 개체명 인식 결과를 바탕으로 문장 구조를 트리 구조로 생성하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
    - *sa_result (list) : (형태소, 개체명, 개체명 태그, 개체명위치) 구조의 Tuple을 포함하는 리스트. `teanaps.nlp.sa.parse`참고.*
  - Returns
    - *label_list (list) : 트리구조 문장의 각 인덱스에 해당하는 라벨을 포함하는 리스트.*
    - *edge_list (list) : 트리구조 문장의 각 라벨 인덱스 간의 연결된 엣지를 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > #sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > #sa_result = [('teanaps', 'NNP', 'ORG', (0, 7)), ('는', 'JX', 'UNK', (7, 8)), ('텍스트', 'NNG', 'UNK', (9, 12)), ('마이닝', 'NNP', 'UNK', (13, 16)), ('을', 'JKO', 'UNK', (16, 17)), ('위한', 'VV+ETM', 'UNK', (18, 20)), ('python', 'NNP', 'CVL', (0, 27)), ('패키지', 'NNG', 'UNK', (28, 31)), ('입니다', 'VCP+EF', 'UNK', (32, 35)), ('.', 'SW', 'UNK', (35, 36))]
    > label_list, edge_list = sa.get_sentence_tree(sentence, sa_result)
    > print(label_list)
    > print(edge_list)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > ['TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다.<br>/SENTENCE', 'TEANAPS는 텍스<br>/SUBJECT', ' 마이닝을 위<br>/OBJECT', ' Python 패키지 <br>/EF', 'TEANA<br>/N', 'P<br>/S', 'S는 <br>/N', '텍<br>/S', '스<br>/J', ' 마이닝을 <br>/N', '위<br>/J', ' P<br>/V', 'thon<br>/N', '패키지 <br>/S', '자연어<br>/NNG<br>/UNK', '처리<br>/NNG<br>/UNK', '(<br>/SW<br>/UNK', 'NLP<br>/NNP<br>/TRM', ')<br>/SW<br>/UNK', '는<br>/JX<br>/UNK', '텍스트<br>/NNG<br>/UNK', '분석<br>/NNG<br>/UNK', '을<br>/JKO<br>/UNK', '위한<br>/VV+ETM<br>/UNK', '기반<br>/NNG<br>/UNK', '기술<br>/NNG<br>/UNK', '입니다<br>/VCP+EF<br>/UNK', '.<br>/SW<br>/UNK']
    > [(0, 1), (1, 4), (4, 14), (4, 15), (1, 5), (5, 16), (1, 6), (6, 17), (1, 7), (7, 18), (1, 8), (8, 19), (0, 2), (2, 9), (9, 20), (9, 21), (2, 10), (10, 22), (0, 3), (3, 11), (11, 23), (3, 12), (12, 24), (12, 25), (3, 13), (13, 26), (13, 27)]
    > ```

- `teanaps.nlp.SyntaxAnalyzer.draw_sentence_tree(sentence, label_list, edge_list)`
  - 형태소 분석과 개체명 인식 결과를 바탕으로 생성된 트리 구조의 문장을 트리 그래프로 출력합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
    - *label_list (list) : 트리구조 문장의 각 인덱스에 해당하는 라벨을 포함하는 리스트. `teanaps.nlp.sa.get_sentence_tree`참고.*
    - *edge_list (list) : 트리구조 문장의 각 라벨 인덱스 간의 연결된 엣지를 포함하는 리스트. `teanaps.nlp.sa.get_sentence_tree`참고.*
  - Returns
    - *plotly graph (graph object) : 트리구조 문장에 대한 트리 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > #sentence = "TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다."
    > #label_list = ['TEANAPS는 텍스트 마이닝을 위한 Python 패키지 입니다.<br>/SENTENCE', 'TEANAPS는 텍스<br>/SUBJECT', ' 마이닝을 위<br>/OBJECT', ' Python 패키지 <br>/EF', 'TEANA<br>/N', 'P<br>/S', 'S는 <br>/N', '텍<br>/S', '스<br>/J', ' 마이닝을 <br>/N', '위<br>/J', ' P<br>/V', 'thon<br>/N', '패키지 <br>/S', '자연어<br>/NNG<br>/UNK', '처리<br>/NNG<br>/UNK', '(<br>/SW<br>/UNK', 'NLP<br>/NNP<br>/TRM', ')<br>/SW<br>/UNK', '는<br>/JX<br>/UNK', '텍스트<br>/NNG<br>/UNK', '분석<br>/NNG<br>/UNK', '을<br>/JKO<br>/UNK', '위한<br>/VV+ETM<br>/UNK', '기반<br>/NNG<br>/UNK', '기술<br>/NNG<br>/UNK', '입니다<br>/VCP+EF<br>/UNK', '.<br>/SW<br>/UNK']
    > #edge_list = [(0, 1), (1, 4), (4, 14), (4, 15), (1, 5), (5, 16), (1, 6), (6, 17), (1, 7), (7, 18), (1, 8), (8, 19), (0, 2), (2, 9), (9, 20), (9, 21), (2, 10), (10, 22), (0, 3), (3, 11), (11, 23), (3, 12), (12, 24), (12, 25), (3, 13), (13, 26), (13, 27)]
    > sa.draw_sentence_tree(sentence, label_list, edge_list)
    > ```
    > Output (in Jupyter Notebook) :  
    > ![sentence_tree](../data/sample_image/sentence_tree.png)

##### 2.4. `teanaps.nlp.Processing` (pre-processing)

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.nlp import Processing
>
> pro = Processing()
> ```

> Notes :  
> - import시 최초 1회 경고메시지 (Warnning)가 출력될 수 있습니다. 무시하셔도 좋습니다.

- `teanaps.nlp.Processing.get_stopword()`
  - `TEANAPS`에서 기본으로 제공하는 불용어를 호출하고 그 결과를 반환합니다.
  - Parameters
    - *None*
  - Returns
    - *result (list) : 불용어를 모두 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이']
    > ```

- `teanaps.nlp.Processing.add_stopword(word/word_list)`
  - `TEANAPS`에서 기본으로 제공하는 불용어 리스트에 임의의 불용어 또는 불용어 리스트를 추가합니다.
  - Parameters
    - *word/word_list (str/list) : 불용어 또는 불용어를 포함하는 리스트*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.add_stopword("가")
    >
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > #['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이']
    > ['ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이', '가']
    > ```

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.add_stopword(["으로", "로서", "때문에"])
    >
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > #['ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이', '가']
    > ['ㅡ', 'ㅣ', '', '은', '는', '이', '가', '으로', '로서', '때문에']
    > ```

- `teanaps.nlp.Processing.remove_stopword(word/word_list)`
  - 전체 불용어 리스트에서 불용어 또는 불용어 리스트를 모두 삭제합니다.
  - Parameters
    - *word/word_list (str/list) : 불용어 또는 불용어를 포함하는 리스트*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.remove_stopword("때문에")
    >
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > #['ㅡ', 'ㅣ', '', '은', '는', '이', '가', '으로', '로서', '때문에']
    > ['ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이', '가', '으로', '로서']
    > ```

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.remove_stopword(["은", "는", "이", "가"])
    >
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > #['ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이', '가', '으로', '로서']
    > ['ㅖ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '', '으로', '로서']
    > ```

- `teanaps.nlp.Processing.clear_stopword()`
  - 전체 불용어 리스트에서 불용어 또는 불용어 리스트를 모두 삭제합니다.
  - Parameters
    - *None*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.clear_stopword()
    >
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > #['ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이', '가', '으로', '로서']
    > []
    > ```

- `teanaps.nlp.Processing.set_org_stopword()`
  - 불용어 리스트를 `TEANAPS`에서 기본으로 제공하는 불용어 리스트로 초기화합니다.
  - Parameters
    - *None*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.set_org_stopword()
    >
    > result = pro.get_stopword()
    > print(result[-10:])
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > #[]
    > ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', '', '은', '는', '이']
    > ```

- `teanaps.nlp.Processing.is_stopword(word)`
  - 단어가 불용어 리스트에 포함되어있는지 여부를 확인하고 그 결과를 반환합니다.
  - Parameters
    - *word (str) : 불용어*
  - Returns
    - *result (bool) : 불용어 포함여부. True or False*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > result = pro.is_stopword("은")
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > True
    > ```

    > Python Code (in Jupyter Notebook) :
    > ```python
    > result = pro.is_stopword("없는단어")
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > False
    > ```

- `teanaps.nlp.Processing.start_timer()`
  - 타이머를 초기화하고 다시 시작합니다.
  - Parameters
    - *None*
  - Returns
    - *None*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > pro.start_timer()
    > ```

- `teanaps.nlp.Processing.lab_timer()`
  - 타이머 랩타임을 기록하고 그 결과를 반환합니다.
  - Parameters
    - *None*
  - Returns
    - *result (list) : (랩, 랩타임) 구조의 Tuple을 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > import time
    >
    > #pro.start_timer()
    > 
    > time.sleep(1)
    > result = pro.lab_timer()
    > print(result)
    > 
    > time.sleep(2)
    > result = pro.lab_timer()
    > print(result)
    > ```

    > Output (in Jupyter Notebook) :
    > ```python
    > [(1, 1.0033)]
    > [(1, 1.0033), (2, 3.0068)]
    > ```

- `teanaps.nlp.Processing.get_spacing(sentence)`
  - 문장의 띄어쓰기 오류를 보정하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *result (str) : 띄어쓰기 오류가 보정된 문장.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "TEANAPS는텍스트마이닝을위한Python패키지입니다."
    > result = pro.get_spacing(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > TEANAPS는 텍스트마이닝을 위한 Python 패키지입니다.
    > ```

<!--
- `teanaps.nlp.Processing.get_token_position(sentence_org, word_tagged_pos_list)`
-->

<!--
- `teanaps.nlp.Processing.language_detector(sentence)`
-->

<!--
- `teanaps.nlp.Processing.iteration_remover(sentence)`
-->

<!--
- `teanaps.nlp.Processing.get_plain_text(sentence, pos_list=[], word_index=0, pos_index=1, tag_index=1, tag=True)`
-->

- `teanaps.nlp.Processing.replacer(sentence)`
  - 문장에서 축약된 표현을 찾아 원래의 표현으로 수정하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *result (str) : 축약된 표현이 수정된 문장.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "If it is to be, it's up to me."
    > result = pro.replacer(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > If it is to be, it is up to me.
    > ```

<!--
##### 2.5. `teanaps.nlp.Embedding`
-->
#### 3. `teanaps.text_analysis`
##### 3.1. `teanaps.text_analysis.TfidfCalculator`
##### 3.1. `teanaps.text_analysis.DocumentClustering`
##### 3.1. `teanaps.text_analysis.TopicClustering`
##### 3.1. `teanaps.text_analysis.CoWordCalculator`
##### 3.1. `teanaps.text_analysis.SentimentAnalysis`
##### 3.1. `teanaps.text_analysis.DocumentSummarizer`
##### 3.1. `teanaps.text_analysis.KeyphraseExtraction`
#### 4. `teanaps.visualization`
##### 4.1. `teanaps.visualization.GraphVisualizer`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.vis import GraphVisualizer
>
> gv = GraphVisualizer()
> ```

- `teanaps.visualization.GraphVisualizer.draw_histogram(self, data_meta_list, graph_meta)`
  - 입력된 그래프 메타정보를 바탕으로 생성된 히스토그램 그래프를 출력합니다.
  - Parameters
    - *data_meta_list (list) : 그래프에 표현할 데이터 딕셔너리를 포함하는 리스트. Examples 참고.*
    - *graph_meta (dict) : 그래프 속성을 정의한 딕셔너리. Examples 참고.*
  - Returns
    - *plotly graph (graph object) : 히스토그램 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > x = ["a", "b", "c", "d", "e", "f"]
    > y = [1, 2, 3, 4, 5, 6]
    > z = [4, 6, 3, 4, 2, 9]
    > 
    > data_meta_list = []
    > 
    > data_meta = {
    >     "graph_type": "histogram",
    >     "data_name": "Y",
    >     "x_data": x,
    >     "y_data": y,
    >     "y_axis": "y1",
    > }
    > data_meta_list.append(data_meta)
    > 
    > data_meta = {
    >     "graph_type": "histogram",
    >     "data_name": "Z",
    >     "x_data": x,
    >     "y_data": z,
    >     "y_axis": "y1"
    > }
    > data_meta_list.append(data_meta)
    > 
    > graph_meta = {
    >     "title": "HISTOGRAM",
    >     "x_tickangle": 0,
    >     "y1_tickangle": 0,
    >     "y2_tickangle": 0,
    >     "x_name": "X",
    >     "y1_name": "Y1",
    >     "y2_name": "Y2",
    > }
    > 
    > gv.draw_histogram(data_meta_list, graph_meta)
    > ```
    > Output (in Jupyter Notebook) :
    > ![histogram](../data/sample_image/histogram.png)

- `teanaps.visualization.GraphVisualizer.draw_line_graph(self, data_meta_list, graph_meta)`
  - 입력된 그래프 메타정보를 바탕으로 생성된 라인 그래프를 출력합니다.
  - Parameters
    - *data_meta_list (list) : 그래프에 표현할 데이터 딕셔너리를 포함하는 리스트. Examples 참고.*
    - *graph_meta (dict) : 그래프 속성을 정의한 딕셔너리. Examples 참고.*
  - Returns
    - *plotly graph (graph object) : 라인 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > x = ["a", "b", "c", "d", "e", "f"]
    > y = [1, 2, 3, 4, 5, 6]
    > z = [4, 6, 3, 4, 2, 9]
    > 
    > data_meta_list = []
    > 
    > data_meta = {
    >     "graph_type": "scatter",
    >     "data_name": "Y",
    >     "x_data": x,
    >     "y_data": y,
    >     "y_axis": "y1",
    > }
    > data_meta_list.append(data_meta)
    > 
    > data_meta = {
    >     "graph_type": "scatter",
    >     "data_name": "Z",
    >     "x_data": x,
    >     "y_data": z,
    >     "y_axis": "y2"
    > }
    > data_meta_list.append(data_meta)
    > 
    > graph_meta = {
    >     "title": "LINE GRAPH",
    >     "x_tickangle": 0,
    >     "y1_tickangle": 0,
    >     "y2_tickangle": 0,
    >     "x_name": "X",
    >     "y1_name": "Y1",
    >     "y2_name": "Y2",
    > }
    > 
    > gv.draw_line_graph(data_meta_list, graph_meta)
    > ```
    > Output (in Jupyter Notebook) :
    > ![line_graph](../data/sample_image/line_graph.png)

- `teanaps.visualization.GraphVisualizer.draw_matrix(self, data_meta_list, graph_meta)`
  - 입력된 그래프 메타정보를 바탕으로 생성된 매트릭스 그래프를 출력합니다.
  - Parameters
    - *data_meta (dict) : 그래프에 표현할 데이터 딕셔너리. Examples 참고.*
    - *graph_meta (dict) : 그래프 속성을 정의한 딕셔너리. Examples 참고.*
  - Returns
    - *plotly graph (graph object) : 매트릭스 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > x = ["A", "B", "C", "D", "E", "F"]
    > y = ["AA", "BB", "CC", "DD", "EE", "FF"]
    > x_data = []
    > y_data = []
    > z_data = []
    > for x_index in range(len(x)):
    >     for y_index in range(len(y)):
    >         x_data.append(x[x_index])
    >         y_data.append(y[y_index])
    >         z_data.append(x_index/2 + y_index)
    > 
    > data_meta = {
    >     "colorbar_title": "Z RANGE",
    >     "x_data": x_data,
    >     "y_data": y_data,
    >     "z_data": z_data
    > }
    > 
    > graph_meta = {
    >     "title": "MATRIX",
    >     "height": 1000, 
    >     "width": 1000,
    >     "y_tickangle": 0,
    >     "y_name": "Y",
    >     "x_tickangle": 0,
    >     "x_name": "X",
    > }
    > 
    > gv.draw_matrix(data_meta, graph_meta)
    > ```
    > Output (in Jupyter Notebook) :
    > ![matrix](../data/sample_image/matrix.png)

- `teanaps.visualization.GraphVisualizer.draw_scatter(self, data_meta_list, graph_meta)`
  - 입력된 그래프 메타정보를 바탕으로 생성된 산점도 그래프를 출력합니다.
  - Parameters
    - *data_meta_list (list) : 그래프에 표현할 데이터 딕셔너리를 포함하는 리스트. Examples 참고.*
    - *graph_meta (dict) : 그래프 속성을 정의한 딕셔너리. Examples 참고.*
  - Returns
    - *plotly graph (graph object) : 산점도 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > x1 = [1, 2, 3, 4, -5, 6]
    > y1 = [-4, 6, 3, 4, 2, 9]
    > label1 = ["a", "b", "c", "d", "e", "f"]
    > 
    > x2 = [6, 7, 2, -4, 5, 2]
    > y2 = [1, 3, 5, 2, -7, 9]
    > label2 = ["A", "B", "C", "D", "E", "F"]
    > 
    > data_meta_list = []
    > 
    > data_meta = {
    >     "data_name": "COORDINATES1",
    >     "x_data": x1,
    >     "y_data": y1,
    >     "label": label1
    > }
    > data_meta_list.append(data_meta)
    > 
    > data_meta = {
    >     "data_name": "COORDINATES2",
    >     "x_data": x2,
    >     "y_data": y2,
    >     "label": label2
    > }
    > data_meta_list.append(data_meta)
    > 
    > graph_meta = {
    >     "title": "SCATTER",
    >     "x_name": "X",
    >     "y_name": "Y"
    > }
    > 
    > gv.draw_scatter(data_meta_list, graph_meta)
    > ```
    > Output (in Jupyter Notebook) :
    > ![scatter](../data/sample_image/scatter.png)

##### 4.2. `teanaps.visualization.TextVisualizer`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.vis import TextVisualizer
>
> gv = TextVisualizer()
> ```

- `teanaps.visualization.Textisualizer.draw_sentence_attention(token_list, weight_list)`
  - 형태소 단위로 분리된 문장과 각 형태소별 가중치를 바탕으로 문장의 특정 부분을 하이라이트한 형태의 문장 그래프를 출력합니다.
  - Parameters
    - *token_list (list) : 형태소 단위로 분리된 문장의 각 형태소를 포함하는 리스트.*
    - *weight_list (list) : 형태소 단위로 분리된 문장의 각 형태소에 해당하는 가중치를 포함하는 리스트.*
  - Returns
    - *plotly graph (graph object) : 문장 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "문장에서 중요한 부분을 음영으로 강조하여 표현하기 위해 사용됩니다."
    > token_list = sentence.split(" ")
    > #token_list = ['문장에서', '중요한', '부분을', "음영으로", '강조하여', '표현하기', '위해', '사용됩니다.']
    > weight_list = [1, 5, 2, 1, 4, 2, 1, 1]
    > 
    > tv.draw_sentence_attention(token_list, weight_list)
    > ```
    > Output (in Jupyter Notebook) :
    > ![sentence_attention](../data/sample_image/sentence_attention.png)

- `teanaps.visualization.Textisualizer.draw_wordcloud(data_meta, graph_meta)`
  - 단어와 그 가중치를 바탕으로 생성된 워드클라우드 이미지를 출력합니다.
  - Parameters
    - *data_meta (dict) : 그래프에 표현할 데이터 딕셔너리. Examples 참고.*
    - *graph_meta (dict) : 그래프 속성을 정의한 딕셔너리. Examples 참고.*
  - Returns
    - *figure (matplotlib.pyplot.plt) : 워드클리우드.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > tf = {
    >     "TEANAPS": 10,
    >     "teanaps.com": 4,
    >     "fingeredman": 2,
    >     "텍스트마이닝": 3,
    >     "자연어처리": 4,
    >     "감성분석": 1,
    >     "단어빈도": 1,
    >     "TFIDF": 1,
    >     "요약": 1,
    >     "단어네트워크": 1,
    >     "형태소분석": 1,
    >     "개체명인식": 1,
    >     "구문분석": 1
    > }
    > 
    > data_meta = {
    >     "weight_dict": tf,
    > }
    > 
    > graph_meta = {
    >     "height": 1000, 
    >     "width": 1000,
    >     "min_font_size": 10,
    >     "max_font_size": 500,
    >     "margin": 10,
    >     "background_color": "white"
    > }
    > 
    > tv.draw_wordcloud(data_meta, graph_meta)
    > ```
    > Output (in Jupyter Notebook) :
    > ![wordcloud](../data/sample_image/wordcloud.png)

- `teanaps.visualization.Textisualizer.draw_network(data_meta, graph_meta)`
  - 단어와 그 가중치, 그리고 순서쌍을 바탕으로 생성된 네트워크 이미지를 출력합니다.
  - Parameters
    - *data_meta (dict) : 그래프에 표현할 데이터 딕셔너리. Examples 참고.*
    - *graph_meta (dict) : 그래프 속성을 정의한 딕셔너리. Examples 참고.*
  - Returns
    - *plotly graph (graph object) : 네트워크 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > data_meta = {
    >     "node_list": ["a", "b", "c", "d", "e", "f"],
    >     "edge_list": [("a", "b", None), ("c", "d", None), ("a", "c", None), ("b", "d", None),
    >                   ("a", "f", None), ("a", "e", None), ("e", "d", None), ("d", "f", None)],
    >     "weight_dict": {
    >         "a": 4,
    >         "b": 2,
    >         "c": 2,
    >         "d": 3,
    >         "e": 2,
    >         "f": 2
    >     }
    > }
    > 
    > graph_meta = {
    >     "title": "WORD NETWORK",
    >     "height": 1000, 
    >     "width": 1000,
    >     "weight_name": "Weight",
    > }
    > 
    > tv.draw_network(data_meta, graph_meta)
    > ```
    > Output (in Jupyter Notebook) :
    > ![network](../data/sample_image/network.png)

<!--
#### 5. `teanaps.machine_learning`
##### 5.1. `teanaps.machine_learning.Regression`
##### 5.2. `teanaps.machine_learning.Classification`
##### 5.3. `teanaps.machine_learning.Clustering`
-->
