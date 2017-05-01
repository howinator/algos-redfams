import os
import yaml
import json
import cProfile as profile
from typing import Dict

from .bellman_ford import bellman_ford as bf
from .dijkstra import dijkstra as dj

def run_tests():
    parent_dir = os.path.dirname(__file__)
    test_case_dir = os.listdir(os.path.join(parent_dir, 'out', 'tests'))
    results_dir = os.path.join(parent_dir, 'out', 'results')
    test_files = os.listdir(results_dir)
    no_ext_basnames = sorted([os.path.splitext(ele)[0] for ele in test_files], key=int)
    test_basenames = ["{base}.json".format(base=ele ) for ele in no_ext_basnames]
    largest_case = read_basename(test_basenames[-1], test_case_dir)
    connectedness = {key: len(value.keys()) for key, value in largest_case}
    # get the most connected node
    most_connected_souce = max(connectedness.keys(), key=(lambda key: connectedness[key]))
    # test_basenames = os.listdir(results_dir)
    results_dict = {'bellman_ford': None, 'dijkstra': None}
    for base_name in test_basenames:
        with open(os.path.join(test_case_dir, base_name), 'r') as fin:
            test_case = json.load(fin)
            bf_result = profile.runctx('bf.bellman_ford(graph, d', {'graph'})

def read_basename(basename: str, base_dir: str) -> Dict[str, Dict[str, int]]:
    with open(os.path.join(base_dir, basename)) as f:
        loaded = json.load(f)
    return loaded






if __name__ == '__main__':
    run_tests()