#!/bin/env python

import argparse
import requests

REDDIT_URL = 'https://www.reddit.com/'
OAUTH_URL = 'https://oauth.reddit.com'

def get_token(username, password, app_id, app_secret):
    """Get an Oauth token

    Args:
        username (str): Reddit username
        password (str): Reddit password
        app_id (str): Reddit app id
        app_secret (str): Reddit app secret

    Returns:
        str: Oauth token to make API requests
    """
    data = {'grant_type': 'password', 'username': username, 'password': password}

    auth = requests.auth.HTTPBasicAuth(app_id, app_secret)
    r = requests.post(REDDIT_URL + 'api/v1/access_token',
                    data=data,
                    headers={'user-agent': 'new-reddit-account by {}'.format(username)},
                    auth=auth)  # request to get an access token
    json_data = r.json()

    token = 'bearer ' + json_data['access_token']
    return token

def get_old_account_subs(token, username):
    """Get all subs from old account

    Args:
        token (str): Oauth token
        username (str): Reddit username
    """
    headers = {'Authorization': token, 'User-Agent': 'new-reddit-account by {}'.format(username)}

    params = {'limit': 100}  # 100 is the most we can request at once
    response = requests.get(OAUTH_URL + '/subreddits/mine/subscriber', headers=headers, params=params)
    subs = response.json()['data']['children']  # List of subs that we received
    all_subs = []
    while subs:
        all_subs.extend([sub['data']['display_name'] for sub in subs])
        params = {'limit': 100, 'after': "t5_{}".format(subs[-1]['data']['id']), 'count': len(all_subs)}
        response = requests.get(OAUTH_URL + '/subreddits/mine/subscriber', headers=headers, params=params)
        subs = response.json()['data']['children']
    return all_subs

def get_parser():
    """Set up argument parser

    Returns:
        Namespace??: Arguments
    """
    parser = argparse.ArgumentParser("Create a new reddit account")
    parser.add_argument("--username", nargs=1, help="Old reddit account username", required=True)
    parser.add_argument("--password", nargs=1, help="Old reddit account password", required=True)
    parser.add_argument("--app-id", nargs=1, help="Reddit app id", required=True)
    parser.add_argument("--app-secret", nargs=1, help="Reddit app secret", required=True)
    parser.add_argument("--new-username", nargs=1, help="Username of new reddit account", required=True)
    parser.add_argument("--new-password", nargs=1, help="Password of new reddit account", required=True)
    return parser.parse_args()


def subscribe_new_account(subs, username, token):
    """Subscribe the new account to all the subreddits in subs

    Args:
        subs (list(str)): List of subreddit names
    """
    headers = {'Authorization': token, 'User-Agent': 'new-reddit-account by {}'.format(username)}
    for i in range(0, len(subs), 20):
        # We cant send them all at once because its too large so lets send 20 at a time
        params = {'action': 'sub', 'sr_name': ','.join(subs[i:i+20])}
        requests.post(OAUTH_URL + '/api/subscribe', headers=headers, params=params)


if __name__ == '__main__':
    args = get_parser()
    print("Getting OAuth tokens")
    old_token = get_token(args.username[0], args.password[0], args.app_id[0], args.app_secret[0])
    new_token = get_token(args.new_username[0], args.new_password[0], args.app_id[0], args.app_secret[0])
    print("Getting all current subscribed subreddits")
    old_subs = get_old_account_subs(old_token, args.username)
    print("Subscribing to all current subs in new account")
    subscribe_new_account(old_subs, args.new_username[0], new_token)
