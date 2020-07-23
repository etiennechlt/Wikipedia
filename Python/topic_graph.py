#!/usr/bin/env python
# coding: utf-8

### Extraction of topics from Wikipedia pages ###

import sys
import os
import numpy as np
import networkx as nx
import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import community
from fonctions import *


### Parameters for the following pipeline ###

pd.set_option('mode.chained_assignment', None)



### Making a class to englobe all variables ###
class Parameters:
    ignored_topics = ['Culture.Biography*', 'Compilation.List_Disambig', 'Geography', 'STEM.STEM*']
    
    def __init__(self, region, date_beg, date_end, path='', graph_type='gexf', list_ignored_topics=ignored_topics,                                   prob_threshold=0.1, save=True, plot=False):
        self.region = region
        self.date_beg = date_beg
        self.date_end = date_end
        self.graph_type = graph_type
        self.list_ignored_topics = list_ignored_topics
        self.prob_threshold = prob_threshold
        self.save = save
        self.plot = plot
        if (path == ''):
            self.path = "Results/"+region+"/"+region+"_"+date_beg+"_"+date_end+"/"
        else: 
            self.path = path



### Importing the nodes as a DataFrame for easier manipulations ###

def init_graph(param):
    print("Initializing graph...", end="\r")
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    save = param.save
    
    # Try with default name from SparkWiki
    try:
        graph = nx.read_gexf(path+'peaks_graph_'+date_beg+'_'+date_end+'.gexf')
        graph = nx.Graph(graph)
    except:
        ### With .GEXF ###
        if (graph_type == 'gexf'):
            graph = nx.read_gexf(path+'graph.gexf')
            graph = nx.Graph(graph)

        ### With .GRAPHML ###
        if (graph_type == 'graphml'):
            graph = nx.read_graphml(path+'graph.graphml')


    dataFrame = pd.DataFrame.from_dict(dict(graph.nodes(data=True)), orient='index')
    dataFrame['Id'] = dataFrame.index
    dataFrame.rename(columns={'label': 'Label'}, inplace=True)
    dataFrame['Label'] = dataFrame['Label'].astype('string')
    dataFrame['Id'] = dataFrame['Id'].astype('int64')

    degree = dict(nx.degree(graph, nbunch=None, weight=10))
    partition = community.best_partition(graph, randomize=True, weight='Weight', resolution=1.5)
    btw_cent = nx.betweenness_centrality(graph,normalized=False)


    dataFrame['Degree'] = pd.DataFrame.from_dict(degree, orient='index')[0]
    dataFrame['modularity_class'] = pd.DataFrame.from_dict(partition, orient='index')[0]
    dataFrame['betweenesscentrality'] = pd.DataFrame.from_dict(btw_cent, orient='index')[0]


    dataFrame.sort_values(by = ['modularity_class'], inplace=True, ascending = [True])
    dataFrame.sort_values(by = ['Id'], inplace=True, ascending = [True])
    
    if (save == True):
        dataFrame.to_csv(path + 'nodes.csv', encoding='utf-8')
        
    sys.stdout.write("\033[K")
    print("Initializing graph: Done")
    
    return dataFrame





### Associate the 'Qid' value of Wikipedia pages in the DataFrame ###
### Give '-1' value if an error has occured during the query      ###

def match_Qids(param):
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    save = param.save
    
    dataFrame = pd.read_csv(path + 'nodes.csv')
    
    # URL for the quieries
    urls = "https://"+region+".wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&pageids="

    i=0
    Nb_pages = len(dataFrame)
    for pageId in np.int64(dataFrame['Id']):
        response = requests.get(urls + str(pageId)).json()
        try:
            Qid = (list(findkeys(response, 'wikibase_item'))[0])
            Title = (list(findkeys(response, 'title'))[0])
        except IndexError:
            dataFrame.loc[dataFrame['Id'] == pageId, 'Qid'] = '-1'
            i+=1
            # Loading display
            print("Matching Qids:", i,"/", Nb_pages, dataFrame.loc[dataFrame['Id'] == pageId, 'Label'], "\t error", end="\r")
            sys.stdout.flush()

        else:
            dataFrame.loc[dataFrame['Id'] == pageId, 'Qid'] = Qid
            dataFrame.loc[dataFrame['Id'] == pageId, 'Label'] = Title
            i+=1
            # Loading display
            sys.stdout.write("\033[K")
            print("Matching Qids:", i,"/", Nb_pages, dataFrame.loc[dataFrame['Id'] == pageId, 'Label'].values[0], end="\r")
    # Save the DataFrame with their associated Qids
    if (save ==True):
        dataFrame.to_csv(path + 'pages_Qids.csv', encoding='utf-8')
    
    sys.stdout.write("\033[K")
    print("Matching Qids: Done")    
        
    return dataFrame






### Extracting topic pages from database API ###

