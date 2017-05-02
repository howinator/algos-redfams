import os
import yaml
import json
import cProfile as profile
import pstats
from typing import Dict

from bellman_ford import bellman_ford as bf
from dijkstra import dijkstra as dj

AdjGraphDict = Dict[str, Dict[str, int]]
DIJKSTRA = 'dijkstra'
BELLMANFORD = 'bellman_ford'


def run_tests():
    max_str = 'max'
    min_str = 'min'

    parent_dir = os.path.dirname(__file__)
    test_case_dir = os.path.join(parent_dir, 'out', 'tests')
    results_dir = os.path.join(parent_dir, 'out', 'results')
    test_files = os.listdir(test_case_dir)
    test_files = [file for file in test_files if 'json' in file]

    # sort filenames names from smallest to largest by converting filename to integer
    test_sizes = sorted([os.path.splitext(ele)[0] for ele in test_files], key=int)

    results_dict = {BELLMANFORD: {min_str: {}, max_str: {}}, DIJKSTRA: {min_str: {}, max_str: {}}}

    for test_size in test_sizes:
        # reform filenames now in sorted order
        base_name = "{base}.json".format(base=test_size)
        case = read_basename(test_case_dir, base_name)

        vertex_degrees = {key: len(value.keys()) for key, value in case.items()}
        # get the vertex with max degree
        max_degree_vertex = max(vertex_degrees.keys(), key=(lambda key: vertex_degrees[key]))
        # don't want only self-connected vertices, so min_connected will be least-connected vertex that has
        # at least two adjacent vertices
        min_degree_vertex = min(vertex_degrees.keys(), key=(lambda key: vertex_degrees[key] if vertex_degrees[key] >= 2 else float('inf')))

        results_dict[BELLMANFORD][min_str][test_size] = profile_call(BELLMANFORD, case, min_degree_vertex)
        results_dict[BELLMANFORD][max_str][test_size] = profile_call(BELLMANFORD, case, max_degree_vertex)
        results_dict[DIJKSTRA][min_str][test_size] = profile_call(DIJKSTRA, case, min_degree_vertex)
        results_dict[DIJKSTRA][max_str][test_size] = profile_call(DIJKSTRA, case, max_degree_vertex)

    results_file_basename = "test-results-{min_v}-{max_v}.json".format(min_v=str(test_sizes[0]), max_v=str(test_sizes[-1]))
    results_file_full_path = os.path.join(results_dir, results_file_basename)
    with open(results_file_full_path, 'w') as f:
        json.dump(results_dict, f, sort_keys=True, indent=4, separators=(',', ': '))



def profile_call(algo: str, graph: AdjGraphDict, src: str) -> float:
    prof = profile.Profile()
    if algo not in (DIJKSTRA, BELLMANFORD):
        raise ValueError('algo must be either dijkstra or bellmanford')
    run_str = 'call(graph, src)'
    call_module = dj if algo == DIJKSTRA else bf
    prof.runctx(run_str, {'graph': graph, 'src': src, 'call': call_module}, {})
    stats = pstats.Stats(prof)
    return stats.total_tt

def read_basename(base_dir: str, basename: str) -> AdjGraphDict:
    with open(os.path.join(base_dir, basename)) as f:
        loaded = json.load(f)
    return loaded

'''
from time import sleep
def foo(a):
    sleep(1)
prof=profile.Profile()
prof.runctx('foo(b)', {'foo': foo, 'b': 4}, {})
<cProfile.Profile object at 0x1073223f0>
new_stat=pstats.Stats(prof)
new_stat.total_tt
1.0043059999999997

'''

'''
from time import sleep
def foo(a):
    time.sleep(1)
prof=profile.Profile()
prof.runctx('foo(b)', {'foo': foo, 'a': 4}, {})
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "/Users/howie/.pyenv/versions/3.6.1/lib/python3.6/cProfile.py", line 100, in runctx
    exec(cmd, globals, locals)
  File "<string>", line 1, in <module>
NameError: name 'b' is not defined
prof.runctx('foo(b)', {'foo': foo, 'b': 4}, {})
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "/Users/howie/.pyenv/versions/3.6.1/lib/python3.6/cProfile.py", line 100, in runctx
    exec(cmd, globals, locals)
  File "<string>", line 1, in <module>
  File "<input>", line 2, in foo
NameError: name 'time' is not defined
def foo(a):
    sleep(1)
prof.runctx('foo(b)', {'foo': foo, 'b': 4}, {})
<cProfile.Profile object at 0x1073223f0>
new_stat=pstats.Stats(prof)
new_stat.time_tt
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'Stats' object has no attribute 'time_tt'
new_stat.total_tt
1.0043059999999997

'''


if __name__ == '__main__':
    run_tests()