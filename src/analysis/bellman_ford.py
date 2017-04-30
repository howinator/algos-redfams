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
        pred[node] = No
    dest[source] = 0 #from source to itself
    return d, p

def relax(node, adj, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one I have now
    if d[adj] > d[node] + graph[node][adj]:
        # lower distance
        d[adj]  = d[node] + graph[node][adj]
        p[adj] = node

def bellman_ford(graph, src):
    
    d, p = init(graph, src)
    l = len(graph)
    for i in range(l-1): 
        for u in graph:
            for v in graph[u]: 
                relax(u, v, graph, d, p) #for neighbors of u
     #deal with negative edge-weights
    for u in graph:
        for v in graph[u]:
            assert d[v] <= d[u] + graph[u][v]

    return d, p