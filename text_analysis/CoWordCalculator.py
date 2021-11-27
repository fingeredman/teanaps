from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY
from teanaps.visualization import TextVisualizer
from teanaps.visualization import GraphVisualizer

import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

from IPython.display import display

import concurrent.futures
from collections import Counter
import math

import networkx as nx

class CoWordCalculator():  
    def __init__(self):
        None
        
    def __calculation(self, word_list):
        word_pair_list = []
        for word_index in range(len(word_list)):
            if word_list[word_index] in self.__get_stopwords() or len(word_list[word_index]) <= 1:
                continue
            WINDOW_SIZE = con.WINDOW_SIZE
            start_window_index = word_index-WINDOW_SIZE if WINDOW_SIZE <= word_index else 0
            end_window_index = word_index+WINDOW_SIZE+1
            window = word_list[start_window_index:end_window_index] 
            #pairs = [(word_list[word_index], word) for word in window if word not in self.__get_stopwords() and len(word) > 1]
            pairs = [(word_list[word_index], word) for word in window if word not in self.__get_stopwords()]
            word_pair_list.extend(pairs)
        return word_pair_list

    def __calculation_co_word(self, tokenized_sentence_list):
        sentence_list = []
        for tokenized_sentence in tokenized_sentence_list:
            sentence_list.append(tokenized_sentence.split(" "))
        word_pair_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=con.MAX_WORKERS) as executor:
            future_co_word = {
                executor.submit(self.__calculation, sentence_list[idx]): idx for idx in range(len(sentence_list))
            }
            for future in concurrent.futures.as_completed(future_co_word):
                try:
                    word_pair_list.extend(future.result())
                except Exception as exc:
                    continue
        return word_pair_list
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    
    def calculation_co_matrix(self, tokenized_sentence_list, node_list=[]):
        word_pair_list = self.__calculation_co_word(tokenized_sentence_list)
        if len(node_list) == 0:
            self.result_list = [((first_word, second_word), count) 
                                for (first_word, second_word), count in Counter(word_pair_list).items()]    
        else:
            self.result_list = [((first_word, second_word), count) 
                                for (first_word, second_word), count in Counter(word_pair_list).items() 
                                if first_word in node_list and second_word in node_list]
        self.result_list.sort(key=lambda elem: elem[1], reverse=True)
    
    def get_edge_list(self):
        return self.result_list
    
    def get_node_list(self):
        node_list = []
        for result in self.result_list:
            node = result[0][0]
            if node not in node_list:
                node_list.append(node)
        return node_list
    
    def get_co_word(self, word):
        co_word_list = [(first_word, count) 
                        for (first_word, second_word), count in self.result_list 
                        if second_word == word]
        co_word_list.sort(key=lambda elem: elem[1], reverse=True)
        return co_word_list[1:]
        
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
        
    def get_co_matrix_graph(self, max_words):
        gv = GraphVisualizer()
        gv.set_plotly()
        co_word_list = self.result_list
        x_data = []
        max_freq = 0
        for co_word, freq in co_word_list[:max_words]:
            first_word = co_word[0]
            second_word = co_word[1]
            if max_freq < freq:
                max_freq = freq
            if first_word not in x_data:
                x_data.append(first_word) 
            if second_word not in x_data:
                x_data.append(second_word)
        y_data = x_data
        z_data = [[0 for freq in x_data] for freq in y_data]
        for co_word, freq in co_word_list[:max_words]:
            first_word = co_word[0]
            second_word = co_word[1]
            z_data[x_data.index(first_word)][y_data.index(second_word)] = freq
        data_meta = {
            "colorbar_title": "동시출현빈도 (CO-WORD FREQUENCY)",
            "x_data": x_data,
            "y_data": y_data,
            "z_data": z_data
        }
        graph_meta = {
            "title": "동시출현빈도 매트릭스 (CO-WORD MATRIX)",
            "height": 1000, 
            "width": 1000,
            "y_tickangle": -45,
            "y_name": "Y",
            "x_tickangle": -45,
            "x_name": "X",
        }
        return gv.draw_matrix(data_meta, graph_meta)
    
    def get_centrality(self, centrality_type):
        edge_list = self.get_edge_list()
        edge_list = [(co_word[0], co_word[1], freq) for co_word, freq in edge_list]
        self.G = nx.Graph()        
        self.G.add_weighted_edges_from(edge_list)
        if centrality_type == "b_cent":
            centrality_dict = nx.betweenness_centrality(self.G)
        elif centrality_type == "d_cent":
            centrality_dict = nx.degree_centrality(self.G)
        elif centrality_type == "c_cent":
            centrality_dict = nx.closeness_centrality(self.G)
        return centrality_dict  
    
    
    def get_word_network_graph(self, centrality_dict, mode="markers", centrality_th=0.5, weight_th=0.5, ego_node_list=[], node_size_rate=10, edge_width_rate=10, text_size_rate=10):
        tv = TextVisualizer()
        tv.set_plotly()
        
        if len(ego_node_list) > 0:
            edge_list = [(a, b, w) for (a, b), w in self.get_edge_list() if w >= weight_th and (a in ego_node_list or b in ego_node_list) and (centrality_dict[a] >= centrality_th and centrality_dict[b] >= centrality_th)]
        else:
            edge_list = [(a, b, w) for (a, b), w in self.get_edge_list() if w >= weight_th and (centrality_dict[a] >= centrality_th and centrality_dict[b] >= centrality_th)]
        node_list = []
        for a, b, c in edge_list:
            #if c >= weight_th:
            if a not in node_list:
                node_list.append(a)
            if b not in node_list:
                node_list.append(b)
        
        data_meta = {
            "node_list": node_list,
            "edge_list": edge_list,
            "weight_dict": centrality_dict
        }

        graph_meta = {
            "title": "Word Network Graph",
            "height": 1000, 
            "width": 1000,
            "weight_name": "Word Centrality",
        }

        return tv.draw_network(data_meta, graph_meta, mode=mode, node_size_rate=node_size_rate, edge_width_rate=edge_width_rate)