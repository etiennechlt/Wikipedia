# Wikipedia trending topic detection

Python topic detection module for [SparkWiki](https://github.com/epfl-lts2/sparkwiki). The module computes statistics, clustering and assigns topics to clusters of trending [Wikipedia](https://www.wikipedia.org) pages, extracted using the [Anomaly Detection Algorithm](https://github.com/mizvol/anomaly-detection). Topic classification model is available [here](https://meta.wikimedia.org/wiki/Research:Language-Agnostic_Topic_Classification). The module works with all language editions of Wikipedia.

## Features
* Compute degree, betweeness centrality and modularity for clustering the graph by events
* Match wikipages with their Qids (unique Wikipedia ID)
* Match wikipages with their corresponding topics
* Match wikipages with their pageviews
* Save a new corresponding graph with these attributes
* Give a graphical topics partition of each cluster


## Pre-requisites
##### Python libraries
* numpy, matplotlib, pandas, networkx, requests
* [community](https://github.com/taynaud/python-louvain)
  ```bash
  $ pip install python-louvain
  ```
* [Googletrans](https://github.com/ssut/py-googletrans) (Optional)
  ```bash
  $ pip install googletrans
  ```

##### Wikipedia graph
Get the graph from [SparkWiki projet](https://github.com/epfl-lts2/sparkwiki) using [PeakFinder](https://github.com/epfl-lts2/sparkwiki/blob/master/src/main/scala/ch/epfl/lts2/wikipedia/PeakFinder.scala) module.

Put the graph file into a local folder `Python/Results/<Language>/<Language>_<date_start>_<date_end>`.

Language: EN, FR, RU, etc.

Date format: YYYYMMDD

Graph file name format: `peaks_graph_<date_start>_<date_end>.gexf`

Example: `Python/Results/EN/EN_20200316_20200331/peaks_graph_20200316_20200331.gexf`


## Usage
To compute the whole pipeline from a graph with the **name and folder path in the correct format** (cf. Pre-requisites), run the following command in the terminal:

```bash
$ python main.py EN 20200316 20200331
```

The pipeline can also be computed partially. To do that, specify the optional parameter from 1 to 6 to run only a part of the pipeline corresponding to the features described in the table below:

```bash
$ python main.py EN 20200316 20200331 1
```

| Parameter value        | Description                                                |
| :--------------------: | :--------------------------------------------------------- |
|           `0`          | Default                                                    |
|           `1`          | Compute degree, betweeness centrality and modularity       |
|           `2`          | Match Qids                                                 |
|           `3`          | Match topics                                               |
|           `4`          | Match pageviews                                            |
|           `5`          | Save graph attributes                                      |
|           `6`          | Give topics repartition per cluster                        |
|           `7`          | Translate labels into English                              |

Alternatively, one can run the `Topics_exctraction.ipynb` notebook. The notebook also includes the code generating visualisations.

## Results
Every stage of the pipeline generates and saves a .csv file with corresponding results.

The final step creates `/Figures` folder with figures of the topics partition per cluster.

Also, the final stage creates a graph file with all the computed attributes: `filled_graph.gexf`

In order to explore the detected topics, the graph can be visualized in [Gephi](https://gephi.org). We used Circle Pack Layout with modularity class as a partitioning attribute.


## Tests
Wikipedia graphs of trending pages are available in `Python/Result` for 16/08/2018 to 31/12/2018 and 17/12/2019 to 15/04/2020 periods for DE, EN, ES, FR, IT, RU, ZH languages.

The notebook `Topic_comparison.ipynb` gives a topic comparaison between EN, FR, RU languages. The figures are saved in `Python/Comparison_figures`.

Gephi files representing the graphs are also located in `/Gephi` folder.


## Examples

Here you can see a visual example. The animation shows trending topics for the last four months of 2018. The graph visualization illustrates the graph computed for the period 1-15 March 2020.

**Topics comparaison**
![Topics comparaison](https://raw.githubusercontent.com/etiennechlt/Wikipedia/master/Figures/bar.gif)
**Gephi graph (EN\_20200301\_20200315)**
![Gephi graph example (EN\_20200301\_20200315)](https://raw.githubusercontent.com/etiennechlt/Wikipedia/master/Figures/EN_20200301_20200315.png)



## Credits

Wikipedia trending topics detection: [SparkWiki](https://github.com/epfl-lts2/sparkwiki)

Clustering of trending pages: [Community detection](https://github.com/taynaud/python-louvain)

Topic classification model: [Language-Agnostic Topic Classification](https://github.com/geohci/wikidata-topic-model)

Labels translation: [Googletrans](https://github.com/ssut/py-googletrans)
