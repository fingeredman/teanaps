from teanaps import configure as con
from teanaps.nlp import Processing
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

from gensim.summarization.summarizer import summarize

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

class DocumentSummarizer():  
    def __init__(self):
        self.stopword_list = self.__get_stopwords()
        self.pro = Processing()
        self.document = ""
    
    def summarize(self, summarizer_type, max_sentences, document = ""):
        if self.document == "":
            target_document = document
        else:
            target_document = self.document
        # Spacing
        _target_document = ""
        sentence_list = self.pro.sentence_splitter(target_document)
        for sentence in sentence_list:
            _target_document += sentence + " "
        _target_document = _target_document.strip()
        # TextRank
        if summarizer_type == "textrank":
            self.result_list = summarize(_target_document, ratio=0.3, word_count=None, split=True)[:max_sentences]
        # PyTextRank
        elif summarizer_type == "lsa":
            parser = HtmlParser.from_string(_target_document, None,tokenizer=Tokenizer("english"))
            stemmer = Stemmer("english")
            summarizer = LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")
            summarized_sentence_list = summarizer(parser.document, max_sentences)
            self.result_list = [str(sentence) for sentence in summarized_sentence_list]
        return self.result_list
    
    def set_document(self, document_path):
        self.document = open(document_path, encoding="utf-8").read().strip()
        
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list

    def get_result(self):
        return self.result_list