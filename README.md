# Wikipedia topics

A Python tools helping to give statistics, clustering and topics labeling on [Wikipedia](https://www.wikipedia.org) pages graphs.

## Features
* Compute degree, betweeness centrality and modularity for clustering the graph by events
* Match wikipages with their Qids (unique Wikipedia ID)
* Match wikipages with their corresponding topics
* Match wikipages with their pagesviews
* Save a new corresponding graph with these attributes
* Give a graphical topics repartition of each cluster


## Pre-requisites
##### Python libraries
* numpy, matplotlib, pandas, networkx, requests
* [community](https://github.com/taynaud/python-louvain)
  ```bash
  $ pip install python-louvain
  ```

##### Wikipedia grah
Get the graph from [SparkWiki projet](https://github.com/epfl-lts2/sparkwiki).

Place the file in a folder "Python/Results/<Region>/<Region>\_<date\_beg>\_<date\_end>".
  
With date format: YYYYMMDD

Graph file format: peaks\_graph\_<date\_beg>\_<date\_end>.gexf

Example: "Python/Results/EN/EN\_20200316\_20200331/peaks\_graph\_20200316\_20200331.gexf"


## Usage
To compute the whole pipeline from a graph with the **right name and folder path** (cf. Pre-requisites).

```bash
$ python main.py EN 20200316 20200331
```

Or with optional parameter from 1 to 6 to run only a part of the pipeline corresponding to the features
```bash
$ python main.py EN 20200316 20200331 1
```

| Additionnal parameter  | Description                                                |
| :--------------------: | :--------------------------------------------------------- |
|           `0`          | Default                                                    |
|           `1`          | Compute degree, betweeness centrality and modularity       |
|           `2`          | Match Qids                                                 |
|           `3`          | Match topics                                               |
|           `4`          | Match pageviews                                            |
|           `5`          | Save graph attributes                                      |
|           `6`          | Give topics repartition per cluster                        |

Or run the "Topics_exctraction.ipynb" notebook for step visualisation

## Results
At each step a .csv file is created to save the computation. 

The final step createa "/Figures" folder with figures of the topics repartition per cluster.

At the end a graph file with all the computed attributes is created : "filled\_graph.gexf"

The graph can be visualize in Gephi with the Circle Pack Layout and modularity class attribute.


## Tests
Wiki graphs are available in "Python/Result" for 16/08/2018 to 31/12/2018 and 17/12/2019 to 15/04/2020 periods for EN, FR, RU regions.

The notebook "Topic\_comparison.ipynb" give a topic comparaison between EN, FR, RU regions. The figures are saved in "Python/Comparison_figures".

Gephi files representing the graphs are also in "/Gephi"


## Screenshots

![Topics comparaison](https://raw.githubusercontent.com/etiennechlt/Wikipedia/master/Python/Figures_comparison/bar.gif)
![Gephi graph example (EN\_20200301\_20200315)](https://raw.githubusercontent.com/etiennechlt/Wikipedia/master/Gephi/Figures/EN_20200301_20200315.png)



## Credits
[SparkWiki](https://github.com/epfl-lts2/sparkwiki)

[Community detection](https://github.com/taynaud/python-louvain)
