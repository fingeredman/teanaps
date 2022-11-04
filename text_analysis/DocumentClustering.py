from teanaps.text_analysis import TfidfCalculator
from teanaps.visualization import GraphVisualizer
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
from sklearn.cluster import DBSCAN
import hdbscan

import matplotlib.cm as cm
import matplotlib

import pandas as pd
import numpy as np
from collections import OrderedDict

import warnings
warnings.filterwarnings(action='ignore')

class DocumentClustering():  
    def __init__(self):
        self.stopword_list = self.__get_stopwords()
        self.tfidf = TfidfCalculator()
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
    
    def __get_tfidf_matrix(self, document_list):
        self.tfidf.calculation_tfidf(document_list)
        tfidf_matrix = self.tfidf.get_tfidf_matrix()
        return tfidf_matrix
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    
    # .kmeans_clustering() Will be replaced by .clustering()
    def kmeans_clustering(self, document_list, num_cluters, max_iterations):
        print(".kmeans_clustering() Will be replaced by .clustering()")
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        km = KMeans(n_clusters = num_cluters, init="k-means++", n_init=10, max_iter=max_iterations, random_state=0)
        predict_list = km.fit_predict(tfidf_matrix)
        inertia = km.inertia_
        return {"inertia": inertia, "predict_list": predict_list}
    
    def clustering(self, alg, document_list, num_cluters=3, max_iterations=300, eps=0.5, min_samples=5):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        if alg == "kmeans":
            km = KMeans(n_clusters = num_cluters, init="k-means++", n_init=10, max_iter=max_iterations, random_state=0)
            predict_list = km.fit_predict(tfidf_matrix)
            inertia = km.inertia_
        if alg == "dbscan":
            dbs = DBSCAN(eps=eps, min_samples=min_samples)
            predict_list = dbs.fit_predict(tfidf_matrix)
            inertia = None
        if alg == "hdbscan":
            hdbs = hdbscan.HDBSCAN(min_cluster_size=min_samples)
            predict_list = hdbs.fit_predict(tfidf_matrix)
            inertia = None
        return {"inertia": inertia, "predict_list": predict_list}
    
    # .inertia_transition() Will be replaced by .kmeans_inertia_transition()
    def inertia_transition(self, document_list, max_cluters, max_iterations):
        print(".inertia_transition() Will be replaced by .kmeans_inertia_transition()")
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        inertia_list = []
        for num_clutsers in range(1, max_cluters+1):
            km = KMeans(n_clusters = num_clutsers, init="k-means++", n_init=10, max_iter=max_iterations, random_state=0)
            km.fit(tfidf_matrix)
            inertia_list.append(km.inertia_)
        return inertia_list
    
    def kmeans_inertia_transition(self, document_list, max_cluters, max_iterations):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        inertia_list = []
        for num_clutsers in range(1, max_cluters+1):
            km = KMeans(n_clusters = num_clutsers, init="k-means++", n_init=10, max_iter=max_iterations, random_state=0)
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
        fig['layout']["images"] = self.watermark_image
        fig['layout']["title"] = "DENDOGRAM GRAPH"
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
        fig['layout']["images"] = self.watermark_image
        fig['layout']["title"] = "PAIR-WIZE MATRIX"
        self.set_plotly()
        return  iplot(fig, filename='HEATMAP')
    
    # .get_kmeans_graph() Will be replaced by .get_cluster_graph()
    def get_kmeans_graph(self, df_result, label):
        print(".get_kmeans_graph() Will be replaced by .get_cluster_graph()")
        gv = GraphVisualizer()
        gv.set_plotly()
        data_meta_list = []
        for predict in list(OrderedDict.fromkeys(df_result[label])):
            data_meta = {
                "data_name": predict,
                "x_data": df_result[df_result[label]==predict]["x"],
                "y_data": df_result[df_result[label]==predict]["y"],
                "label": predict
            }
            data_meta_list.append(data_meta)
        graph_meta = {
            "title": "K-Means Clutering Graph - " + label,
            "x_name": "TSNE X",
            "y_name": "TSNE Y"
        }
        return gv.draw_scatter(data_meta_list, graph_meta)
    
    def get_cluster_graph(self, df_result, label):        
        gv = GraphVisualizer()
        gv.set_plotly()
        data_meta_list = []
        for i in OrderedDict.fromkeys(df_result[label]):
            content_label_list = []
            for content_label in df_result[df_result.predict==i]["content"]:
                if len(content_label) > 30:
                    content_label = content_label[:30]+"..."
                    content_label_list.append(content_label)
                else:
                    content_label_list.append(content_label)
                
            data_meta = {
                "data_name": i,
                "x_data": df_result[df_result[label]==i]["x"],
                "y_data": df_result[df_result[label]==i]["y"],
                "label": content_label_list
            }
            data_meta_list.append(data_meta)
        graph_meta = {
            "title": "Cluter Graph - " + label,
            "x_name": "TSNE X",
            "y_name": "TSNE Y"
        }
        return gv.draw_scatter(data_meta_list, graph_meta)
        
    def get_tfidf_tsne(self, document_list, predict_list, df_document_list):
        tfidf_matrix = self.__get_tfidf_matrix(document_list)
        tsne = TSNE(n_components=2)
        X_tsne = tsne.fit_transform(tfidf_matrix)
        #DF_DOCUMENT_LIST = df_article = pd.DataFrame(document_list, columns = ["label", "source", "datetime", "title", "content"])
        df_tfidf_matrix_tsne = pd.DataFrame(X_tsne, columns=['x', 'y'])
        df_predict = pd.DataFrame(predict_list, columns=['predict'])
        df_token = pd.DataFrame(document_list, columns=['plain text'])
        #df_content = pd.DataFrame(df_document_list, columns=['content'])
        #df_result = df_document_list[["label"]].join(df_predict).join(df_content).join(df_token).join(df_tfidf_matrix_tsne)
        df_result = df_document_list.join(df_predict).join(df_token).join(df_tfidf_matrix_tsne)
        return df_result
    
    # .get_silhouette_score() Will be replaced by .get_silhouette_score2()
    def get_silhouette_score(self, document_list, df_result, num_clusters):
        print(".get_silhouette_score() Will be replaced by .get_silhouette_score2()")
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
    
    # .get_silhouette_score2() Will be replaced by .get_silhouette_score()
    #def get_silhouette_score2(self, alg, document_list, df_document_list, num_clusters=3, eps=0.5, min_samples=5):
    def get_silhouette_score2(self, document_list, df_result):
        print(".get_silhouette_score2() Will be replaced by .get_silhouette_score()")
        X = self.__get_tfidf_matrix(document_list)
        fig = tools.make_subplots(rows=1, cols=2, print_grid=False, subplot_titles=('Silhouette Graph', 'Clutering Graph'))
        '''
        if alg == "kmeans":
            # Compute K-Means Cluster
            clusterer = KMeans(n_clusters=num_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(X)
            # Initialize Silhouette Graph
            fig["layout"]["xaxis1"].update(title="Silhouette Coefficient", range=[-0.1, 1])
            fig["layout"]["yaxis1"].update(title="Cluster Label", showticklabels=False, 
                                           range=[0, len(X) + (num_clusters + 1) * 10])
        if alg == "dbscan":
            # Compute DBSCAN Cluster
            clusterer = DBSCAN(eps=eps, min_samples=min_samples)
            cluster_labels = clusterer.fit_predict(X)
            num_clusters = len(set(cluster_labels))
            # Initialize Silhouette Graph
            fig["layout"]["xaxis1"].update(title="Silhouette Coefficient", range=[-0.1, 1])
            fig["layout"]["yaxis1"].update(title="Cluster Label", showticklabels=False, 
                                           range=[0, len(X) + (num_clusters + 1) * 10])
        if alg == "hdbscan":
            # Compute HDBSCAN Cluster
            clusterer = hdbscan.HDBSCAN(min_cluster_size=min_samples)
            cluster_labels = clusterer.fit_predict(X)
            num_clusters = len(set(cluster_labels))
            # Initialize Silhouette Graph
            fig["layout"]["xaxis1"].update(title="Silhouette Coefficient", range=[-0.1, 1])
            fig["layout"]["yaxis1"].update(title="Cluster Label", showticklabels=False, 
                                           range=[0, len(X) + (num_clusters + 1) * 10])
        '''
        # Compute Silhouette Score
        cluster_labels = df_result["predict"]
        silhouette_avg = silhouette_score(X, cluster_labels)
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        #df_result = self.get_tfidf_tsne(document_list, cluster_labels, df_document_list)
        silhouette_result = {"silhouette_avg": silhouette_avg, "silhouette_score": []}
        for label, content, predict, silhouette in zip(df_result['label'], df_result['content'], 
                                  df_result['predict'], sample_silhouette_values):
            silhouette_result["silhouette_score"].append([str(predict), str(silhouette)[:8], label, content])
        return silhouette_result
    
    # .get_silhouette_graph2() Will be replaced by .get_silhouette_graph()
    #def get_silhouette_graph2(self, alg, document_list, df_document_list, num_clusters=3, eps=0.5, min_samples=5, print_result=False):
    def get_silhouette_graph2(self, document_list, df_result, print_result=False):
        print(".get_silhouette_graph2() Will be replaced by .get_silhouette_graph()")
        X = self.__get_tfidf_matrix(document_list)
        color_list = con.COLOR_CODE_LIST
        '''
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
        '''
        cmap = cm.get_cmap("Spectral")
        fig = tools.make_subplots(rows=1, cols=2, print_grid=False, subplot_titles=('Silhouette Graph', 'Clutering Graph'))
        # Initialize Silhouette Graph
        num_clusters = len(OrderedDict.fromkeys(df_result["predict"]))
        fig['layout']['xaxis1'].update(title='Silhouette Coefficient', range=[-0.1, 1])
        fig['layout']['yaxis1'].update(title='Cluster Label', showticklabels=False, range=[0, len(X) + (num_clusters + 1) * 10])
        '''
        if alg == "kmeans":
            # Compute K-Means Cluster
            clusterer = KMeans(n_clusters=num_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(X)
            # Compute Average Silhouette Score
            silhouette_avg = silhouette_score(X, cluster_labels)
            print("For n_clusters =", num_clusters, "The average silhouette_score is :", silhouette_avg)
        if alg == "dbscan":
            # Compute DBSCAN Cluster
            clusterer = DBSCAN(eps=eps, min_samples=min_samples)
            cluster_labels = clusterer.fit_predict(X)
            # Compute Average Silhouette Score
            silhouette_avg = silhouette_score(X, cluster_labels)
            print("For eps =", eps, "& min_samples =", min_samples, "The average silhouette_score is :", silhouette_avg)
        if alg == "hdbscan":
            # Compute HDBSCAN Cluster
            clusterer = hdbscan.HDBSCAN(min_cluster_size=min_samples)
            cluster_labels = clusterer.fit_predict(X)
            # Compute Average Silhouette Score
            silhouette_avg = silhouette_score(X, cluster_labels)
            print("For min_samples =", min_samples, "The average silhouette_score is :", silhouette_avg)
        '''
        # Compute the Silhouette Scores for Each Sample
        cluster_labels = df_result["predict"]
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", num_clusters, "The average silhouette_score is :", silhouette_avg)
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        #df_result = self.get_tfidf_tsne(document_list, cluster_labels, df_document_list)
        
        y_lower = 10
        for i in OrderedDict.fromkeys(cluster_labels):
            content_label_list = []
            for content_label in df_result[df_result.predict==i]["content"]:
                if len(content_label) > 30:
                    content_label = content_label[:30]+"..."
                    content_label_list.append(content_label)
                else:
                    content_label_list.append(content_label)
                    
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
            #colors = cmap(cluster_labels.astype(float) / num_clusters)
            filled_area = go.Scatter(y=np.arange(y_lower, y_upper),
                                     x=ith_cluster_silhouette_values,
                                     mode='lines',
                                     text=ith_cluster_silhouette_values,
                                     name=i,
                                     showlegend=False,
                                     #line=dict(width=0.5, color=colors),
                                     line=dict(width=0.5, color=color_list[i]),
                                     fill='tozerox')
            fig.append_trace(filled_area, 1, 1)
            y_lower = y_upper + 10  # 10 for the 0 samples
            # Vertical Line for Average Silhouette Score
            axis_line = go.Scatter(x=[silhouette_avg, silhouette_avg],
                                   y=[0, len(X)+(num_clusters + 1)*10],
                                   showlegend=False,
                                   mode='lines',
                                   line=dict(color="red", dash='dash', width =1))
            fig.append_trace(axis_line, 1, 1)
            # Cluster Graph
            #colors = matplotlib.colors.colorConverter.to_rgb(cmap(float(i) / num_clusters))
            #colors = 'rgb'+str(colors)
            clusters = go.Scatter(x=df_result[df_result.predict==i]['x'], 
                                  y=df_result[df_result.predict==i]['y'], 
                                  showlegend=True,
                                  mode='markers',
                                  text=content_label_list,
                                  name=i,
                                  marker=dict(color=color_list[i], size=10)
                                 )
            fig.append_trace(clusters, 1, 2)
            fig['layout']['xaxis2'].update(title='Feature space for the 1st feature', zeroline=False)
            fig['layout']['yaxis2'].update(title='Feature space for the 2nd feature', zeroline=False)
            fig['layout'].update(title="Silhouette Analysis for KMeans Clustering - " + str(num_clusters) + " Cluster")
            fig['layout']["images"] = self.watermark_image
        self.set_plotly()
        if print_result == True:
            for label, content, predict, silhouette in zip(df_result['label'], df_result['content'], 
                                                           df_result['predict'], sample_silhouette_values):
                print(str(predict) + "|" + str(silhouette)[:8] + "|" + label + "|" + content)
        return iplot(fig, filename='basic-line')
    
    # .get_silhouette_graph() Will be replaced by .get_silhouette_graph2()
    def get_silhouette_graph(self, document_list, df_result, num_clusters):
        print(".get_silhouette_graph() Will be replaced by .get_silhouette_graph2()")
        X = self.__get_tfidf_matrix(document_list)
        color_list = con.COLOR_CODE_LIST
        '''
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
        '''
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
            fig['layout']["images"] = self.watermark_image
        self.set_plotly()
        return iplot(fig, filename='basic-line')
    
    # .get_inertia_transition_graph() Will be replaced by .get_kmeans_inertia_transition_graph()
    def get_inertia_transition_graph(self, inertia_list):
        print(".get_inertia_transition_graph() Will be replaced by .get_kmeans_inertia_transition_graph()")
        gv = GraphVisualizer()
        gv.set_plotly()
        x = [i for i in range(1, len(inertia_list)+1)]
        y = inertia_list
        data_meta_list = []
        data_meta = {
            "graph_type": "scatter",
            "data_name": "Y",
            "x_data": x,
            "y_data": y,
            "y_axis": "y1",
        }
        data_meta_list.append(data_meta)
        graph_meta = {
            "title": "K-Means Clutering Inertia Transition Graph",
            "x_tickangle": 0,
            "y1_tickangle": 0,
            "y2_tickangle": 0,
            "x_name": "NUMBER of CLUSTER",
            "y1_name": "INERTIA",
            "y2_name": "Y2",
        }
        return gv.draw_line_graph(data_meta_list, graph_meta)
    
    def get_kmeans_inertia_transition_graph(self, inertia_list):
        gv = GraphVisualizer()
        gv.set_plotly()
        x = [i for i in range(1, len(inertia_list)+1)]
        y = inertia_list
        data_meta_list = []
        data_meta = {
            "graph_type": "scatter",
            "data_name": "Y",
            "x_data": x,
            "y_data": y,
            "y_axis": "y1",
        }
        data_meta_list.append(data_meta)
        graph_meta = {
            "title": "K-Means Clutering Inertia Transition Graph",
            "x_tickangle": 0,
            "y1_tickangle": 0,
            "y2_tickangle": 0,
            "x_name": "NUMBER of CLUSTER",
            "y1_name": "INERTIA",
            "y2_name": "Y2",
        }
        return gv.draw_line_graph(data_meta_list, graph_meta)
