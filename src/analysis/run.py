from dijkstra import dijkstra
#from bellmanford import bellmanford
import os, json, argparse, time
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-graph', action='store', dest='graphFile', default='UNDEF', type=str)
parser.add_argument('-source', action='store', dest='source', default='UNDEF', type=str)
parser.add_argument('-algo', action='store', dest='algo', default='both', type=str)

args = parser.parse_args()
if ((args.algo != 'both') and (args.algo != 'dijkstra') and (args.algo != 'bellmanford')):
    print("ERROR: -algo argument must be either 'dijkstra', 'bellmanford', or 'both'")
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
    runtime = end - start
    printResults('Dijkstra', args.source, shortPaths, runtime)
'''
if (args.algo == 'both') or (args.algo == 'bellmanford'):
    start = time.time()
    shortPaths = bellmanford(adj_list,args.source)
    end = time.time()
    run_time = end - start
    printResults('Bellman-Ford', shortPaths, runtime)
'''
