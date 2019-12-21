from teanaps.text_analysis import TfidfCalculator
from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

from IPython.display import display

from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

import matplotlib.cm as cm
import matplotlib

import pandas as pd
import numpy as np
from collections import OrderedDict

class DocumentClustering():  
    def __init__(self):
        self.stopword_list = self.__get_stopwords()
        self.tfidf = TfidfCalculator()
    
    def __get_tfidf_matrix(self, document_list):
        self.tfidf.calculation_tfidf(document_list)
        tfidf_matrix = self.tfidf.get_tfidf_matrix()
        return tfidf_matrix
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    
    def kmeans_clustering(self, document_list, num_cluters, num_init, max_iterations):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        km = KMeans(n_clusters = num_cluters, init="k-means++", n_init=num_init, max_iter=max_iterations, random_state=0)
        predict_list = km.fit_predict(tfidf_matrix)
        inertia = km.inertia_
        return {"inertia": inertia, "predict_list": predict_list}
    
    def inertia_transition(self, document_list, max_cluters, num_init, max_iterations):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        inertia_list = []
        for num_clutsers in range(1, max_cluters+1):
            km = KMeans(n_clusters = num_clutsers, init="k-means++", n_init=num_init, max_iter=max_iterations, random_state=0)
            km.fit(tfidf_matrix)
            inertia_list.append(km.inertia_)
        return inertia_list
    
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
        
    def get_dendrogram_graph(self, document_list):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        similarity_matrix = 1 - cosine_similarity(tfidf_matrix)
        names = [str(i) for i in range(len(similarity_matrix))]
        fig = ff.create_dendrogram(similarity_matrix, orientation='left', labels=names)
        fig['layout'].update({'width':1000, 'height':1500})
        return iplot(fig, filename='dendrogram_with_labels')
    
    def get_pair_wize_matrix(self, document_list):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        similarity_matrix = 1 - cosine_similarity(tfidf_matrix)
        x = []
        y = []
        z = []
        for x_index in range(len(similarity_matrix)):
            for y_index in range(len(similarity_matrix[x_index])):
                x.append(x_index)
                y.append(y_index)
                z.append(similarity_matrix[x_index][y_index])
        trace = go.Heatmap(z=z, x=x, y=y, colorscale='Reds', 
                           colorbar = dict(title = 'Freq.', titleside='right', xanchor='left', thickness=15, ticks = 'outside')
                    )
        layout = go.Layout(width=1000, height=1000)
        data=[trace]
        fig = go.Figure(data=data, layout=layout)
        return  iplot(fig, filename='HEATMAP')
    
    def get_kmeans_graph(self, df_result, label):
        fig = {
            "data": [
                {
                    "x": df_result[df_result[label]==predict]["x"],
                    "y": df_result[df_result[label]==predict]["y"],
                    "name": predict, "mode": "markers",
                } for predict in list(OrderedDict.fromkeys(df_result[label]))
            ],
            "layout": {
                "title": "K-Means Clutering Graph - " + label,
                "xaxis": {"title": "TSNE X"},#, 'type': 'log'},
                "yaxis": {"title": "TSNE Y"},
                "width": 500,
                "height": 500,
            }
        }
        return iplot(fig, filename='GROUPED-SCATTER')
    
    def get_tfidf_tsne(self, document_list, predict_list, df_document_list):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        tsne = TSNE(n_components=2)
        X_tsne = tsne.fit_transform(tfidf_matrix)
        df_tfidf_matrix_tsne = pd.DataFrame(X_tsne, columns=['x', 'y'])
        df_predict = pd.DataFrame(predict_list, columns=['predict'])
        df_result = df_document_list[["label"]].join(df_predict).join(df_tfidf_matrix_tsne)
        return df_result
    
    def get_silhouette_score(self, document_list, df_result, num_clusters):
        X = self.__get_tfidf_matrix(document_list)
        fig = tools.make_subplots(rows=1, cols=2, print_grid=False, subplot_titles=('Silhouette Graph', 'Clutering Graph'))
        # Initialize Silhouette Graph
        fig["layout"]["xaxis1"].update(title="Silhouette Coefficient", range=[-0.1, 1])
        fig["layout"]["yaxis1"].update(title="Cluster Label", showticklabels=False, range=[0, len(X) + (num_clusters + 1) * 10])
        # Compute K-Means Cluster
        clusterer = KMeans(n_clusters=num_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        # Compute Average Silhouette Score
        silhouette_avg = silhouette_score(X, cluster_labels)
        return silhouette_avg
    
    def get_silhouette_graph(self, document_list, df_result, num_clusters):
        X = self.__get_tfidf_matrix(document_list)
        color_list = [
            '#1f77b4',  # muted blue
            '#ff7f0e',  # safety orange
            '#2ca02c',  # cooked asparagus green
            '#d62728',  # brick red
            '#9467bd',  # muted purple
            '#8c564b',  # chestnut brown
            '#e377c2',  # raspberry yogurt pink
            '#7f7f7f',  # middle gray
            '#bcbd22',  # curry yellow-green
            '#17becf'   # blue-teal
        ]
        cmap = cm.get_cmap("Spectral")
        fig = tools.make_subplots(rows=1, cols=2, print_grid=False, subplot_titles=('Silhouette Graph', 'Clutering Graph'))
        # Initialize Silhouette Graph
        fig['layout']['xaxis1'].update(title='Silhouette Coefficient', range=[-0.1, 1])
        fig['layout']['yaxis1'].update(title='Cluster Label', showticklabels=False, range=[0, len(X) + (num_clusters + 1) * 10])
        # Compute K-Means Cluster
        clusterer = KMeans(n_clusters=num_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        # Compute Average Silhouette Score
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", num_clusters, "The average silhouette_score is :", silhouette_avg)
        # Compute the Silhouette Scores for Each Sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        y_lower = 10
        for i in range(num_clusters):
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
            colors = cmap(cluster_labels.astype(float) / num_clusters)
            filled_area = go.Scatter(y=np.arange(y_lower, y_upper),
                                     x=ith_cluster_silhouette_values,
                                     mode='lines',
                                     showlegend=False,
                                     line=dict(width=0.5, color=colors),
                                     fill='tozerox')
            fig.append_trace(filled_area, 1, 1)
            y_lower = y_upper + 10  # 10 for the 0 samples
            # Vertical Line for Average Silhouette Score
            axis_line = go.Scatter(x=[silhouette_avg],
                                   y=[0, len(X) + (num_clusters + 1) * 10],
                                   showlegend=False,
                                   mode='lines',
                                   line=dict(color="red", dash='dash', width =1) )
            fig.append_trace(axis_line, 1, 1)
            # Cluster Graph
            colors = matplotlib.colors.colorConverter.to_rgb(cmap(float(i) / num_clusters))
            colors = 'rgb'+str(colors)
            clusters = go.Scatter(x=df_result['x'], 
                                  y=df_result['y'], 
                                  showlegend=False,
                                  mode='markers',
                                  text=cluster_labels,
                                  marker=dict(color=[color_list[cluster_label] for cluster_label in cluster_labels], size=10)
                                 )
            fig.append_trace(clusters, 1, 2)
            fig['layout']['xaxis2'].update(title='Feature space for the 1st feature', zeroline=False)
            fig['layout']['yaxis2'].update(title='Feature space for the 2nd feature', zeroline=False)
            fig['layout'].update(title="Silhouette Analysis for KMeans Clustering - " + str(num_clusters) + " Cluster")
        return iplot(fig, filename='basic-line')
    
    def get_inertia_transition_graph(self, inertia_list):
        trace = go.Scatter(
            x = [i for i in range(1, len(inertia_list)+1)],
            y = inertia_list,
        )
        layout = go.Layout(
                    title='K-Means Clutering Inertia Transition Graph',
                    xaxis=dict(
                        title='NUMBER of CLUSTER',
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
                        dtick = 1,
                        exponentformat='e',
                        showexponent='all'
                    ),
                    yaxis=dict(
                        title='INERTIA',
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
            width=1000,
            height=500,
        )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig, filename='basic-line')