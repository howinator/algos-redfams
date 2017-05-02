import argparse
import json
import os
import sys
from itertools import groupby
from random import sample
from typing import Dict, List

sys.path.append(os.path.abspath('../helper'))
import aux as aux

AdjGraphDict = Dict[str, Dict[str, int]]


##
# Goal: Build adjacency list in the format
# adj_dict = {sub1 : { sub2: edge_weight,
#                      sub3: edge_weight,
#                      ...
#                    },
#             sub2 : { sub1 : edge_weight,
#                      ...
#                    },
#             ...
#             }
#

def generate_graphs(source: str, start: int = 1, stop: int = 100, step: int = 10) -> None:
    """
    Generates varying sizes of test cases which are written to disk to be used at a later time
    
    :param start: Smallest number of subreddits to include in test cases (inclusive)
    :param stop: Largest number of subreddits to include in test cases (inclusive)
    :param step: Step size for generating test case sizes
    :param source: Data source to pull from
    :return: None, side effect of writing to disk
    """
    # local = 'local'
    # prod = 'prod'
    exclusive_lower_limit = start - step
    step *= -1

    prev_test_case = form_graph(source)
    write_graph(prev_test_case, source)

    # Each test case is a subset of previous test case for performance reasons, so it makes sense to step through
    # test case generation from largest to smallest
    for num_ele in range(stop, exclusive_lower_limit, step):
        possible_subs = sample(prev_test_case.keys(), num_ele)
        new_test_case = form_subset_graph(prev_test_case, possible_subs)
        del prev_test_case
        write_graph(new_test_case, num_ele, source)
        prev_test_case = new_test_case


def form_subset_graph(orig_graph: AdjGraphDict, new_sub_set: List[str]) -> AdjGraphDict:
    return {out_key: {in_key: in_value for in_key, in_value in out_value.items() if in_key in new_sub_set} for
            out_key, out_value in orig_graph.items() if out_key in new_sub_set}


def form_graph(env: str) -> AdjGraphDict:
    """
    Connects to database and forms graph from entire data set

    :param env: 
    :return: Returns a dict representing the graph
    """
    config_vars = aux.ConfigHelper(env).config
    with aux.SQLWrapper(config_vars) as db:
        user_sub_results = db.get_user_sub_pairs()
        sub_results = db.get_subreddits()

    # [(user1, [sub1, sub2]), (user2, [sub2, sub3])]
    user_sub_groups = [(user, [sub for subuser, sub in group]) for (user, group) in
                       groupby(user_sub_results, lambda x: x[0])]
    subs = tuple([x[0] for x in sub_results])
    del (user_sub_results)
    del (sub_results)

    # Adj List -- not prefilled -- better for sparse graphs
    adj_dict = {name: {} for name in subs}

    # O(u*n*n) = for each user, for each node up to n, for each node up to n
    # user_group= (user, [sub1, sub2])
    for user_group in user_sub_groups:
        # Get all their subreddits
        node_list = user_group[1]
        for node in node_list:
            node_name = node
            for mapped_node in node_list:
                if mapped_node in adj_dict[node_name]:
                    adj_dict[node_name][mapped_node] += 1
                else:
                    adj_dict[node_name][mapped_node] = 1

    return adj_dict


def write_graph(graph: AdjGraphDict, suffix: str, env: str = None) -> None:
    """
    Writes graph to disk
    :param env: 
    :param graph: Dict-based graph to write to disk
    :param suffix: str to append to filename before extension. Also determines directory to write to
    :return: side effect of writing to disk
    """
    dir_name = os.path.dirname(__file__)
    if suffix in ('prod', 'local'):
        out_file_path = os.path.join(dir_name, 'out', 'adj_{suffix}.json'.format(suffix=suffix))
        with open(out_file_path, 'w') as outfile:
            json.dump(graph, outfile, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        out_file_path = os.path.join(dir_name, 'out', 'tests', env, '{suffix}.json'.format(suffix=suffix))
        with open(out_file_path, 'w') as outfile:
            json.dump(graph, outfile)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default = -1
    parser.add_argument('source', choices=['local', 'prod'], type=str)
    parser.add_argument('--start', type=int, dest='start', default=default)
    parser.add_argument('--stop', type=int, dest='stop', default=default)
    parser.add_argument('--step', type=int, dest='step', default=default)
    args=parser.parse_args()
    num_args = len([k for k, v in vars(args).items() if v != default])
    if num_args != 1 and num_args != 4:
        print("If you specify start, stop or step, you must specify all three")
        sys.exit(1)
    if args.start > args.stop:
        print("Start cannot be greater than stop.")
        sys.exit(1)
    if num_args == 1:
        form_graph(args.source)
    else:
        generate_graphs(source=args.source, start=args.start, stop=args.stop, step=args.step)

