from Teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly.plotly as py
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

class TfidfCalculator():  
    def __init__(self):
        self.stopword_list = self.__get_stopwords()
    
    def calculation_tfidf(self, tokenized_sentence_list):
        # TF-IDF Vector
        tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(tokenized_sentence_list).todense()
        self.tfidf_matrix = pd.DataFrame(self.tfidf_matrix, columns=tfidf_vectorizer.get_feature_names())
        self.tfidf_dict = dict(self.tfidf_matrix.sum(axis=0).sort_values(ascending=False).items())
        # TF Vector
        tf_vectorizer = CountVectorizer()
        self.tf_matrix = tf_vectorizer.fit_transform(tokenized_sentence_list).todense()
        self.tf_matrix = pd.DataFrame(self.tf_matrix, columns=tf_vectorizer.get_feature_names())
        self.tf_dict = dict(self.tf_matrix.sum(axis=0).sort_values(ascending=False).items())
        # Make Result Dictionary
        self.result_dict = {}
        for word in self.tf_dict.keys():
            self.result_dict[word] = {"tf": self.tf_dict[word], "tfidf": self.tfidf_dict[word]}
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list

    def get_result(self):
        return self.result_dict
    
    def get_tf_matrix(self):
        return self.tf_matrix
    
    def get_tf_dict(self):
        return self.tf_dict
    
    def get_tf_list(self):
        tf_list = [[word, self.tf_dict[word]] for word in self.tf_dict.keys() if word not in self.stopword_list]
        return tf_list
        
    def get_tfidf_matrix(self):
        return self.tfidf_matrix
    
    def get_tfidf_dict(self):
        return self.tfidf_dict
    
    def get_tfidf_list(self):
        tfidf_list = [[word, self.tfidf_dict[word]] for word in self.tfidf_dict.keys() if word not in self.stopword_list]
        return tfidf_list
        
    def get_word_list(self):
        word_list = [word for word in self.tfidf_dict.keys() if word not in self.stopword_list]
        return word_list
    
    def get_plotly_graph(self, max_words):
        x = self.get_word_list()[:max_words]
        y = [score for word, score in self.get_tf_list()][:max_words]
        z = [score for word, score in self.get_tfidf_list()][:max_words]
        data = [
            go.Histogram(
                histfunc = "sum",
                x=x,
                y=y,
                name="TF",
                marker=dict(
                    color='#FFD7E9',
                ),
                yaxis = 'y'
            ),
            go.Scatter(
                x=x,
                y=z,
                name="TF-IDF",
                marker=dict(
                    color='black',
                ),
                yaxis='y2'
            )
        ]
        layout = go.Layout(
            title='TF & TF-IDF Graph',
            xaxis=dict(
                title='WORD',
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                showticklabels=True,
                tickangle=-45,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all'
            ),
            yaxis=dict(
                title='TF',
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all',
                #overlaying='y',
            ),
            yaxis2=dict(
                title='TF-IDF',
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                overlaying='y',
                side='right'
            )
        )
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig, filename='TF-IDF Graph')