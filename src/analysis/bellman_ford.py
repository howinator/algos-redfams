import pdb
import os, sys, time, json
from collections import defaultdict
from pprint import pprint
"""
The Bellman-Ford algorithm
Graph API:
    graph = nested dictionary repr of
#           adjaceny list
#   src = node to start from
"""

def init(graph, source):
    dest = dict() 
    pred = dict()
    for node in graph:
        dest[node] = float('Inf') #assume everything is infinitely far away
        pred[node] = None
    dest[source] = 0 #from source to itself
    return dest, pred

def bellman_ford(graph, src):  
    d, p = init(graph, src)
    l = len(graph)
    for i in range(l-1): 
        for u, edges in graph.items():
            for v, wt in edges.items():
                if d[v] > d[u] + wt:
                    # lower distance
                    d[v]  = d[u] + wt
                    p[u] = v
    #deal with negative edge-weights
    for u in graph:
        for v in graph[u]:
            assert d[v] <= d[u] + graph[u][v]

    return d, p