def match_topic(param):
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    save = param.save
    
    dataFrame = pd.read_csv(path + 'pages_Qids.csv')
    Match_topic_API = pd.DataFrame()

    ### The API's URL from the topic is extracted ###         
    urls = "http://86.119.25.229:5000/api/v1/wikidata/topic?qid="
    

    a=0 
    n = dataFrame.index[-1]
    for pageIndex in dataFrame.index:
        pageQid = dataFrame.at[pageIndex, 'Qid']
        pageModularity = dataFrame.at[pageIndex, 'modularity_class']
        response = requests.get(urls + pageQid + "&threshold=" + '0.1').json()
        scores = list(findkeys(response, 'score'))
        topics = list(findkeys(response, 'topic'))
        try:
            page_title = response['name']
        except KeyError:
            page_title = dataFrame.at[pageIndex, 'Label']
        for i in range(len(scores)):
            page = dataFrame.iloc[pageIndex]
            page['Topic'] = topics[i]
            page['Probability'] = scores[i]
            Match_topic_API = Match_topic_API.append(page, ignore_index=True)
        a+=1
        # Loading display
        sys.stdout.write("\033[K")
        print("Matching topics:", a, "/",n, " ",page_title, end="\r")

    Match_topic_API.drop(columns = ['Unnamed: 0'], inplace = True )
   
    # Save the results with their associated topics
    if (save==True):
        Match_topic_API.to_csv(path + 'pages_topic.csv', encoding='utf-8')

    sys.stdout.write("\033[K")
    print("Matching topics: Done")
    
    return Match_topic_API







### Counting the number of views per page using pageviews.toolforge.org API ###
def count_views(param):
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    save = param.save
    
    df = pd.read_csv(path + 'pages_topic.csv', index_col = 'Unnamed: 0')

    urls = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+region+".wikipedia/all-access/all-agents/"

    i=0
    list_id = list(dict.fromkeys(df['Id']))
    Nb_pages = len(list_id)

    for pageId in list_id:
        label = df.loc[df['Id'] == pageId, 'Label'].max()
        label = label.replace(" ", "_")
        try:
            response = requests.get(urls+label+"/daily/"+date_beg+"/"+date_end ).json()
            views = np.sum(list(findkeys(response, 'views')))
        except KeyError:
            df.loc[df['Id'] == pageId, 'Views'] = 0
            i+=1
            # Loading display
            sys.stdout.write("\033[K")
            print("Counting views:", i,"/", Nb_pages, "Error", end="\r")
        else:
            df.loc[df['Id'] == pageId, 'Views'] = views
            i+=1
            # Loading display
            sys.stdout.write("\033[K")
            print("Counting views:", i,"/", Nb_pages, label," views: ", views, end="\r")

    # Save the DataFrame with their associated views
    if (save==True):
        df.to_csv(path + 'pages_views.csv', encoding='utf-8')
        
    sys.stdout.write("\033[K")
    print("Counting views: Done")
    
    return df








### Saving to nodes attributes into the graph ###
def save_graph_attributes(param):
    print("Saving graph attributes...", end="\r")
    
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    save = param.save
    list_ignored_topics = param.list_ignored_topics
    prob_threshold = param.prob_threshold
    
   # Try with default name from SparkWiki
    try:
        graph = nx.read_gexf(path+'peaks_graph_'+date_beg+'_'+date_end+'.gexf')
        graph = nx.Graph(graph)
    except:
        ### With .GEXF ###
        if (graph_type == 'gexf'):
            graph = nx.read_gexf(path+'graph.gexf')
            graph = nx.Graph(graph)

        ### With .GRAPHML ###
        if (graph_type == 'graphml'):
            graph = nx.read_graphml(path+'graph.graphml')


    df = pd.read_csv(path + 'pages_views.csv', index_col = 'Unnamed: 0')
    df.rename_axis("Index", inplace=True)    

    nodes = pd.DataFrame()

    df = weight_topic(df, list_ignored_topics)
    string_topic_separator(df)

    df.sort_values(by = ['Id', 'Weight'], inplace=True, ascending = [True, False])

    list_id = list(dict.fromkeys(df['Id']))

    # Keeping only the node with the higher Weight and threshold them with lower 'Probability' (~confidence)
    for Id in list_id:
        page_max = df.loc[(df['Id'] == Id) & (df['Probability'] > prob_threshold), 'Weight']
        if (page_max.empty == True):
            id_max = df.loc[df['Id'] == Id, 'Probability'].idxmax()
        else :
            id_max = page_max.idxmax()
        nodes = nodes.append(df.loc[df.index == id_max], ignore_index=True)

    add_graph_attribute(graph, nodes, 'Degree')
    add_graph_attribute(graph, nodes, 'modularity_class')
    add_graph_attribute(graph, nodes, 'betweenesscentrality')
    add_graph_attribute(graph, nodes, 'Qid')
    add_graph_attribute(graph, nodes, 'Topic')
    add_graph_attribute(graph, nodes, 'Main topic')
    add_graph_attribute(graph, nodes, 'Subtopic')
    add_graph_attribute(graph, nodes, 'Weight')
    add_graph_attribute(graph, nodes, 'Views')

        
    # Save the graph
    nx.write_gexf(graph, path + 'filled_graph.gexf')  

        
    # Save the result
    if (save==True):
        nodes.to_csv(path + 'filled_nodes.csv', encoding='utf-8')
    
    sys.stdout.write("\033[K")
    print("Saving graph attributes: Done")
    
    return graph

    
    
    



