#!/tools/common/linux/python/3.5.0/bin/python3

from dijkstra import dijkstra
import bellman_ford as bf
import os, json, argparse, time, sys
from pprint import pprint
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument('-graph', action='store', dest='graphFile', default='UNDEF', type=str)
parser.add_argument('-source', action='store', dest='source', default='rand', type=str)
parser.add_argument('-algo', action='store', dest='algo', default='both', type=str)

args = parser.parse_args()
if ((args.algo != 'both') and (args.algo != 'dijkstra') and (args.algo != 'bellman_ford')):
    print("ERROR: -algo argument must be either 'dijkstra', 'bellman_ford', or 'both'")
    sys.exit(1)
if not(os.path.isfile(args.graphFile)):
    print("ERROR: -graph argument must point to a valid JSON file")
    sys.exit(1)
with open(args.graphFile) as data_file:
    try:
        adj_list = json.load(data_file)
    except:
        print("ERROR: -graph argument must point to a valid JSON file")
        sys.exit(1)
if (args.source == 'rand'):
    args.source = list(adj_list.keys())[randint(0,len(adj_list.keys())-1)]
if args.source not in adj_list.keys():
    print("ERROR: -source argument must be a Vertex in the graph provided")
    sys.exit(1)


def printResults(algo, src, results, runtime):
    print(algo + " Shortest Path Results from vertex " + str(src) + ":")
    pprint(results)
    print(algo + " ran in " + str(runtime*1000.0) + " ms")

if (args.algo == 'both') or (args.algo == 'dijkstra'):
    start = time.time()
    shortPaths = dijkstra(adj_list,args.source)
    end = time.time()
    d_runtime = end - start
    printResults('Dijkstra', args.source, shortPaths, d_runtime)

if (args.algo == 'both') or (args.algo == 'bellman_ford'):
    start = time.time()
    shortPaths = bf.bellman_ford(adj_list,args.source)[0]
    end = time.time()
    bf_runtime = end - start
    printResults('Bellman-Ford', args.source, shortPaths, bf_runtime)

if (args.algo == 'both'):
    # Print summary with runtimes together
    print("\n\nSummary:")
    print("Dijkstra ran in     " + str(d_runtime*1000.0) + " ms")
    print("Bellman-Ford ran in " + str(bf_runtime*1000.0) + " ms")
