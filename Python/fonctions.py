import numpy as np
import networkx as nx
import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time



def mult(a=0, b=0):
    return a*b


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
                
 



# 
### src countains Qid, Topic, Probability, Page Id, Wiki_DB, etc and the old 'modularity_class' ###     
### dst countains the new 'modularity_class' to update to ###

def change_modularity(src, dst):
    src['modularity_class'] = ''
    for page_index in dst['Id']:
        src.loc[src['page_id'] == page_index, 'modularity_class'] = dst.loc[dst['Id'] == page_index, 'modularity_class'].item()
        src.loc[src['page_id'] == page_index, 'cluster'] = dst.loc[dst['Id'] == page_index, 'Cluster'].item()
        src.loc[src['page_id'] == page_index, 'degree'] = dst.loc[dst['Id'] == page_index, 'Degree'].item()
    return src



def string_separator(df):
    for index, row in df.iterrows():
        topic_str = row['topic']
        topic_list = topic_str.split('.') 
        df.loc[df['topic'] == topic_str, 'subtopic'] = topic_list[-1]