### Display a bar chart of the repartition of topics per cluster ###
### Save the number of each topic per cluster and their ratio ###
### Note : here only ignore 'Culture.Biography' topic ###

def count_topic_per_cluster(param):
    print("Counting topics per clusters...", end="\r")
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    save = param.save
    plot = param.plot
    
    # Create a folder for the figures
    try:
        os.mkdir(path+'Figures')
    except:
        pass
    
    nodes = pd.read_csv(path + 'filled_nodes.csv', index_col = 'Unnamed: 0')

    list_cluster_topic = pd.DataFrame()

    nb_cluster = int( nodes['modularity_class'].max() ) + 1
    for cluster_id in range(nb_cluster):
        df = nodes.loc[(nodes['modularity_class'] == cluster_id) & (~nodes['Topic'].str.contains('Culture.Biography'))]
         # Avoid clusters without topics
        if (df.empty == True):
            df = nodes.loc[(nodes['modularity_class'] == cluster_id)]

        # Counting each topic and make a ratio over the total 
        df['Count'] = 1
        cluster = df.groupby(['Subtopic']).sum()['Count']
        df_cluster = pd.DataFrame(cluster)
        df_cluster['modularity_class'] = cluster_id
        df_cluster['Percentage'] = (cluster / cluster.sum() * 100).round(decimals=1)
        df_cluster['Subtopic'] = df_cluster.index
        df_cluster.set_index('modularity_class', inplace=True)
        df_cluster.sort_values(by = ['Count'], ascending = [False], inplace=True)
        df_cluster = df_cluster[['Subtopic', 'Percentage', 'Count']]
        list_cluster_topic = list_cluster_topic.append(df_cluster, ignore_index=False)

        
        plt.figure(cluster_id)
        # Making descending lists for plotting
        labels = list(df_cluster['Subtopic'])[::-1]
        ratio = list(df_cluster['Percentage'])[::-1]

        ind = np.arange(len(ratio))  
        height = 0.8

        fig1, ax1 = plt.subplots()
        ax1.barh(ind, ratio, height=height, align='center')

        # Labeling everything
        ax1.set_yticks(ind)
        ax1.set_yticklabels(labels)
        for i, v in enumerate(ratio):
            ax1.text(v, i, " "+str(v), color='black', va='center')
        plt.xlabel('Percentage')
        plt.ylabel('Topics')
        plt.title('Cluster ' + str(cluster_id))
        plt.savefig(path+'Figures/Cluster_' + str(cluster_id)+'.png', bbox_inches='tight', transparent=False, pad_inches=0.1)
        if (plot == True):
            plt.show()
        plt.close(cluster_id)
        
    # Save the result
    if (save == True):
        list_cluster_topic.to_csv(path + 'list_cluster_topic.csv', encoding='utf-8')
    
    sys.stdout.write("\033[K")
    print("Counting topics per clusters: Done")
    
    return list_cluster_topic






def translate_label(param):
    print("Translating label...", end="\r")
    from googletrans import Translator
    translator = Translator()
    region = param.region
    date_beg = param.date_beg
    date_end = param.date_end
    path = param.path
    graph_type = param.graph_type
    
     # Try with default name from SparkWiki
    try:
        graph = nx.read_gexf(path+'filled_graph.gexf')
        graph = nx.Graph(graph)
    except:
        print("Error: filled_graph.gexf not found")
        return
    
    df = pd.read_csv(path + 'filled_nodes.csv', index_col = 'Unnamed: 0')
    i=0
    n=df['Label'].size
    

    if region == 'ZH':
        for label in df['Label']:
            word_to_translate = label
            label_en = vars(translator.translate(word_to_translate, src='zh-cn', dest='en'))['text']
            df.loc[df['Label'] == label, 'Label_en'] = label_en
            i+=1
            # Loading display
            sys.stdout.write("\033[K")
            print("Translating label:", i,"/", n, label,'->', label_en, end="\r")
            
    else:
        for label in df['Label']:
            word_to_translate = label
            label_en = vars(translator.translate(word_to_translate, src=region.lower(), dest='en'))['text']
            df.loc[df['Label'] == label, 'Label_en'] = label_en
            i+=1
            # Loading display
            sys.stdout.write("\033[K")
            print("Translating label:", i,"/", n, label,'->', label_en, end="\r")
            
            
    add_graph_attribute(graph, df, 'Label_en')

    # Save the graph
    nx.write_gexf(graph, path + 'filled_graph_translated.gexf')  

    df.to_csv(path + 'filled_nodes_translated.csv', encoding='utf-8')
    
    sys.stdout.write("\033[K")
    print("Translating label: Done")
    
    return df



