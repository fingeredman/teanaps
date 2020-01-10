# `TEANAPS` User Guide

---
## Contents
- [Install `TEANAPS`](./teanaps_user_guide-install_teanaps.md)
- [API Documentation](./teanaps_user_guide-api_documentation-handler.md)
  - [Handler](./teanaps_user_guide-api_documentation-handler.md)
  - [NLP](./teanaps_user_guide-api_documentation-nlp.md)
  - [Text Analysis](./teanaps_user_guide-api_documentation-text_analysis.md)
  - [Visualization](./teanaps_user_guide-api_documentation-visualization.md)
  - [Machine Learning](./teanaps_user_guide-api_documentation-visualization.md)
- [Tutorial](./teanaps_user_guide-tutorial.md)
- [References](./teanaps_user_guide-references_journal_project.md)
- [Journal & Project](./teanaps_user_guide-references_journal_project.md)
- [Appendix](./teanaps_user_guide-appendix.md)

---
## API Documentation

### `TEANAPS` Architecture

```python
├─teanaps  
│     │  
│     ├─ handler  
│     │     ├─ FileHandler  
│     │     ├─ MessageHandler  
│     │     └─ QueueHandler  
│     │  
│     ├─ nlp
│     │     ├─ MorphologicalAnalyzer
│     │     ├─ NamedEntityRecognizer
│     │     ├─ SyntaxAnalyzer 
│     │     ├─ Processing 
│     │     └─ Embedding 
│     │ 
│     ├─ text_analysis 
│     │     ├─ TfidfCalculator 
│     │     ├─ DocumentClustering
│     │     ├─ TopicClustering 
│     │     ├─ CoWordCalculator
│     │     ├─ SentimentAnalysis
│     │     ├─ DocumentSummarizer 
│     │     └─ KeyphraseExtraction
│     │  
│     ├─ visualization
│     │     ├─ GraphVisualizer
│     │     └─ TextVisualizer 
│     │  
│     └─ machine_learning
│           ├─ Regression
│           ├─ Classification
│           └─ Clustering
└─────────────────────────────────────────
```

### Jump to

| Package   | Class     |
|-----------|-----------|
| [handler](./teanaps_user_guide-api_documentation-handler.md#1-teanapshandler)    | [FileHandler](./teanaps_user_guide-api_documentation-handler.md#11-teanapshandlerfilehandler), [MessageHandler](./teanaps_user_guide-api_documentation-handler.md#12-teanapshandlermessagehandler), [QueueHandler](./teanaps_user_guide-api_documentation-handler.md#13-teanapshandlerqueuehandler)    |
| [nlp](./teanaps_user_guide-api_documentation-nlp.md#2-teanapsnlp)    | [MorphologicalAnalyzer](./teanaps_user_guide-api_documentation-nlp.md#21-teanapsnlpmorphologicalanalyzer), [NamedEntityRecognizer](./teanaps_user_guide-api_documentation-nlp.md#22-teanapsnlpnamedentityrecognizer), [SyntaxAnalyzer](./teanaps_user_guide-api_documentation-nlp.md#23-teanapsnlpsyntaxanalyzer), [Processing](./teanaps_user_guide-api_documentation-nlp.md#24-teanapsnlpprocessing), [Embedding](./teanaps_user_guide-api_documentation-nlp.md#25-teanapsnlpembedding)    |
| [text_analysis](./teanaps_user_guide-api_documentation-text_analysis.md#3-teanapstext_analysis)    | [TfidfCalculator](./teanaps_user_guide-api_documentation-text_analysis.md#31-teanapstext_analysistfidfcalculator), [DocumentClustering](./teanaps_user_guide-api_documentation-text_analysis.md#32-teanapstext_analysisdocumentclustering), [TopicClustering](./teanaps_user_guide-api_documentation-text_analysis.md#33-teanapstext_analysistopicclustering), [CoWordCalculator](./teanaps_user_guide-api_documentation-text_analysis.md#34-teanapstext_analysiscowordcalculator), [SentimentAnalysis](./teanaps_user_guide-api_documentation-text_analysis.md#35-teanapstext_analysissentimentanalysis), [DocumentSummarizer](./teanaps_user_guide-api_documentation-text_analysis.md#36-teanapstext_analysisdocumentsummarizer), [KeyphraseExtraction](./teanaps_user_guide-api_documentation-text_analysis.md#37-teanapstext_analysiskeyphraseextraction)    |
| [visualization](./teanaps_user_guide-api_documentation-visualization.md#4-teanapsvisualization)    | [GraphVisualizer](./teanaps_user_guide-api_documentation-visualization.md#41-teanapsvisualizationgraphvisualizer), [TextVisualizer](./teanaps_user_guide-api_documentation-visualization.md#42-teanapsvisualizationtextvisualizer)    |
| [machine_learning](./teanaps_user_guide-api_documentation-visualization.md#5-teanapsmachine_learning)    | [Regression](./teanaps_user_guide-api_documentation-visualization.md#51-teanapsmachine_learningregression), [Classification](./teanaps_user_guide-api_documentation-visualization.md#52-teanapsmachine_learningclassification), [Clustering](./teanaps_user_guide-api_documentation-visualization.md#53-teanapsmachine_learningclustering)    |

### Manual
#### 1. `teanaps.handler`
##### 1.1. `teanaps.handler.FileHandler`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.handler import FileHandler
> 
> fh = FileHandler()
> ```

- `teanaps.handler.FileHandler.save_data(file_name, data)` [[Top]](#teanaps-architecture)
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

- `teanaps.handler.FileHandler.load_data(file_name)` [[Top]](#teanaps-architecture)
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

- `teanaps.nlp.MessageHandler.send_slack_msg(message)` [[Top]](#teanaps-architecture)
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

- `teanaps.nlp.QueueHandler.add_lambda(function, parmeter_dict)` [[Top]](#teanaps-architecture)
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

- `teanaps.nlp.QueueHandler.get_result()` [[Top]](#teanaps-architecture)
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
