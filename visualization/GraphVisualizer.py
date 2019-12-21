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

from igraph import Graph, EdgeSeq

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
            "opacity": 0.3,
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

    def draw_histogram(self, data_meta_list, graph_meta):
        # Data
        data_list = []
        for data_meta in data_meta_list:
            data = {
                "name": data_meta["data_name"],
                "type": data_meta["graph_type"],
                "x": data_meta["x_data"],
                "y": data_meta["y_data"],
                "yaxis": data_meta["y_axis"],
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
        return iplot(fig, filename='labelled-heatmap')
    
    def draw_scatter(self, data_meta_list, graph_meta, mode="markers"):
        # Data
        data_list = []
        for data_meta in data_meta_list:
            data = {
                "name": data_meta["data_name"],
                "mode": mode,
                "x": data_meta["x_data"],
                "y": data_meta["y_data"],
                "text": data_meta['label']
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
        return iplot(fig, filename=graph_meta["title"])
    
    def draw_sentence_attention(self, token_list, weight_list):
        # Normalize
        max_len = 50
        normalized_weight_list = [weight/max(weight_list) for weight in weight_list]
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
            normalized_weight_list = normalized_weight_list[len(token_list):]
            token_len_list = [len(token) for token in token_list]
            token_len_list += [1 for i in range(max_len-sum(token_len_list))]
            tokenized_weight_list += [0 for i in range(len(token_len_list) - len(tokenized_weight_list))]
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
            for token_len, weight in zip(token_len_list, tokenized_weight_list):
                block = go.Bar(
                    y=[1], x=[token_len], orientation="h", width=0.5,                    
                    text=round(weight, 1) if weight != 0 else "", hoverinfo='text',
                    marker=dict(color="rgb(" + str(255) + ", " + str(255-(weight*200)) + ", " + str(255-(weight*200)) + ")")
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
        return iplot(fig, filename="SENTENCE ATTENTION")
    
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
        return iplot(fig, filename="SENTENCE TREE")