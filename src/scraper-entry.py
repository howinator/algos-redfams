#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # #
#
#  Usage: ./scraper-entry.py [local | prod]
#
# # # # # # # # # # # # # # # # # # #
import os.path
import sys

import praw
import praw.exceptions
import prawcore

# import src.helper.aux as aux
sys.path.append(os.path.abspath('./helper'))
import aux

def main(argv):
    agent_str = 'Scraper script by /u/howinator'
    user = ""

    helper = aux.ConfigHelper(argv)
    config_vars = helper.config
    creds = helper.creds


    while True:
        try:
            r = praw.Reddit(client_id=creds['client_id'], client_secret=creds['client_secret'], user_agent=agent_str)
            sub_all = r.subreddit('all')
            praw_usernames = [u.author.name for u in sub_all.comments(limit=100)]
            with aux.SQLWrapper(config_vars) as db:
                added_users = db.add_users(praw_usernames)
                for username in added_users:
                    user = r.redditor(username)
                    comments = [com for com in user.comments.new(limit=100)]
                    username_list = [username for ele in comments]
                    subreddit_list = [com.subreddit.display_name for com in comments]
                    db.add_subreddits(subreddit_list)
                    db.add_comments(username_list, subreddit_list)
        except praw.exceptions.PRAWException as e:
            print("API Exception: " + str(e) + "\nLast User: " + username)
            continue
        except prawcore.exceptions.PrawcoreException as e:
            print("Prawcore exception: " + str(e) + "\nLast User: " + username)
            continue
        except Exception as e:
            print("Unknown exception" + str(e))
            continue


if __name__ == '__main__':
    main(sys.argv[1:][0])
