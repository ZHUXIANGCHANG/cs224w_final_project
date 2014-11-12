The macro graph of a country refers to that country's inter-county graph.

Within ./images are .png files depicting the inter-county graph for each 
country. These graphs were generated manually by looking at the underlying road
networks and translating paths along the road network into edges.

The *_graph.txt files contain the SNAP graph representation for each country's 
inter-county graph. One thing to note is that while the images number nodes 
starting from 1, the nodes in our graph representation are zero-indexed.

The *_labels.csv files contain the mapping for each country, from node IDs in 
that country's graph to the name of the corresponding county.
