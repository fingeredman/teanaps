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

### Requirements
- [Gensim](https://pypi.org/project/gensim/) - *pip install gensim --upgrade*
- [Glove](https://pypi.org/project/glove_python/) - *pip install glove_python*
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
- [PyKoSpacing](https://github.com/haven-jeon/PyKoSpacing) - *pip install git+https://github.com/haven-jeon/PyKoSpacing.git*
- [PyTorch-CRF](https://pypi.org/project/pytorch-crf/) - *pip install pytorch-crf*
- [PyTorch-Transformers](https://pypi.org/project/pytorch-transformers/) - *pip install pytorch-transformers*
- [Transformers](https://pypi.org/project/transformers/) - *pip install transformers*
- [GluonNLP](https://pypi.org/project/gluonnlp/) - *pip install gluonnlp*
- [mxnet](https://) - *pip install --upgrade mxnet>=1.5.0*
- [iGraph](https://pypi.org/project/igraph-python/) - *pip install python-igraph*
- [mecab](http://) - *Install MeCab for [Mac/Linux](http://), or [Windows](http://)*
