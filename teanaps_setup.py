import subprocess
import platform
import os

# 1) Gensim (https://pypi.org/project/gensim/)
subprocess.call("pip install gensim --upgrade", shell=True)
#!pip install gensim --upgrade

# 2) Glove (https://pypi.org/project/glove_python/)
subprocess.call("pip install glove_python", shell=True)
#!pip install glove_python

# 3) NLTK (https://www.nltk.org/install.html)
subprocess.call("pip install nltk", shell=True)
#!pip install nltk

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# 4) Plotly (https://plot.ly/python/getting-started/)
subprocess.call("pip install plotly==2.7.0", shell=True)
#!pip install plotly==2.7.0

# 5) PyLDAvis (https://pypi.org/project/pyLDAvis/)
subprocess.call("pip install pyldavis", shell=True)
#!pip install pyldavis

# 6) Wordcloud (https://pypi.org/project/wordcloud/)
subprocess.call("pip install wordcloud", shell=True)
#!pip install wordcloud

# 7) xlwt (https://pypi.org/project/xlwt/)
subprocess.call("pip install xlwt", shell=True)
#!pip install xlwt

# 8) KoNLPy (http://konlpy.org/en/latest/#getting-started)
subprocess.call("!pip install konlpy==0.5.1", shell=True)
#!pip install konlpy

# 9) newspaper (https://pypi.org/project/newspaper3k/)
subprocess.call("pip install newspaper3k", shell=True)
#!pip install newspaper3k

# 10) sumy (https://pypi.org/project/sumy/)
subprocess.call("pip install sumy", shell=True)
#!pip install sumy

# 11) SoyNLP (https://github.com/lovit/soynlp)
subprocess.call("pip install soynlp", shell=True)
#!pip install soynlp

# 12) PyKoSpacing(https://github.com/haven-jeon/PyKoSpacing)
subprocess.call("pip install git+https://github.com/haven-jeon/PyKoSpacing.git", shell=True)
#!pip install git+https://github.com/haven-jeon/PyKoSpacing.git

# 13) PyTorch-CRF(https://pypi.org/project/pytorch-crf/)
subprocess.call("pip install pytorch-crf", shell=True)
#!pip install pytorch-crf

# 14) PyTorch-Transformers(https://pypi.org/project/pytorch-transformers/)
subprocess.call("pip install pytorch-transformers", shell=True)
#!pip install pytorch-transformers

# 15) Transformers(https://pypi.org/project/transformers/)
subprocess.call("pip install transformers", shell=True)
#!pip install transformers

# 16) GluonNLP(https://pypi.org/project/gluonnlp/)
subprocess.call("pip install gluonnlp", shell=True)
#!pip install gluonnlp
subprocess.call("pip install --upgrade mxnet>=1.5.0", shell=True)
#!pip install --upgrade mxnet>=1.5.0

os_type = platform.platform()
if "Windows" not in os_type:
    # MeCab
    subprocess.call("apt-get install openjdk-8-jdk-headless -qq > /dev/null", shell=True)
    subprocess.call("pip3 install JPype1-py3", shell=True)

    os.chdir('/tmp/')
    subprocess.call("curl -LO https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.1.tar.gz", shell=True)
    subprocess.call("tar zxfv mecab-0.996-ko-0.9.1.tar.gz", shell=True)

    os.chdir('/tmp/mecab-0.996-ko-0.9.1')
    subprocess.call("./configure", shell=True)
    subprocess.call("make", shell=True)
    subprocess.call("make check", shell=True)
    subprocess.call("make install", shell=True)

    os.chdir('/tmp')
    subprocess.call("curl -LO http://ftpmirror.gnu.org/automake/automake-1.11.tar.gz", shell=True)
    subprocess.call("tar -zxvf automake-1.11.tar.gz", shell=True)
    os.chdir('/tmp/automake-1.11')
    subprocess.call("./configure", shell=True)
    subprocess.call("make", shell=True)
    subprocess.call("make install", shell=True)

    os.chdir('/tmp/')
    subprocess.call("wget -O m4-1.4.9.tar.gz http://ftp.gnu.org/gnu/m4/m4-1.4.9.tar.gz", shell=True)
    subprocess.call("tar -zvxf m4-1.4.9.tar.gz", shell=True)
    os.chdir('/tmp/m4-1.4.9')
    subprocess.call("./configure", shell=True)
    subprocess.call("make", shell=True)
    subprocess.call("make install", shell=True)

    os.chdir('/tmp')
    subprocess.call("curl -OL http://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz", shell=True)
    subprocess.call("tar xzf autoconf-2.69.tar.gz", shell=True)
    os.chdir('/tmp/autoconf-2.69')
    subprocess.call("./configure --prefix=/usr/local", shell=True)
    subprocess.call("make", shell=True)
    subprocess.call("make install", shell=True)
    subprocess.call("export PATH=/usr/local/bin", shell=True)
    subprocess.call("sudo apt-get install automake", shell=True)

    os.chdir('/tmp')
    subprocess.call("curl -LO https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz", shell=True)
    subprocess.call("tar -zxvf mecab-ko-dic-2.0.1-20150920.tar.gz", shell=True)
    
    os.chdir('/tmp/mecab-ko-dic-2.0.1-20150920')
    subprocess.call("./autogen.sh", shell=True)
    subprocess.call("./configure", shell=True)
    subprocess.call("make", shell=True)
    subprocess.call("make install", shell=True)
    
    # install mecab-python
    os.chdir('/content')
    subprocess.call("git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git", shell=True)

    os.chdir('/content/mecab-python-0.996')
    subprocess.call("python3 setup.py build", shell=True)
    subprocess.call("python3 setup.py install", shell=True)
    subprocess.call("cd", shell=True)