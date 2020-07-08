#!/usr/bin/env python
# coding: utf-8


import os
import sys
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
from topic_graph import *



# region, date_beg, date_end, path, graph_type, list_ignored_topics,prob_threshold
def main():
    if (len(sys.argv) < 4):
        raise ValueError("Wrong arguments : <region> <date_beg> <date_end> <path>")
    param =Parameters(*sys.argv[1:])
    try:
        dataFrame = init_graph(param)
    except (FileNotFoundError):
        print("Wrong file argument: ", param.path+"graph."+param.graph_type, "not found")
        return
    dataFrame = match_Qids(dataFrame, param)
    dataFrame = match_topic(dataFrame, param)
    dataFrame = count_views(dataFrame, param)
    dataFrame = save_graph_attributes(dataFrame, param)
    count_topic_per_cluster(dataFrame, param)
    
    
    
if __name__ == "__main__":
    main()