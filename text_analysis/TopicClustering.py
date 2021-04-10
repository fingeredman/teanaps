from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

from IPython.display import display

import gensim
from gensim import corpora
from gensim.models import ldaseqmodel
from gensim.models import CoherenceModel
#import pyLDAvis.gensim

import pandas as pd
pd.set_option('display.max_columns', None)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

class TopicClustering():  
    def __init__(self):
        None
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    
    def sequence_lda_topic_modeling(self, tokenized_sentence_list, time_slice, num_topics):
        self.time_slice = time_slice
        texts = [[word for word in document.split(" ") if word not in self.__get_stopwords()] 
                 for document in tokenized_sentence_list]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        self.ldaseq = ldaseqmodel.LdaSeqModel(corpus=corpus, id2word=dictionary, 
                                         time_slice=self.time_slice, num_topics=num_topics, em_max_iter=10)
        sequence_topic_list = []
        for num in range(num_topics):
            sequence_topic_list.append((num, self.ldaseq.print_topic_times(topic=num)))
        return sequence_topic_list
    
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
    
    def get_sequence_topic_graph(self):
        max_topics = self.ldaseq.num_topics
        topic_weight_dict = {}
        for num_topics in range(max_topics):
            topic_weight_list = []
            topic_keyword_list = []
            for topic in self.ldaseq.print_topic_times(topic=num_topics):
                topic_weight = sum([weight for word, weight in topic])
                topic_weight_list.append(topic_weight)
                topic_keyword_list = [word for word, weight in topic]
            topic_weight_dict[num_topics] = {"topic_weight_list": topic_weight_list, "topic_keyword_list": topic_keyword_list}
        
        data = []
        x = [str(num_topics) for num_topics in range(len(self.time_slice))]
        for num_topic, value in topic_weight_dict.items():
            y = value["topic_weight_list"]
            data.append(go.Scatter(
                x=x,
                y=y,
                name='topic '+str(num_topic)+"<br>"+str(value["topic_keyword_list"][:10]),
                marker=dict(
                    #color='blue',
                ),
                yaxis='y'
            ),)
        layout = go.Layout(
            title='Sequence LDA Model Topic Trend',
            xaxis=dict(
                title='TIME SLICE',
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                dtick = 1,
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all'
            ),
            yaxis=dict(
                title='WEIGHT',
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
            ),
        )
        self.set_plotly()
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig, filename='TF-IDF Graph')
    
    def topic_modeling(self, model_type, document_list, num_topics, num_keywords):
        topic_list = []
        self.texts = [[word for word in document.split(" ") if word not in self.__get_stopwords()] for document in document_list]
        self.dictionary = corpora.Dictionary(self.texts)    
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]
        if model_type == "lsi":
            self.model = gensim.models.lsimodel.LsiModel(self.corpus, num_topics=num_topics, id2word=self.dictionary)
        elif model_type == "lda":
            self.model = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary, passes=10)
        elif model_type == "hdp":
            self.model = gensim.models.hdpmodel.HdpModel(self.corpus, id2word=self.dictionary)
        else:
            return []
        for num in range(num_topics):
            topic_list.append((num, self.model.show_topic(num, num_keywords)))
        return topic_list
    
    def get_model(self):
        return self.model
    
    def get_model_validation_result(self):
        try:
            perplexity = self.model.log_perplexity(self.corpus)
        except:
            perplexity = 0
        coherence_model = CoherenceModel(model=self.model, texts=self.texts, dictionary=self.dictionary, coherence='c_v')
        coherence = coherence_model.get_coherence()
        return perplexity, coherence
    
    def display_model_result(self):
        pyLDAvis.enable_notebook()
        lda_display = pyLDAvis.gensim.prepare(self.model, self.corpus, self.dictionary, sort_topics=True)
        return pyLDAvis.display(lda_display)
    
    def get_model_validation_graph(self, model_type, document_list, max_topics):
        validation_list = []
        num_keywords = 10
        for num_topics in range(2, max_topics+1):
            self.topic_modeling(model_type, document_list, num_topics, num_keywords)
            perplexity, coherence = self.get_model_validation_result()
            validation_list.append([num_topics, perplexity, coherence])
        x = [str(num_topics) for num_topics, perplexity, coherence in validation_list]
        y = [perplexity for num_topics, perplexity, coherence in validation_list]
        z = [coherence for num_topics, perplexity, coherence in validation_list]
        data = [
            go.Scatter(
                x=x,
                y=y,
                name="Perplexity",
                marker=dict(
                    #color='blue',
                ),
                yaxis='y'
            ),
            go.Scatter(
                x=x,
                y=z,
                name="Coherence",
                marker=dict(
                    #color='red',
                ),
                yaxis='y2'
            )
        ]
        layout = go.Layout(
            title='LDA Model Perplexity & Coherence Graph',
            xaxis=dict(
                title='NUMBER of TOPIC',
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                dtick = 1,
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all'
            ),
            yaxis=dict(
                title='Perplexity',
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
            ),
            yaxis2=dict(
                title='Coherence',
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
        self.set_plotly()
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig, filename='TF-IDF Graph')

    def get_topics_sentences(self, document_list):
        df_topics_sentences = pd.DataFrame()
        for i, row in enumerate(self.model[self.corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            for j, (num_topic, prop_topic) in enumerate(row):
                if j == 0:
                    wp = self.model.show_topic(num_topic)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    df_topics_sentences = df_topics_sentences.append(pd.Series([int(num_topic), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break
        df_topics_sentences.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
        contents = pd.Series(document_list)
        df_topics_sentences = pd.concat([df_topics_sentences, contents], axis=1)
        df_dominant_topic = df_topics_sentences.reset_index()
        df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        return df_topics_sentences
    
    def get_topics_documents(self, document_list):
        df_topics_sentences = pd.DataFrame()
        for row in self.model[self.corpus]:
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            for j, (num_topic, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = self.model.show_topic(num_topic)
                    topic_keywords = ", ".join([word for word, _ in wp])
                    df_topics_sentences = df_topics_sentences.append(pd.Series([int(num_topic), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break
        df_topics_sentences.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
        
        contents = pd.Series(document_list)
        df_topics_sentences = pd.concat([df_topics_sentences, contents], axis=1)
        df_dominant_topic = df_topics_sentences.reset_index()
        df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        
        sent_topics_sorteddf = pd.DataFrame()
        sent_topics_outdf_grpd = df_topics_sentences.groupby('Dominant_Topic')
        for _, grp in sent_topics_outdf_grpd:
            sent_topics_sorteddf = pd.concat([sent_topics_sorteddf, 
                                                     grp.sort_values(['Perc_Contribution'], ascending=[0]).head(5)], axis=0)
        sent_topics_sorteddf.reset_index(drop=True, inplace=True)
        sent_topics_sorteddf.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]
        return sent_topics_sorteddf