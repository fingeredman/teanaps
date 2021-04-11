# `TEANAPS` User Guide

---
## Contents
- Install `TEANAPS`
- [API Documentation](./teanaps_user_guide-api_documentation-handler.md#teanaps-user-guide)
  - [Handler](./teanaps_user_guide-api_documentation-handler.md#teanaps-user-guide)
  - [NLP](./teanaps_user_guide-api_documentation-nlp.md#teanaps-user-guide)
  - [Text Analysis](./teanaps_user_guide-api_documentation-text_analysis.md#teanaps-user-guide)
  - [Visualization](./teanaps_user_guide-api_documentation-visualization.md#teanaps-user-guide)
  - [Machine Learning](./teanaps_user_guide-api_documentation-machine-learning.md#teanaps-user-guide)
- [`TEANAPS` OPEN API](./teanaps_user_guide-rest_api.md#teanaps-user-guide)
- [Tutorial](./teanaps_user_guide-tutorial.md#teanaps-user-guide)
- [References](./teanaps_user_guide-references_journal_project.md#teanaps-user-guide)
- [Journal & Project](./teanaps_user_guide-references_journal_project.md#teanaps-user-guide)
- [Appendix](./teanaps_user_guide-appendix.md#teanaps-user-guide)

---
## Install `TEANAPS`

### Quick Start
- `install.ipynb` 파일을 참조해주세요.
- 링크를 통해 설치용 `Jupyter Notebook` 파일을 `Google Colabotory`로 열 수 있습니다. [(Link)](https://colab.research.google.com/github/fingeredman/teanaps/blob/master/install.ipynb)
- 로컬 환경에 철치가 필요하신 경우, [teanaps_install.py](https://github.com/fingeredman/teanaps/blob/master/teanaps_setup.py) 파일을 참고 바랍니다.
- 본 패키지는 `pip`를 통한 설치를 지원하지 않습니다.
- `Windows 운영체제`에서 일부 기능에 제한이 있을 수 있습니다.

> Python Code (in Jupyter Notebook) :
> ```python
> !git clone https://github.com/fingeredman/teanaps.git
> !python "teanaps/teanaps_setup.py"
> ```

### 로컬환경 설치 가이드

> 1. 가이드 문서를 참조하여 Python Anaconda, Java 환경 설치 [(LINK)](https://github.com/fingeredman/text-mining-for-beginner/blob/master/lecture-note/text-mining-for-beginner-appendix1.pdf)
> 2. 아래 Requirements에 명시된 Python 라이브러리 설치
> 3. TEANAPS [메인페이지](http://teanaps.com) [Code > Download ZIP]을 통해 TEANAPS 라이브러리 다운로드
> 4. 다운로드한 파일 압축해제 후 폴더이름을 [teanaps-master > teanaps]로 변경하여 분석을 수행하는 Jupyter Notebook 파일(*.ipynb)과 같은 폴더로 이동

#### Requirements
- [PyTorch](https://pytorch.org/) - *conda install pytorch*
- [Gensim](https://pypi.org/project/gensim/) - *pip install gensim==3.8.3*
- [NLTK](https://www.nltk.org/install.html) - *pip install nltk*

  > Python Code (in Jupyter Notebook) :
  > ```python
  > import nltk
  > nltk.download('punkt')
  > nltk.download('averaged_perceptron_tagger')
  > nltk.download('wordnet')
  > ```

- [Plotly](https://plot.ly/python/getting-started/) - *pip install plotly==2.7.0*
- [PyLDAvis](https://pypi.org/project/pyLDAvis/) - *pip install pyldavis*
- [Wordcloud](https://pypi.org/project/wordcloud/) - *pip install wordcloud*
- [xlwt](https://pypi.org/project/xlwt/) - *pip install xlwt*
- [KoNLPy](http://konlpy.org/en/latest/#getting-started) - *pip install konlpy==0.5.1*
- [newspaper](https://pypi.org/project/newspaper3k/) - *pip install newspaper3k*
- [sumy](https://pypi.org/project/sumy/) - *pip install sumy*
- [SoyNLP](https://github.com/lovit/soynlp) - *pip install soynlp*
- [PyTorch-CRF](https://pypi.org/project/pytorch-crf/) - *pip install pytorch-crf*
- [PyTorch-Transformers](https://pypi.org/project/pytorch-transformers/) - *pip install pytorch-transformers*
- [Transformers](https://pypi.org/project/transformers/) - *pip install transformers*
- [GluonNLP](https://pypi.org/project/gluonnlp/) - *pip install gluonnlp*
- [pytorch-pretrained-bert](https://pypi.org/project/pytorch-pretrained-bert/) - *pip install pytorch-pretrained-bert*
- [mxnet](https://pypi.org/project/mxnet/) - *pip install --upgrade mxnet>=1.5.0*
- [iGraph](https://pypi.org/project/igraph-python/) - *pip install python-igraph*
- [pdfminer](https://pypi.org/project/pdfminer/) - *pip install pdfminer*
- [docx2txt](https://pypi.org/project/docx2txt/) - *pip install docx2txt*
- [python-pptx](https://python-pptx.readthedocs.io/en/latest/) - *pip install python-pptx*
- [Korean Sentence Splitter](https://github.com/hyunwoongko/kss?fbclid=IwAR2G4Ym3OwQOeouTokpjTMXo49vpZGuF5mYS7GUsmTSpKehXvDrCqSj-Zhk#korean-sentence-splitter) - *pip install kss*
- [mecab](https://bitbucket.org/eunjeon/mecab-ko/src/master/) - *Install MeCab for [Mac/Linux](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/), or [Windows](https://cleancode-ws.tistory.com/97)*  
	- Windows 운영체제 설치 시 현재 파이썬 버전이 3.8인 경우 *.whl 파일 다운로드 [(Link)](https://github.com/Pusnow/mecab-python-msvc/releases)

<br><br>
---
<center>ⓒ 2021. TEANAPS all rights reserved.</center>
