from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY
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
        self.stopword_list = self.__get_stopwords()
        
    def __calculation(self, word_list):
        word_pair_list = []
        for word_index in range(len(word_list)):
            if word_list[word_index] in self.stopword_list or len(word_list[word_index]) <= 1:
                continue
            WINDOW_SIZE = con.WINDOW_SIZE
            start_window_index = word_index-WINDOW_SIZE if WINDOW_SIZE <= word_index else 0
            end_window_index = word_index+WINDOW_SIZE+1
            window = word_list[start_window_index:end_window_index] 
            pairs = [(word_list[word_index], word) for word in window if word not in self.stopword_list and len(word) > 1]
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
            self.result_list = [[(first_word, second_word), count] 
                                for (first_word, second_word), count in Counter(word_pair_list).items()]    
        else:
            self.result_list = [[(first_word, second_word), count] 
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
        co_word_list = [[first_word, count] 
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
    
    
    def get_word_network_graph(self, node_list, centrality_dict):
        edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5,color='#999'), hoverinfo='none', mode='lines')
        pos = nx.spring_layout(self.G)
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text', 
                                marker=dict(showscale=True, colorscale='YlOrRd', reversescale=True, color=[],
                                            size=[math.sqrt(centrality_dict[node])*100 for node in node_list],
                                            colorbar=dict(thickness=15, title='Node Centrality', xanchor='left', 
                                                          titleside='right'), 
                                            line=dict(width=1, color="black")))
        for node in node_list:
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
        for node, adjacencies in enumerate(self.G.adjacency()):
            node_trace['marker']['color']+=tuple([len(adjacencies[1])])
            node_info = "Node: " + str(adjacencies[0]) + "<br>centrality: " + str(centrality_dict[adjacencies[0]])
            node_trace['text']+=tuple([node_info])

        fig = go.Figure(data=[edge_trace, node_trace], 
                        layout=go.Layout(title='Network Graph', titlefont=dict(size=16),
                                         showlegend=False, hovermode='closest',
                                         width=1000, height=1000,margin=dict(b=20,l=5,r=5,t=40),
                                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        return iplot(fig, filename='networkx')
    
    '''
    from multiprocessing import Pool
    import itertools
    import time

    def chunks(l, n):
        l_c = iter(l)
        while 1:
            x = tuple(itertools.islice(l_c, n))
            if not x:
                return
            yield x

    def _betmap(G_normalized_weight_sources_tuple):
        if centrality_type == "b_cent":
            return nx.betweenness_centrality_source(*G_normalized_weight_sources_tuple)
        elif centrality_type == "c_cent":
            return nx.closeness_centrality_source(*G_normalized_weight_sources_tuple)

    def betweenness_centrality_parallel(G, processes=None):
        p = Pool(processes=processes)
        node_divisor = len(p._pool) * 4
        node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
        num_chunks = len(node_chunks)
        bt_sc = p.map(_betmap,
                      zip([G] * num_chunks,
                          [True] * num_chunks,
                          [None] * num_chunks,
                          node_chunks))
        bt_c = bt_sc[0]
        for bt in bt_sc[1:]:
            for n in bt:
                bt_c[n] += bt[n]
        return bt_c

    def closeness_centrality_parallel(G, processes=None):
        p = Pool(processes=processes)
        node_divisor = len(p._pool) * 4
        node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
        num_chunks = len(node_chunks)
        bt_sc = p.map(_betmap,
                      zip([G] * num_chunks,
                          [True] * num_chunks,
                          [None] * num_chunks,
                          node_chunks))
        bt_c = bt_sc[0]
        for bt in bt_sc[1:]:
            for n in bt:
                bt_c[n] += bt[n]
        return bt_c
        '''