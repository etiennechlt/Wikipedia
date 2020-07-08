import numpy as np
import networkx as nx
import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time





# Find the key of the value 'kv'  in a nested dictionnary
def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x
                
 


### src countains Qid, Topic, Probability, Page Id, Wiki_DB, etc and the old 'modularity_class' ###     
### dst countains the new 'modularity_class' to update to ###

def change_modularity(src, dst):
    src['modularity_class'] = ''
    for page_index in dst['Id']:
        src.loc[src['page_id'] == page_index, 'modularity_class'] = dst.loc[dst['Id'] == page_index, 'modularity_class'].item()
        src.loc[src['page_id'] == page_index, 'cluster'] = dst.loc[dst['Id'] == page_index, 'Cluster'].item()
        src.loc[src['page_id'] == page_index, 'degree'] = dst.loc[dst['Id'] == page_index, 'Degree'].item()
    return src



def string_topic_separator(df):
    for index, row in df.iterrows():
        topic_str = row['Topic']
        topic_list = topic_str.split('.') 
        df.loc[df['Topic'] == topic_str, 'Main topic'] = topic_list[0]
        df.loc[df['Topic'] == topic_str, 'Subtopic'] = topic_list[-1]

        
        
### Add the column 'name' from src to dst
def add_column(src, dst, name):
    for page_index in src['Id']:
        dst.loc[dst['Id'] == page_index, name] = src.loc[src['Id'] == page_index, name].item()
    return dst



# Normalize the column 'name'
def df_normalize(df, name):
#     df[name] = df[name] / df[name].max()
#     df[name]=(df[name]-df[name].min())/(df[name].max()-df[name].min())
    df[name] = (df[name] - df[name].mean() ) / df[name].std()
    return df


# Normalize the column 'name'
def series_normalize(df, name):
#     df[name] = df[name] / df[name].max()
#     df[name]=(df[name]-df[name].min())/(df[name].max()-df[name].min())
    s = (df[name] - df[name].mean() ) / df[name].std()
    return s




# Count the number of topics for each cluster of 'modularity_class'
def count_topic(dataFrame):
    
    topic_group = ((dataFrame.groupby(['Topic', 'modularity_class']))).count()

    total_cluster = ((dataFrame.groupby(['modularity_class']))).count()
    total_cluster = total_cluster['Qid'].to_frame()
    total_cluster.rename(columns={'Qid':'Total'}, inplace=True)

    topic_group = topic_group['Qid'].to_frame().reset_index('Topic')
    topic_group.rename(columns={'Qid':'Count'}, inplace=True)
    topic_group.sort_values(by = ['modularity_class', 'Count'], inplace=True, ascending = [True, False])

    topic_group['Total'] = total_cluster['Total']
    topic_group['Degree Ratio'] = topic_group['Count'] / topic_group['Total']
    topic_group['Subtopic'] = ''
    string_topic_separator(topic_group)

    for page in topic_group.iterrows():
        modularity = page[0]
        topic = page[1]['Topic']
        count = page[1]['Count']
        total = page[1]['Total']
        ratio = page[1]['Degree Ratio']
        subtopic = page[1]['Subtopic']
        maintopic = page[1]['Main topic']
        dataFrame.loc[(dataFrame['modularity_class'] == modularity) & (dataFrame['Topic'] == topic), 'Count'] = count
        dataFrame.loc[(dataFrame['modularity_class'] == modularity) & (dataFrame['Topic'] == topic), 'Total'] = total    
        dataFrame.loc[(dataFrame['modularity_class'] == modularity) & (dataFrame['Topic'] == topic), 'Degree Ratio'] = ratio
        dataFrame.loc[(dataFrame['modularity_class'] == modularity) & (dataFrame['Topic'] == topic), 'Subtopic'] = subtopic     
        dataFrame.loc[(dataFrame['modularity_class'] == modularity) & (dataFrame['Topic'] == topic), 'Main topic'] = maintopic
        
    return dataFrame





def weight_topic(df, list_ignored_topics):
#     weight = df['Probability'] * df['Count'] * df['Degree'] 
    weight = df['Degree'] * df['Probability']
    df['Weight'] = weight
    
    # Weighting theses topics at 0 because it's overrepresented and/or not representative of events
    df.loc[df['Topic'].isin(list_ignored_topics), 'Weight'] = 0
    return df








def add_graph_attribute(graph, df, attribute_name):
    dic = df[['Id', attribute_name]].set_index(keys='Id')
    dic.index = dic.index.astype('int64')
    dic.index = dic.index.astype('str')
    dic = dic.to_dict()[attribute_name]
    nx.set_node_attributes(graph, dic, attribute_name)

    
    
    
    
    
    
    
 
    
    
    
    
    
    
    