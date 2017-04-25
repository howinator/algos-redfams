#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # #
#
#  Usage: ./entry.py [local | prod]
#
# # # # # # # # # # # # # # # # # # #
import psycopg2
import yaml
import sys


def main(argv):
    # load config variables
    env = argv[0]
    file_path = "../infra/vars/{env}.yml".format(env=env)
    with open(file_path, 'r') as st:
        try:
            config_vars = yaml.load(st)
        except yaml.YAMLError as e:
            print(e)
            raise e
    # Get db pass and user and use defaults if vars don't exist
    db_pass = config_vars.get('db_pass', 'postgres')
    db_user = config_vars.get('db_user', 'postgres')


if __name__ == '__main__':
    main(sys.argv[1:])
