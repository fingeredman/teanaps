from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from newspaper import Article #!pip install newspaper3k
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

import sumy
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy import summarizers
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

class DocumentSummarizer():  
    def __init__(self):
        self.stopword_list = self.__get_stopwords()
    
    def summarize(self, summarizer_type, max_sentences):
        # TextRank
        if summarizer_type == "textrank":
            self.result_list = summarize(self.document, ratio=0.3, word_count=None, split=True)
        #PyTextRank
        elif summarizer_type == "lsa":
            parser = HtmlParser.from_string(self.document, None,tokenizer=Tokenizer("english"))
            stemmer = Stemmer("english")
            summarizer = summarizers.lsa.LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")
            summarized_sentence_list = summarizer(parser.document, max_sentences)
            self.result_list = [str(sentence) for sentence in summarized_sentence_list]
    
    def set_document(self, document_path):
        self.document = open(document_path, encoding="utf-8").read().strip()
        
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list

    def get_result(self):
        return self.result_list