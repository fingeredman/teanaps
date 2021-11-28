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

from igraph import Graph
import networkx as nx
import numpy as np
import math
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import random
from PIL import Image

class TextVisualizer():  
    def __init__(self):
        self.watermark_image = [{
            "source": con.WATERMARK_URL,
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": 0.6,
            "sizex": 0.7,
            "sizey": 0.7,
            "xanchor": "center",
            "yanchor": "center",
            "opacity": 0.1,
            "layer": "above"
        }]
        
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
    
    def draw_sentence_attention(self, token_list, weight_list):
        # Normalize
        max_len = 50
        polarity_list = [1 if weight > 0 else -1 for weight in weight_list]
        weight_list = [abs(weight) for weight in weight_list]
        normalized_weight_list = [(weight)/(max(weight_list)) for weight in weight_list]
        temp_len = 0
        temp_token_list = []
        tokenized_token_list = []
        for i, token in enumerate(token_list):
            if temp_len+len(token) <= max_len:
                temp_len += len(token)
                temp_token_list.append(token)
                if i+1 == len(token_list):
                    tokenized_token_list.append(temp_token_list)
            else:
                tokenized_token_list.append(temp_token_list)
                temp_len = 0
                temp_token_list = [token]
        # Data
        fig = plotly.tools.make_subplots(rows=len(tokenized_token_list), cols=1, print_grid=False)
        annotations = []
        for tokenized_index, token_list in enumerate(tokenized_token_list):
            tokenized_weight_list = normalized_weight_list[:len(token_list)]
            tokenized_polarity_list = polarity_list[:len(token_list)]
            normalized_weight_list = normalized_weight_list[len(token_list):]
            polarity_list = polarity_list[len(token_list):]
            token_len_list = [len(token) for token in token_list]
            token_len_list += [1 for i in range(max_len-sum(token_len_list))]
            tokenized_weight_list += [0 for i in range(len(token_len_list) - len(tokenized_weight_list))]
            tokenized_polarity_list += [0 for i in range(len(token_len_list) - len(tokenized_polarity_list))]
            xaxis = "x" + str(tokenized_index + 1)
            yaxis = "y" + str(tokenized_index + 1)
            char_list = []
            for token in token_list:
                char_list += token
            for char_index, char in enumerate(char_list):
                annotations.append(dict(xref=xaxis, yref=yaxis, 
                                        x=char_index+0.5, y=1, text=char, align="left",
                                        font=dict(family="Arial", size=14, color="black"), showarrow=False))
            data = []
            for token_len, weight, polarity in zip(token_len_list, tokenized_weight_list, tokenized_polarity_list):
                if polarity < 0:
                    block = go.Bar(
                        y=[1], x=[token_len], orientation="h", width=0.5,                    
                        text=str(round(weight, 2)) if weight != 0 else "", hoverinfo='text',
                        marker=dict(color="rgb(" + str(255) + ", " + str(255-(abs(weight)*150)) + ", " + str(255-(abs(weight)*150)) + ")")
                    )
                else:
                    block = go.Bar(
                        y=[1], x=[token_len], orientation="h", width=0.5,                    
                        text=str(round(weight, 2)) if weight != 0 else "", hoverinfo='text',
                        marker=dict(color="rgb(" + str(255-(abs(weight)*200)) + ", " + str(255-(abs(weight)*100)) + ", " + str(255) + ")")
                    )
                data.append(block)
            for trace in data:
                trace["xaxis"] = xaxis
                trace["yaxis"] = yaxis
                fig.append_trace(trace, tokenized_index+1, 1)
        # Graph
        graph_meta = fig["layout"]
        for axis in graph_meta.keys():
            graph_meta[axis]["showgrid"] = False
            graph_meta[axis]["showline"] = False
            graph_meta[axis]["showticklabels"] = False
            graph_meta[axis]["zeroline"] = False
        graph_meta["barmode"] = "stack"
        graph_meta["showlegend"] = False
        graph_meta["margin"] = {"b": 30, "l": 20, "r": 20, "t": 10}
        graph_meta["annotations"] = annotations
        graph_meta["height"] = 30 + (50*len(tokenized_token_list))
        graph_meta["images"] = self.watermark_image
        self.set_plotly()
        return iplot(fig, filename="SENTENCE ATTENTION")
    
    def draw_wordcloud(self, data_meta, graph_meta):
        weight_dict = data_meta["weight_dict"]
        if graph_meta["mask_path"] is None:
            mask_image = Image.open(con.WORDCLOUD_MASK_PATH)
        else:
            mask_image = Image.open(graph_meta["mask_path"]).convert("RGB")
        mask = np.array(mask_image)
        word_list = []
        for word, frequency in weight_dict.items():
            for i in range(int(frequency)):
                word_list.append(word)
        random.shuffle(word_list)
        word_string = ""
        for word in word_list:
            word_string += word + " "
        word_string = word_string.strip()
        wc = WordCloud(font_path=con.WORDCLOUD_FONT_PATH, background_color=graph_meta["background_color"], \
                       mask=mask, margin=graph_meta["margin"], min_font_size=graph_meta["min_font_size"], \
                       max_font_size=graph_meta["max_font_size"], width=graph_meta["width"], height=graph_meta["height"])
        wc.generate(word_string)

        plt.figure(figsize=(20, 20))
        #plt.imshow(wc, interpolation="bilinear")
        image_colors = ImageColorGenerator(mask)
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        
        if graph_meta["mask_path"] is None:
            wordcloud_watermark_image = Image.open(con.WORDCLOUD_WATERMARK_PATH)
            wordcloud_watermark_image = wordcloud_watermark_image.resize(mask_image.size)
            wordcloud_watermark = np.array(wordcloud_watermark_image)
            plt.imshow(wordcloud_watermark, alpha=1.0)
        plt.axis("off")
        plt.show()
                
    def draw_network(self, data_meta, graph_meta, mode="text+markers", node_size_rate=10, edge_width_rate=10, text_size_rate=10):
        # Generate Graph
        node_list = data_meta["node_list"]
        edge_list = data_meta["edge_list"]
        weight_dict = data_meta["weight_dict"]
        G = nx.Graph()
        G.add_weighted_edges_from(edge_list)
        pos = nx.spring_layout(G)
        '''
        #edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5, color='#999'), hoverinfo='none', mode='lines')
        edge_trace = go.Scatter(x=[], y=[], line=dict(width=50, color='#999'), hoverinfo='none', mode='lines')
                
        pos = nx.spring_layout(G)
        # Data
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
            print(edge[0], edge[1], G.get_edge_data(edge[0], edge[1])['weight'])
            #edge_trace['line']['width'] += tuple([G.get_edge_data(edge[0], edge[1])['weight']])
            #edge_trace['line']['width'] += [10]
        
        print("edge_trace", edge_trace)
        '''
        
        #
        # Data
        edge_trace_list = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace = go.Scatter(x=[], y=[], line=dict(width=G.get_edge_data(edge[0], edge[1])['weight']/edge_width_rate, color='#999'), mode='lines')
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
            edge_trace_list.append(edge_trace)
            
            middle_node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text', marker=go.Marker(opacity=0))
            middle_node_trace['x'].append((x0+x1)/2)
            middle_node_trace['y'].append((y0+y1)/2)
            middle_node_trace['text']+=["strength: " + str(G.get_edge_data(edge[0], edge[1])['weight'])]
            edge_trace_list.append(middle_node_trace)
            #edge_trace['line']['width'] += tuple([G.get_edge_data(edge[0], edge[1])['weight']])
            #edge_trace['line']['width'] += [10]
        
        
        #
        #node_trace = go.Scatter(x=[], y=[], text=[], mode=mode, hoverinfo='text', 
        node_trace = go.Scatter(x=[], y=[], text=[], mode=mode, hoverinfo='hovertext', hovertext=[], 
                                #line=dict(width=500, color='#888'),
                                hoverlabel=dict(namelength=0), # remove trace+number label
                                marker=dict(showscale=True, colorscale='YlOrRd', reversescale=True, color=[],
                                            #size=[math.sqrt(weight_dict[node])*100 for node in node_list],
                                            size=[], 
                                            #colorbar=dict(thickness=15, title=graph_meta["weight_name"], xanchor='left', 
                                            colorbar=dict(thickness=15, title=graph_meta["weight_name"], xanchor='left', 
                                                          titleside='right'), 
                                            line=dict(width=1, color="black")))
        for node in node_list:
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
        for node, adjacencies in enumerate(G.adjacency()):
            #node_trace['marker']['color']+=tuple([len(adjacencies[1])])
            node_trace['marker']['color']+=tuple([math.sqrt(weight_dict[adjacencies[0]])*node_size_rate])
            #node_trace['marker']['size']+=tuple([math.sqrt(weight_dict[adjacencies[0]])*node_size_rate])
            node_trace['marker']['size']+=tuple([weight_dict[adjacencies[0]]*node_size_rate**2])
            #node_info = "Node: " + str(adjacencies[0]) + "<br>weight: " + str(weight_dict[adjacencies[0]])
            #node_trace['text']+=tuple([node_info])
            node_info = str(adjacencies[0])
            hover_info = "Node: " + str(adjacencies[0]) + "<br>weight: " + str(weight_dict[adjacencies[0]])
            node_trace['text']+=tuple([node_info])
            node_trace['hovertext']+=tuple([hover_info])
        
        text_trace_list = []
        if mode == "text":
            text_trace = go.Scatter(
                                    x=node_trace['x'],
                                    y=node_trace['y'],
                                    mode="text",
                                    #name="Lines, Markers and Text",
                                    text=node_trace['text'],
                                    #textposition="top right",
                                    textfont=dict(
                                        #family="sans serif",
                                        size=[s**2/50/text_size_rate for s in node_trace['marker']['size']],
                                        #color="crimson"
                                    )
                                )
            text_trace_list.append(text_trace)
            node_trace['text'] = []
        # Graph
        #fig = go.Figure(data=[edge_trace, node_trace], 
        fig = go.Figure(data=edge_trace_list+[node_trace]+text_trace_list, 
                        layout=go.Layout(title=graph_meta["title"], titlefont=dict(size=16),
                                         showlegend=False, hovermode='closest', images=self.watermark_image,
                                         width=graph_meta["width"], height=graph_meta["height"],margin=dict(b=20,l=5,r=5,t=40),
                                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        self.set_plotly()
        return iplot(fig, filename='WORD NETWORK')