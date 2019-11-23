from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly.plotly as py
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

from IPython.display import display

class GraphVisualizer():  
    def __init__(self):
        None
        
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
                "yaxis": data_meta["y_axis"]
            }
            if data["type"] == "histogram":
                data["histfunc"] = "sum"
            data_list.append(data)
        # Graph
        layout = {
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
            }
        }
        fig = go.Figure(data=data_list, layout=layout)
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
            }
        }
        fig = go.Figure(data=data_list, layout=graph_meta)
        return iplot(fig, filename='labelled-heatmap')
    
    def draw_scatter(self, data_meta_list, graph_meta):
        # Data
        data_list = []
        for data_meta in data_meta_list:
            data = {
                "name": data_meta["data_name"],
                "mode": "markers",
                "x": data_meta["x_data"],
                "y": data_meta["y_data"]
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
        }
        fig = go.Figure(data=data_list, layout=layout)
        return iplot(fig, filename=graph_meta["title"])