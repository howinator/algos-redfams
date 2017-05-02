import argparse
import os
import yaml
import json
import cProfile as profile
import pstats
from typing import Dict, Tuple

import matplotlib
matplotlib.use('svg')

import matplotlib.pyplot as plt

from bellman_ford import bellman_ford as bf
from dijkstra import dijkstra as dj

AdjGraphDict = Dict[str, Dict[str, int]]
DIJKSTRA = 'dijkstra'
BELLMANFORD = 'bellman_ford'


def run_tests(source: str):
    max_str = 'max'
    min_str = 'min'

    parent_dir = os.path.dirname(__file__)
    test_case_dir = os.path.join(parent_dir, 'out', 'tests', source)
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

    results_file_basename = "{env}-test-results-{min_v}-{max_v}.json".format(min_v=str(test_sizes[0]), max_v=str(test_sizes[-1]), env=source)
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


def plot_results(filename: str) -> None:
    base_dir = os.path.dirname(__file__)
    results_dir = os.path.join(base_dir, 'out', 'results')
    results_file = os.path.join(results_dir, filename)
    with open(results_file) as f:
        results_data = json.load(f)
    pink = (194, 227, 119)
    green =(227, 119, 194)
    def convert_color(rgb: Tuple[int]) -> Tuple[float]:
        return rgb[0] / 255., rgb[1] / 255., rgb[2] / 255.
    bf_color = convert_color(pink)
    dj_color = convert_color(green)

    bf_min = results_data[BELLMANFORD]['min']
    bf_max = results_data[BELLMANFORD]['max']
    dj_min = results_data[DIJKSTRA]['min']
    dj_max = results_data[DIJKSTRA]['max']

    plt.figure(figsize=(12, 9))
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Remove plot frame lines
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Ensure axis ticks only show on bottom and left
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # FIXME Use sane limits
    x_lim = (500, 10500)
    y_lim = (0, 1)
    x_range = (0, 105, 10)

    plt.ylim(*y_lim)
    plt.xlim(*x_lim)

    # Make sure ticks are large enough to easily read.
    plt.yticks([x / 100. for x in range(*x_range)], [str(x) + ' ms' for x in [x / 100. for x in range(*x_range)]], fontsize=14)
    plt.xticks(fontsize=14)

    # Provide tick lines across plot
    for y in range(*x_range):
        y /= 100.
        plt.plot(range(*x_lim), [y] * len(range(*x_lim)), "--", lw=0.5, color="black", alpha=0.3)

    # Remove default tick marks
    plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='on', left='off', right='off', labelleft='on')

    def plot_data(dataset: Dict[str, float], label: str, marker: str, color: str):
        zipped_data = zip(dataset.keys(), dataset.values())
        sorted_data = sorted(zipped_data, key=(lambda x: int(x[0])))
        return plt.plot([int(x[0]) for x in sorted_data], [x[1] for x in sorted_data], marker=marker, color=color, label=label)

    first = plot_data(bf_min, 'Bellman Ford, Min-Degree', 'o', bf_color)
    second = plot_data(bf_max, 'Bellman Ford, Max-Degree', 'x', bf_color)
    third = plot_data(dj_min, 'Dijkstra, Min-Degree', 'o', dj_color)
    fourth = plot_data(dj_max, 'Dijkstra, Max-Degree', 'x', dj_color)
    legend = plt.legend()
    # Change font size of legend
    plt.setp(plt.gca().get_legend().get_texts(), fontsize=14)
    # plt.gcf().canvas.renderer.dpi = 300
    plt.savefig(os.path.join(results_dir, "{file}-plot.svg".format(file=filename)), bbox_inches="tight")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default = -1
    parser.add_argument('source', type=str, help="Either the env source for running test or the file name of the results json file for graph")
    args=parser.parse_args()
    # If you give it an environment, run the test suite
    if args.source in ('local', 'prod'):
        run_tests(args.source)
    # if it's not an env, just build the graph
    else:
        plot_results(args.source)
