#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # #
#
#  Usage: ./entry.py [local | prod]
#
# # # # # # # # # # # # # # # # # # #
import yaml
import scraper.sqlwrapper as sql
import praw
import praw.exceptions


def main(argv):
    # load config variables
    env = argv
    db_config_file_path = "../infra/vars/{env}.yml".format(env=env)
    db_password_key = "{env}_pg_pass".format(env=env)
    config_vars = {}
    with open(db_config_file_path, 'r') as st:
        try:
            config_vars = yaml.load(st)
        except yaml.YAMLError as e:
            print(e)
            raise e
    creds_file_path = "../infra/vars/creds.yml"
    with open(creds_file_path, 'r') as f:
        try:
            creds = yaml.load(f)
        except yaml.YAMLError as e:
            print(e)
            raise e

    config_vars['db_pass'] = creds[db_password_key]
    agent_str = 'Scraper script by /u/howinator'
    user = ""

    while True:
        try:
            r = praw.Reddit(client_id=creds['client_id'], client_secret=creds['client_secret'], user_agent=agent_str)
            sub_all = r.subreddit('all')
            praw_usernames = [u.author.name for u in sub_all.comments(limit=100)]
            with sql.SQLWrapper(config_vars) as db:
                added_users = db.add_users(praw_usernames)
                for username in added_users:
                    user = r.redditor(username)
                    comments = [com for com in user.comments.new(limit=100)]
                    username_list = [username for ele in comments]
                    subreddit_list = [com.subreddit.display_name for com in comments]
                    db.add_subreddits(subreddit_list)
                    db.add_comments(username_list, subreddit_list)
        except praw.exceptions.PRAWException as e:
            print("API Exception: " + str(e) + "\nLast User: " + user)
            continue


if __name__ == '__main__':
    main('prod')
    # main(sys.argv[1:])
