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
### Mode: 0 run all (default)             ###
### Mode: 1 run init_graph                ###
### Mode: 2 run match_Qids                ###
### Mode: 3 run match_topic               ###
### Mode: 4 run count_views               ###
### Mode: 5 run save_graph_attributes     ###
### Mode: 6 run count_topic_per_cluster   ###
### Mode: 6 run translate_label           ###

def main():
    if (len(sys.argv) < 4):
        raise ValueError("Not enough arguments : <region> <date_beg> <date_end> <Optional: mode (0 to 6)>")
    param =Parameters(*sys.argv[1:4])
    
    # Mode : 0 to 6 to chose which function to run
    if (len(sys.argv) == 5):
        mode = int(sys.argv[-1])
    else:
        mode = 0
    # Running init_graph()
    if (mode in [0, 1]):
        try:
            init_graph(param)
        except (FileNotFoundError):
            param.graph_type = 'graphml'
            try:
                init_graph(param)
            except (FileNotFoundError):
                print("Wrong file argument: ", param.path+"graph."+param.graph_type, "not found")
                return
            print("Graph type change to graphml")
    # Running match_Qids()
    if (mode in [0, 2]):
        try:
            match_Qids(param)
        except (FileNotFoundError):
                print("File 'pages_Qids.csv' not found, try running 'init_graph()' first")
                return
    # Running match_topic()
    if (mode in [0, 3]):
        try:
            match_topic(param)
        except (FileNotFoundError):
                print("File 'pages_Qids.csv' not found, try running 'match_Qids()' first")
                return
    # Running count_views()
    if (mode in [0, 4]):
        try:
            count_views(param)
        except (FileNotFoundError):
                print("File 'pages_topic.csv' not found, try running 'match_topic()' first")
                return
    # Running save_graph_attributes()
    if (mode in [0, 5]):
        try:
            save_graph_attributes(param)
        except (FileNotFoundError):
            param.graph_type = 'graphml'
            try:
                save_graph_attributes(param)
            except (FileNotFoundError):
                print("Wrong file argument: ", param.path+"graph."+param.graph_type, "not found")
                print("Or file 'pages_views.csv' not found, try running 'count_views()' first")
                return
            print("Graph type change to graphml")
    # Running count_topic_per_cluster()
    if (mode in [0, 6]):
        try:
            count_topic_per_cluster(param)
        except (FileNotFoundError):
            print("File 'filled_nodes.csv' not found, try running 'save_graph_attributes()' first")
            return
    # Running translate_label()    
    if (mode == 7):
        try:
            translate_label(param)
        except (FileNotFoundError):
            print("File 'filled_nodes.csv' not found, try running 'save_graph_attributes()' first")
        return
    
    
if __name__ == "__main__":
    main()