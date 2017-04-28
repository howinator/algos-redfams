import os, time, json, sys
from itertools import groupby
from src.helper import aux


from pprint import pprint

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

def form_graph(env):

    config_vars = aux.ConfigHelper(env).config
    with aux.SQLWrapper(config_vars) as db:
        user_sub_results = db.get_user_sub_pairs()
        sub_results = db.get_subreddits()


    # [(user1, [sub1, sub2]), (user2, [sub2, sub3])]
    user_sub_groups = [(user, [sub for subuser,sub in group]) for (user, group) in groupby(user_sub_results, lambda x: x[0])]
    user_sub_dict = {user: sublist for user, sublist in user_sub_groups}
    subs = tuple([x[0] for x in sub_results])


    #Adj List -- not prefilled -- better for sparse graphs
    adj_dict = {name: {} for name in subs }

    # O(u*n*n) = for each user, for each node up to n, for each node up to n
    # TODO: smarter query?
    for user in users:
        username = user[1]
        # Get all their subreddits
        cur.execute('select subreddit from comments where username=' + str(user) + ';');
        node_list = cur.fetchall()
        for node in node_list:
            node_name = node_set[node[0]]
            for mapped_node in node_list:
                mapped_node = node_set[mapped_node[0]]
                if(mapped_node in adj_dict[node_name]):
                    adj_dict[node_name][mapped_node]+=1
                else:
                    adj_dict[node_name][mapped_node]=1

    with open('adj.json', 'w') as outfile:
        json.dump(adj_dict, outfile)

if __name__ == '__main__':
    form_graph(sys.argv[1:][0])