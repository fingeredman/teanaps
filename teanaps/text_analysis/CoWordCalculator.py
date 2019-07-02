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

import concurrent.futures
from collections import Counter
import itertools
import math

import networkx as nx

class CoWordCalculator():  
    def __init__(self):
        self.tokenized_sentence_list = []
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

    def __calculation_co_word(self, sentence_list):
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
    
    def set_document(self, document_path, pos_list):
        f = open(document_path, encoding="utf-8")
        for line in f:
            line = line.strip()
            words = [w.split("/")[0] for w in line.split(" ") if w.split("/")[3] in pos_list]
            self.tokenized_sentence_list.append(words)
            f.flush()
        f.close()
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    
    def calculation_co_matrix(self):
        word_pair_list = self.__calculation_co_word(self.tokenized_sentence_list)
        self.result_list = [[(first_word, second_word), count] for (first_word, second_word), count in Counter(word_pair_list).items()]
        self.result_list.sort(key=lambda elem: elem[1], reverse=True)
        return self.result_list
    
    def get_co_matrix_graph(self, max_words):
        co_word_list = self.result_list
        x = []
        max_freq = 0
        for co_word, freq in co_word_list[:max_words]:
            first_word = co_word[0]
            second_word = co_word[1]
            if max_freq < freq:
                max_freq = freq
            if first_word not in x:
                x.append(first_word) 
            if second_word not in x:
                x.append(second_word)
        y = x
        z = [[0 for freq in x] for freq in y]
        for co_word, freq in co_word_list[:max_words]:
            first_word = co_word[0]
            second_word = co_word[1]
            #z[x.index(first_word)][y.index(second_word)] = math.log2(freq)
            #z[x.index(first_word)][y.index(second_word)] = math.log10(freq)
            #z[x.index(first_word)][y.index(second_word)] = math.sqrt(freq/max_freq*1000)
            z[x.index(first_word)][y.index(second_word)] = math.sqrt(freq/max_freq)*100
            #z[x.index(first_word)][y.index(second_word)] = math.sqrt(freq)

        trace = go.Heatmap(
                        z=z,
                        x=x,
                        y=y,
                        colorscale=[[0.0, 'rgb(245,245,245)'], 
                                  [0.0511111111111111, 'rgb(254,224,144)'], 
                                  [0.1022222222222222, 'rgb(254,224,144)'],
                                  [0.1533333333333333, 'rgb(254,224,144)'], 
                                  [0.2044444444444444, 'rgb(254,224,144)'], 
                                  [0.2555555555555556, 'rgb(254,224,144)'],
                                  [0.3066666666666666, 'rgb(253,174,97)'],
                                  [0.3577777777777778, 'rgb(244,109,67)'], 
                                  [0.8888888888888888, 'rgb(215,48,39)'],
                                  [1.0, 'rgb(165,0,38)']],
                        colorbar = dict(
                            title = 'Freq.',
                            titleside='right',
                            xanchor='left',
                            thickness=15,
                            #tickmode = 'array',
                            #tickvals = [2,50,98],
                            #ticktext = ['Low','Mid','High'],
                            ticks = 'outside'
                        )
                    )
        layout = go.Layout(
            #autosize=False,
            width=1000,
            height=1000,)
        data=[trace]
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig, filename='labelled-heatmap')
    
    def get_word_network_graph(self, max_words, centrality_type):
        co_word_list = self.result_list
        edge_list = []
        for co_word, freq in co_word_list[:max_words]:
            edge_list.append((co_word[0], co_word[1], freq))
        G = nx.Graph()        
        G.add_weighted_edges_from(edge_list)
        node_count = nx.number_of_nodes(G)
        edge_count = nx.number_of_edges(G)
        #pos = nx.spring_layout(G)
        pos = nx.random_layout(G)
        #pos = nx.circular_layout(G)
        #pos = nx.planar_layout(G)
        #pos = nx.shell_layout(G)

        node_list = nx.nodes(G)
        node_centrality_dict = {
            "b_cent": nx.betweenness_centrality(G),
            "d_cent": nx.degree_centrality(G),
            "c_cent": nx.closeness_centrality(G)
        }

        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5,color='#999'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlOrRd',
                reversescale=True,
                color=[],
                size=[math.sqrt(node_centrality_dict[centrality_type][node])*100 for node in G.nodes()],
                colorbar=dict(
                    thickness=15,
                    title='Node Centrality',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=1, color="black")))

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        for node, adjacencies in enumerate(G.adjacency()):
            node_trace['marker']['color']+=tuple([len(adjacencies[1])])
            node_info = "Node: "+str(adjacencies[0])+'<br>'+centrality_type+": "+str(node_centrality_dict[centrality_type][adjacencies[0]])
            node_trace['text']+=tuple([node_info])

        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='Network Graph',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        width=1000,
                        height=1000,
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        return iplot(fig, filename='networkx')