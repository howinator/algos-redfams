from dijkstra import dijkstra
import unittest, json


class DijkstraTest(unittest.TestCase):
    #Spot check for now. 
    # TODO: Once Bellman-Ford is implemented, compare
    def testA(self):
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

    def testM(self):
        with open('dummy.json') as data_file:    
            graph = json.load(data_file)
        m_paths = {'a': 5, 'b': 3, 'c': 4, 'd': 3, 'e': 3,
            'f': 3, 'g': 2, 'h': 3, 'i': 2, 'j': 1, 'k': 3,
            'l': 3, 'm': 0, 'n': 2, 'o': 2, 'p': 3, 'q': 1,
            'r': 1, 's': 2, 't': 3, 'u': 3, 'v': 2, 'w': 3,
            'x': 1, 'y': 3, 'z': 2,
        }
        shortest = dijkstra(graph,'m')
        for node,dist in m_paths.items():
            self.assertEqual(shortest[node][0], dist)

if __name__ == '__main__':
    unittest.main()


