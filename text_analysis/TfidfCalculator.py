from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY
from teanaps.visualization import GraphVisualizer
from teanaps.visualization import TextVisualizer
from teanaps.handler import FileHandler

import plotly 
from plotly.offline import init_notebook_mode
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

from IPython.display import display

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import warnings
warnings.filterwarnings(action='ignore')

class TfidfCalculator():  
    def __init__(self):
        self.fh = FileHandler()
    
    def calculation_tfidf(self, tokenized_sentence_list, tfidf_count=100, tfidf_state=False, ifidf_state="",
                          tf_vectorizer_path=con.TF_VECTORIZER_PATH, tfidf_vectorizer_path=con.TFIDF_VECTORIZER_PATH):
        if ifidf_state != "":
            print("'ifidf_state' has been replaced with 'tfidf_state'")
            return None
        
        # TF Vector
        self.tf_vectorizer = CountVectorizer(token_pattern='\S+')
        self.tf_matrix = self.tf_vectorizer.fit_transform(tokenized_sentence_list).todense()
        self.tf_matrix = pd.DataFrame(self.tf_matrix, columns=self.tf_vectorizer.get_feature_names())
        #self.tf_dict = dict(self.tf_matrix.sum(axis=0).sort_values(ascending=False).items())
        self.tf_dict = {}
        for tokenized_sentence in tokenized_sentence_list:
            word_list = tokenized_sentence.split(" ")
            for word in word_list:
                word = word.lower()
                if word not in self.__get_stopwords():
                    if word in self.tf_dict.keys():
                        self.tf_dict[word] += 1
                    else:
                        self.tf_dict[word] = 1
        
        # TF-IDF Vector
        self.tfidf_vectorizer = TfidfVectorizer(token_pattern='\S+')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(tokenized_sentence_list).todense()
        self.tfidf_matrix = pd.DataFrame(self.tfidf_matrix, columns=self.tfidf_vectorizer.get_feature_names())
        #self.tfidf_dict = dict(self.tfidf_matrix.sum(axis=0).sort_values(ascending=False).items())
        self.tfidf_dict = {}
        if tfidf_state == True:
            tf_list = self.get_tf_list()#[:tfidf_count]
            tfidf_word_list = [word for word, count in tf_list if word in self.tfidf_matrix.keys()]
            self.tfidf_dict = dict(self.tfidf_matrix[tfidf_word_list].sum())
        # Make Result Dictionary
        #self.result_dict = {}
        #for word in self.tf_dict.keys():
        #    self.result_dict[word] = {"tf": self.tf_dict[word], "tfidf": self.tfidf_dict[word]}
        self.fh.save_data(tfidf_vectorizer_path, self.tfidf_vectorizer)
        self.fh.save_data(tf_vectorizer_path, self.tf_vectorizer)
            
    def get_tf_vector(self, sentence, tf_vectorizer_path=con.TF_VECTORIZER_PATH):
        self.tf_vectorizer = self.fh.load_data(tf_vectorizer_path)        
        return self.tf_vectorizer.transform([sentence]).todense().tolist()[0]
    
    def get_tfidf_vector(self, sentence, tfidf_vectorizer_path=con.TFIDF_VECTORIZER_PATH):
        self.tfidf_vectorizer = self.fh.load_data(tfidf_vectorizer_path)
        return self.tfidf_vectorizer.transform([sentence]).todense().tolist()[0]
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    '''
    def get_result(self):
        return self.result_dict
    '''
    def get_tf_matrix(self):
        return self.tf_matrix
    
    def get_tf_dict(self):
        return self.tf_dict
    
    def get_tf_list(self):
        tf_list = [[word, self.tf_dict[word]] for word in self.tf_dict.keys() if word not in self.__get_stopwords()]
        tf_list.sort(key=lambda elem: elem[1], reverse=True)
        return tf_list
    
    def get_tfidf_matrix(self):
        return self.tfidf_matrix
    
    def get_tfidf_dict(self):
        return self.tfidf_dict
    
    def get_tfidf_list(self):
        tfidf_list = [[word, self.tfidf_dict[word]] for word in self.tfidf_dict.keys() if word not in self.__get_stopwords()]
        tfidf_list.sort(key=lambda elem: elem[1], reverse=True)
        return tfidf_list
        
    def get_word_list(self):
        word_list = [word for word in self.tf_dict.keys() if word not in self.__get_stopwords()]
        return word_list
    
    def set_plotly(self):
        import IPython
        display(IPython.core.display.HTML('''
            <script src="/static/components/requirejs/require.js"></script>
            <script>
              requirejs.config({
                paths: {
                  base: '/static/base',
                  plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
                },
              });
            </script>
            '''))
    
    def draw_tfidf(self, max_words=100):
        gv = GraphVisualizer()
        gv.set_plotly()
        x = [word for word, _ in self.get_tf_list()][:max_words]
        y = [score for _, score in self.get_tf_list()][:max_words]
        data_meta_list = []
        data_meta = {
            "graph_type": "histogram",
            "data_name": "TF",
            "x_data": x,
            "y_data": y,
            "y_axis": "y1",
        }
        data_meta_list.append(data_meta)
        #if max_words <= 100:
        z = [self.get_tfidf_dict()[word] for word, _ in self.get_tf_list()][:max_words]
        data_meta = {
            "graph_type": "scatter",
            "data_name": "TF-IDF",
            "x_data": x,
            "y_data": z,
            "y_axis": "y2"
        }
        data_meta_list.append(data_meta)
        graph_meta = {
            "title": "단어빈도 및 TF-IDF (TF & TF-IDF)",
            "x_tickangle": -45,
            "y1_tickangle": 0,
            "y2_tickangle": 0,
            "x_name": "단어 (WORD)",
            "y1_name": "빈도 (TF)",
            "y2_name": "TF-IDF",
        }
        return gv.draw_histogram(data_meta_list, graph_meta)
    
    def get_wordcloud(self, weight_dict, mask_path=None):
        temp_dict = {}
        if type(weight_dict) == list:
            for word, weight in weight_dict:
                temp_dict[word] = weight
            weight_dict = temp_dict
        tv = TextVisualizer()
        tv.set_plotly()
        data_meta = {
            "weight_dict": weight_dict,
        }
        graph_meta = {
            "height": 1000, 
            "width": 1000,
            "min_font_size": 10,
            "max_font_size": 500,
            "margin": 10,
            "background_color": "white",
            "mask_path": mask_path
        }
        tv.draw_wordcloud(data_meta, graph_meta)
