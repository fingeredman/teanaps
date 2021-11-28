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
import math
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import random

class GraphVisualizer():  
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

    def draw_radar(self, data_meta, graph_meta):
        # Data
        data = [{
            'type': 'scatterpolar',
            'fill': 'toself',
            'r': data_meta["r"],
            'theta': data_meta["label"]
        }]
        layout = {
            "title": graph_meta["title"],
            "polar": {
                "radialaxis": {
                    "visible": True, 
                    "range": [min(data_meta["r"])*1.05, max(data_meta["r"])*1.05]
                    #"range": [-1,0.5]
                    }
                },
                "showlegend": False,
            "images": self.watermark_image
        }
        fig = go.Figure(data=data, layout=layout)
        self.set_plotly()
        iplot(fig, filename=graph_meta["title"])

    def draw_histogram(self, data_meta_list, graph_meta):
        # Data
        data_list = []
        for data_meta in data_meta_list:
            data = {
                "name": data_meta["data_name"],
                #"type": "histogram",
                "type": data_meta["graph_type"],
                "x": data_meta["x_data"],
                "y": data_meta["y_data"],
                "yaxis": data_meta["y_axis"],
                #"histfunc": "sum"
            }
            if data["type"] == "histogram":
                data["histfunc"] = "sum"
            data_list.append(data)
        # Graph
        graph_meta = {
            "title": graph_meta["title"],
            "xaxis": {
                "exponentformat": "e",
                "showexponent": "all",
                "showticklabels": True,
                "tickangle": graph_meta["x_tickangle"],
                "tickfont": {"color": "black", "size": 10},
                "title": graph_meta["x_name"],
                "titlefont": {"color": "black", "size": 10}
            },
            "yaxis1": {
                "showticklabels": True,
                "side": "left",
                "tickangle": graph_meta["y1_tickangle"],
                "tickfont": {"color": "black", "size": 10},
                "title": graph_meta["y1_name"],
                "titlefont": {"color": "black", "size": 10}
            },
            "yaxis2": {
                "overlaying": "y1",
                "showticklabels": True,
                "side": "right",
                "tickangle": graph_meta["y2_tickangle"],
                "tickfont": {"color": "black", "size": 10},
                "title": graph_meta["y2_name"],
                "titlefont": {"color": "black", "size": 10}
            },
            "images": self.watermark_image
        }
        fig = go.Figure(data=data_list, layout=graph_meta)
        self.set_plotly()
        return iplot(fig, filename=graph_meta["title"])
    
    def draw_line_graph(self, data_meta_list, graph_meta):
        # Data
        data_list = []
        for data_meta in data_meta_list:
            data = {
                "name": data_meta["data_name"],
                "type": "scatter",
                "x": data_meta["x_data"],
                "y": data_meta["y_data"],
                "yaxis": data_meta["y_axis"],
            }
            data_list.append(data)
        # Graph
        graph_meta = {
            "title": graph_meta["title"],
            "xaxis": {
                "exponentformat": "e",
                "showexponent": "all",
                "showticklabels": True,
                "tickangle": graph_meta["x_tickangle"],
                "tickfont": {"color": "black", "size": 10},
                "title": graph_meta["x_name"],
                "titlefont": {"color": "black", "size": 10}
            },
            "yaxis1": {
                "showticklabels": True,
                "side": "left",
                "tickangle": graph_meta["y1_tickangle"],
                "tickfont": {"color": "black", "size": 10},
                "title": graph_meta["y1_name"],
                "titlefont": {"color": "black", "size": 10}
            },
            "yaxis2": {
                "overlaying": "y1",
                "showticklabels": True,
                "side": "right",
                "tickangle": graph_meta["y2_tickangle"],
                "tickfont": {"color": "black", "size": 10},
                "title": graph_meta["y2_name"],
                "titlefont": {"color": "black", "size": 10}
            },
            "images": self.watermark_image
        }
        fig = go.Figure(data=data_list, layout=graph_meta)
        self.set_plotly()
        return iplot(fig, filename=graph_meta["title"])

    def draw_matrix(self, data_meta, graph_meta):
        # Data
        data_meta = {
            "colorbar": {
                "thickness": 15,
                "ticks": "outside",
                "title": data_meta["colorbar_title"],
                "titleside": "right",
                "xanchor": "left"
            },
            "type": "heatmap",
            "x": data_meta["x_data"],
            "y": data_meta["y_data"],
            "z": data_meta["z_data"]
        }
        data_list = [data_meta]
        # Graph
        graph_meta = {
            "title": graph_meta["title"],
            "height": 1000, 
            "width": 1000,
            "yaxis": {
                "tickangle": graph_meta["y_tickangle"],
                "title": graph_meta["y_name"],
            },
            "xaxis": {
                "tickangle": graph_meta["x_tickangle"],
                "title": graph_meta["x_name"],
            },
            "images": self.watermark_image
        }
        fig = go.Figure(data=data_list, layout=graph_meta)
        self.set_plotly()
        return iplot(fig, filename='labelled-heatmap')
    
    def draw_scatter(self, data_meta_list, graph_meta, mode="markers"):
        color_list = con.COLOR_CODE_LIST
        # Data
        data_list = []
        for i, data_meta in enumerate(data_meta_list):
            data = {
                "name": data_meta["data_name"],
                "mode": mode,
                "x": data_meta["x_data"],
                "y": data_meta["y_data"],
                "text": data_meta['label'],
                "marker": {"color": color_list[i], "size": 10}
            }
            data_list.append(data)
        # Graph
        layout = {
            "title": graph_meta["title"],
            "xaxis": {
                "title": graph_meta["x_name"],
                "exponentformat": "e",
                "showexponent": "all",
                "showticklabels": True,
                #"type": "log",
            },
            "yaxis": {
                "title": graph_meta["y_name"],
                "showticklabels": True,
                #"type": "log"    
            },
            "width": 1000,
            "height": 1000,
            "images": self.watermark_image
        }
        fig = go.Figure(data=data_list, layout=layout)
        self.set_plotly()
        return iplot(fig, filename=graph_meta["title"])
    
    def draw_sentence_tree(self, sentence, label_list, edge_list):
        # Generate Graph
        label_len = len(label_list)
        G = Graph()
        G.add_vertices(label_len)
        G.add_edges(edge_list)
        layout = G.layout("rt", root=[0, 1, 2, 3], rootlevel=[1, 2, 2, 2])
        position = {k: layout[k] for k in range(label_len)}
        Y = [layout[k][1] for k in range(label_len)]
        M = max(Y)
        E = [e.tuple for e in G.es]
        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2*M-position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        # Data
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]
        edge_data = go.Scatter(x=Xe, y=Ye, mode="lines", line=dict(color="rgb(210, 210, 210)", width=1), hoverinfo="none")
        node_data = go.Scatter(x=Xn, y=Yn, mode="markers", name="bla", 
                               marker=dict(symbol="circle", size=1, color="rgb(250,250,250)", 
                                           line=dict(color="rgb(50,50,50)", width=2)),
                               text=label_list, hoverinfo="text", opacity=0.8)
        font_size=10
        font_color="rgb(10, 10, 10)"
        annotation_list = []
        for k in range(L):
            annotation_list.append(dict(text=label_list[k], x=position[k][0], y=2*M-position[k][1], textangle=0,
                                        xref='x1', yref='y1', font=dict(color=font_color, size=font_size), showarrow=False))
        # Graph
        graph_meta = {"height": 300, "width": 20*len(sentence) if len(sentence) > 50 else 1000,
                      "annotations": annotation_list, "xaxis": {}, "yaxis": {}}
        graph_meta["xaxis"]["showgrid"] = False
        graph_meta["xaxis"]["showline"] = False
        graph_meta["xaxis"]["showticklabels"] = False
        graph_meta["xaxis"]["zeroline"] = False
        graph_meta["yaxis"]["showgrid"] = False
        graph_meta["yaxis"]["showline"] = False
        graph_meta["yaxis"]["showticklabels"] = False
        graph_meta["yaxis"]["zeroline"] = False
        graph_meta["showlegend"] = False
        graph_meta["barmode"] = "stack"
        graph_meta["showlegend"] = False
        graph_meta["margin"] = {"b": 30, "l": 20, "r": 20, "t": 10}
        graph_meta["images"] = self.watermark_image
        fig = go.Figure(data=[edge_data, node_data], layout=graph_meta)
        self.set_plotly()
        return iplot(fig, filename="SENTENCE TREE")
    