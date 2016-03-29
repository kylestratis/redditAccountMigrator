#!/usr/bin/python
import praw
import OAuth2Util
import json
import sys

"""

This uses OAuth to log in. Please follow the steps here to initially set up the app 
and config files. You will need two: olduserconfigfile.txt and newuserconfigfile.txt.

OAUth2Util.py by /u/SmBe19 (https://github.com/SmBe19/praw-OAuth2Util)

"""

def main(): 
    r = praw.Reddit(user_agent='RedditAccountMigrator v0.1 by /u/AchillesDev')
    
    # Check if token already exists
    r.config.store_json_result = True
    print("Ensure you are logged in with your original account\n")
    input("Press Enter to continue...")
    o = OAuth2Util.OAuth2Util(r, configfile="olduserconfigfile.txt")
    subreddits = get_subs(r)
    save_to_file(subreddits)
    r.clear_authentication()
    print("Now log in with your new account\n")
    input("Press Enter to continue...")
    o_new_user = OAuth2Util.OAuth2Util(r, configfile="newuserconfigfile.txt")
    subscribe(r, subreddits)


def get_subs(praw_instance):
    subreddits = praw_instance.get_my_subreddits()
    subreddit_list = []
    for s in subreddits:
        subreddit_list.append(s)
    return subreddit_list

def save_to_file(subreddits):
    f = open('subreddits.txt', 'a')
    for s in subreddits:
        f.writelines(s.display_name + '\n' )
    f.close()

def subscribe(praw_instance, subreddit_list): 
    # First, unsubscribe from old account
    old_subs = get_subs(praw_instance)
    for sub in old_subs:
        praw_instance.unsubscribe(sub)
        #print("Unsubscribing from ", sub)
    for s in subreddit_list:
        praw_instance.subscribe(s)
        #print("Subscribing to ", s)
    praw_instance.clear_authentication()

if __name__ == "__main__":
    main()