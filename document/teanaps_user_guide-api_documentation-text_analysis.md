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
#### 3. `teanaps.text_analysis`
##### 3.1. `teanaps.text_analysis.TfidfCalculator`
  - TBU

##### 3.2. `teanaps.text_analysis.DocumentClustering`
  - TBU

##### 3.3. `teanaps.text_analysis.TopicClustering`
  - TBU

##### 3.4. `teanaps.text_analysis.CoWordCalculator`
  - TBU

##### 3.5. `teanaps.text_analysis.SentimentAnalysis`

> Python Code (in Jupyter Notebook) :
> ```python
> from teanaps.text_analysis import SentimentAnalysis
>
> senti = SentimentAnalysis(model_path="/model", kobert_path="/kobert")
> ```

> Notes :  
> - 모델과 KoBERT 파일을 별도로 다운로드([모델](https://drive.google.com/file/d/11zkNQ0i9MUlqWVG_y7Ynrpt1yv5jabsx/view?usp=sharing)/[KoBERT](https://drive.google.com/file/d/11RBCiWkNblT26qAASvYTA4MmkwuE5gGe/view?usp=sharing))하여 파일 경로를 각각 `model_path`, `kobert_path` 변수에 포함해야합니다.

- `teanaps.text_analysis.SentimentAnalysis.tag(self, sentence, neutral_th=0.5)` [[Top]](#teanaps-architecture)
  - 문장의 감성수준을 긍정 또는 부정으로 분류하고 그 결과를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
    - *neutral_th (float) : 긍정 또는 부정의 강도 차이에서 중립으로 판단하는 범위. 0~1.*
  - Returns
    - *result (list) : ((부정 강도, 긍정 강도), 긍/부정 라벨) 구조의 Tuple을 포함하는 리스트. 긍정/부정 강도는 0~1. 긍부정 라벨은 {"positive", "negative"} 중 하나.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "늘 배우고 배푸는 자세가 필요합니다."
    > result = senti.tag(sentence, neutral_th=0.3)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > ((0.0595, 0.9543), 'positive')
    > ```

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "과한 욕심은 주변 사람들에게 피해를 줍니다."
    > result = senti.tag(sentence, neutral_th=0.3)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > ((0.8715, 0.1076), 'negative')
    > ```

- `teanaps.text_analysis.SentimentAnalysis.get_weight(self, sentence)` [[Top]](#teanaps-architecture)
  - 감성수준 분류에 참조된 각 각 형태소별 가중치를 하이라이트한 형태의 문장 그래프로 출력합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *result (dict) : {"token_list", "weight_list"}가 포함된 딕셔너리.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "늘 배우고 배푸는 자세가 필요합니다."
    > result = senti.get_weight(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > {
    >   'token_list': [' 늘', ' 배우', '고', ' 배', '푸', '는', ' 자세', '가', ' 필요', '합니다', ' ', '.'],
    >   'weight_list': [0.072522074, 0.08697342, 0.052703843, 0.051040735, 0.0606895, 0.05134341, 0.05213573, 0.08644837, 0.078125894, 0.079360135, 0, 0.079488374]
    > }
    > ```

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "과한 욕심은 주변 사람들에게 피해를 줍니다."
    > result = senti.get_weight(sentence)
    > print(result)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > ```python
    > {
    >   'token_list': [' ', '과', '한', ' 욕심', '은', ' 주변', ' 사람들', '에게', ' 피해를', ' ', '줍', '니다', ' ', '.'],
    >   'weight_list': [0, 0.020344315, 0.024879746, 0.02612342, 0.03615231, 0.048542265, 0.06707654, 0.0936653, 0.07649707, 0, 0.08189902, 0.08962273, 0, 0.07841993]
    > }
    > ```

- `teanaps.text_analysis.SentimentAnalysis.draw_weight(self, sentence)` [[Top]](#teanaps-architecture)
  - 감성수준 분류에 참조된 각 각 형태소별 가중치를 히스토그램으로 출력합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *plotly graph (graph object) : 감성수준 분류에 참조된 각 각 형태소에 대한 가중치 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "늘 배우고 배푸는 자세가 필요합니다."
    > senti.draw_weight(sentence)
    > ```
    > Output (in Jupyter Notebook) :
    > ![sentiment_pos_histogram](../data/sample_image/sentiment_pos_histogram.png)

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "과한 욕심은 주변 사람들에게 피해를 줍니다."
    > senti.draw_weight(sentence)
    > ```
    > Output (in Jupyter Notebook) :
    > ![sentiment_neg_histogram](../data/sample_image/sentiment_neg_histogram.png)

- `teanaps.text_analysis.SentimentAnalysis.draw_sentence_weight(self, sentence)` [[Top]](#teanaps-architecture)
  - 감성수준 분류에 참조된 각 각 형태소별 가중치를 하이라이트한 형태의 문장 그래프로 출력합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
  - Returns
    - *plotly graph (graph object) : 문장 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "늘 배우고 배푸는 자세가 필요합니다."
    > senti.draw_sentence_weight(sentence)
    > ```
    > Output (in Jupyter Notebook) :
    > ![sentiment_weight_pos](../data/sample_image/sentiment_weight_pos.png)

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "과한 욕심은 주변 사람들에게 피해를 줍니다."
    > senti.draw_sentence_weight(sentence)
    > ```
    > Output (in Jupyter Notebook) :
    > ![sentiment_weight_neg](../data/sample_image/sentiment_weight_neg.png)

- `teanaps.text_analysis.SentimentAnalysis.get_sentiment_parse(sentence, neutral_th=0.3)` [[Top]](#teanaps-architecture)
  - 문장의 각 어절에 대한 감성수준을 긍정 또는 부정으로 분류하고 그 가중치를 반환합니다.
  - Parameters
    - *sentence (str) : 한국어 또는 영어로 구성된 문장. 최대 128자.*
    - *neutral_th (float) : 긍정 또는 부정의 강도 차이에서 중립으로 판단하는 범위. 0~1.*
  - Returns
    - *phrase_token_weight_list (list) : 어절과 각 어절에 대한 감성분석 결과를 포함하는 리스트.*
    - *token_list (list) : 문장의 각 형태소를 포함하는 리스트.*
    - *weight_list (list) : 문장의 각 형태소 별 가중치를 포함하는 리스트.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > sentence = "욕심쟁이에게 스트레스 받으며 살다가 떠나고나니 너무 행복해요!"
    > senti.get_sentiment_parse(sentence, neutral_th=0.5)
    > ```
    > Output (in Jupyter Notebook) :
    > ```python
    > [(((0.5991, 0.3836), 'neutral'), '욕심쟁이에게', [[('욕심쟁이', 'NNG', 'UN', (0, 4))], [('에게', 'JKB', 'UN', (4, 6))]]), (((0.9147, 0.0828), 'negative'), '스트레스 받으며', [[('스트레스', 'NNG', 'UN', (7, 11)), ('받', 'VV', 'UN', (12, 13))], [('으며', 'EC', 'UN', (13, 15))]]), (((0.9047, 0.0953), 'negative'), '살다가', [[('살', 'VV', 'UN', (16, 17))], [('다가', 'EC', 'UN', (17, 19))]]), (((0.8306, 0.1751), 'negative'), '떠나고', [[('떠나', 'VV', 'UN', (20, 22))], [('고', 'EC', 'UN', (22, 23))]]), (((0.453, 0.5296), 'neutral'), '나니', [[('나', 'VX', 'UN', (23, 24))], [('니', 'EC', 'UN', (24, 25))]]), (((0.1065, 0.8982), 'positive'), '너무 행복해요!', [[('너무', 'MAG', 'UN', (26, 28))], [('행복', 'NNG', 'UN', (29, 31))], [('해요', 'XSV+EF', 'UN', (31, 33)), ('!', 'SW', 'UN', (33, 34))]])]
    > [' 욕심', '쟁', '이', '에게', ' 스트레스', ' 받으며', ' 살', '다', '가', ' 떠나', '고', ' 나', '니', ' 너무', ' 행복', '해', '요', ' ', '!']
    > [0, 0, 0, 0, -0.2424436, -0.20117857, -0.16506892, -0.16892226, -0.27025366, -0.16876356, -0.33119142, 0, 0, 0.15942541, 0.13346915, 0.11855107, 0.15605149, 0, 0.11754697]
    > ```

- `teanaps.text_analysis.SentimentAnalysis.draw_sentiment_parse(token_list, weight_list)` [[Top]](#teanaps-architecture)
  - 문장의 각 어절에 대한 감성분석 결과를 하이라이트한 형태의 문장 그래프로 출력합니다.
  - Parameters
    - *token_list (list) : 문장의 각 형태소를 포함하는 리스트. `teanaps.text_analysis.SentimentAnalysis.get_sentiment_parse`참고.*
    - *weight_list (list) : 문장의 각 형태소 별 가중치를 포함하는 리스트. `teanaps.text_analysis.SentimentAnalysis.get_sentiment_parse`참고.*
  - Returns
    - *plotly graph (graph object) : 문장 그래프.*
  - Examples

    > Python Code (in Jupyter Notebook) :
    > ```python
    > #sentence = "욕심쟁이에게 스트레스 받으며 살다가 떠나고나니 너무 행복해요!"
    > #token_list = [' 욕심', '쟁', '이', '에게', ' 스트레스', ' 받으며', ' 살', '다', '가', ' 떠나', '고', ' 나', '니', ' 너무', ' 행복', '해', '요', ' ', '!']
    > #weight_list = [0, 0, 0, 0, -0.2424436, -0.20117857, -0.16506892, -0.16892226, -0.27025366, -0.16876356, -0.33119142, 0, 0, 0.15942541, 0.13346915, 0.11855107, 0.15605149, 0, 0.11754697]
    > senti.draw_sentiment_parse(token_list, weight_list)
    > ```
    > Output (in Jupyter Notebook) :
    > ![sentiment_parse](../data/sample_image/sentiment_parse.png)

##### 3.6. `teanaps.text_analysis.DocumentSummarizer`
  - TBU

##### 3.7. `teanaps.text_analysis.KeyphraseExtraction`
  - TBU
