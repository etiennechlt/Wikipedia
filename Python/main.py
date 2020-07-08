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



### Automate the functions used in the notebook passing the arguments  <region> <date_beg> <date_end> ###
### Example of use in terminal : "python3 main.py FR 20180901 20180915" ### 
### NB: needs the graph file in "Results/'Region'/'Region'_'datebeg'_'dateend'/graph.gexf" ###

def main():
    if (len(sys.argv) < 4):
        raise ValueError("Wrong arguments : <region> <date_beg> <date_end>")
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