import os, sys, time, json
from collections import defaultdict
from heapq import *
from pprint import pprint


########################################
# Dijkstra's Shortest Path Algorithm
#
# Inputs:
#   graph = nested dictionary repr of
#           adjaceny list
#   src = node to start from
#
# Output:
#   dictionary where 
#       key = destination node
#       value = (distance, path taken)
#
########################################
def dijkstra(graph, src):
    numVertices = len(graph.keys())
    weights = {}
    weights[src] = (0, '')
    minHeap = [(0,src,'')]
    visited = set()
    while (minHeap):
        (weight, v1, path) = heappop(minHeap)
        if v1 not in visited:
            visited.add(v1)
            path = v1 + ", " + path
            for v2, moreWeight in graph[v1].items():
                curWeight = sys.maxsize
                if v2 in weights:
                    curWeight = weights[v2][0]
                if ((v2 not in visited) and (weight + moreWeight < curWeight)):
                    weights[v2] = (weight + moreWeight, path);
                    heappush(minHeap, (weight+moreWeight, v2, path))
    return weights


