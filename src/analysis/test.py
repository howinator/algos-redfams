from dijkstra import dijkstra
import bellman_ford as bf
import unittest, json
from random import randint

class AlgoTest(unittest.TestCase):

    def testrandomCompare(self):
        # TODO: We need to make sure this test is run in the same dir
        #       as adj_local.json and dummy.json
        with open('adj_local.json') as data_file:    
            graph = json.load(data_file)
        for i in range(0,10):
            src =  list(graph.keys())[randint(0,len(graph.keys())-1)]
            print("Checking source node " + src)
            d_results = dijkstra(graph,src)
            bf_results = bf.bellman_ford(graph,src)[0]
            for node,dist in bf_results.items():
                self.assertEqual(dist,d_results[node][0])

    def testKnownData(self):
        with open('dummy.json') as data_file:    
            graph = json.load(data_file)

        a_paths = {'a': 0, 'b': 2,'c': 1, 'd': 5, 'e': 5, 
            'f': 4, 'g': 4, 'h': 4, 'i': 4, 'j': 5, 'k': 4, 
            'l': 4, 'm': 5, 'n': 4, 'o': 4, 'p': 5, 'q': 5, 
            'r': 5, 's': 5, 't': 3, 'u': 5, 'v': 4, 'w': 3, 
            'x': 4, 'y': 4, 'z': 3, 
        }
        shortest = dijkstra(graph,'a')
        for node,dist in a_paths.items():
            self.assertEqual(shortest[node][0], dist)
        shortest = bf.bellman_ford(graph,'a')[0]
        for node,dist in a_paths.items():
            self.assertEqual(shortest[node], dist)

        m_paths = {'a': 5, 'b': 3, 'c': 4, 'd': 3, 'e': 3,
            'f': 3, 'g': 2, 'h': 3, 'i': 2, 'j': 1, 'k': 3,
            'l': 3, 'm': 0, 'n': 2, 'o': 2, 'p': 3, 'q': 1,
            'r': 1, 's': 2, 't': 3, 'u': 3, 'v': 2, 'w': 3,
            'x': 1, 'y': 3, 'z': 2,
        }
        shortest = dijkstra(graph,'m')
        for node,dist in m_paths.items():
            self.assertEqual(shortest[node][0], dist)
        shortest = bf.bellman_ford(graph,'m')[0]
        for node,dist in m_paths.items():
            self.assertEqual(shortest[node], dist)


if __name__ == '__main__':
    unittest.main()


