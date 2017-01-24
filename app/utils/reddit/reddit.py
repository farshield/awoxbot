"""
reddit.py
"""
import os
import time
import re
from operator import itemgetter
import yaml
import requests

BASEDIR = os.path.abspath(os.path.dirname(__file__))
USER_AGENT = 'awoxbot'


def base36decode(number):
    return int(number, 36)


def find_keywords(keyword_list, text):
    if keyword_list and text:
        for keyword in keyword_list:
            if re.search(keyword, text, re.IGNORECASE):
                return True
    return False


def reddit_channel_name():
    with open(os.path.join(BASEDIR, 'reddit.conf')) as config_file:
        config_data = yaml.safe_load(config_file)
    return config_data['channel']


def reddit_get_salt(
        keyword_list=None,
        post_enabled=True,
        comment_enabled=True,
        last_post_id=0,
        last_comment_id=0,
        post_limit=10
):
    new_content = []
    first_post_id = 0
    first_comment_id = 0

    # get new posts
    if post_enabled:
        result = requests.get(
            url='https://www.reddit.com/r/Eve/new/.json?limit={}'.format(post_limit),
            headers={'User-Agent': USER_AGENT},
            timeout=3
        )
        posts_json = result.json()['data']['children']
        first_post_id = base36decode(posts_json[0]['data']['id'].encode('ascii', 'ignore'))

        for child in posts_json:
            post_id = base36decode(child['data']['id'].encode('ascii', 'ignore'))
            if post_id > last_post_id:
                created = int(child['data']['created_utc'])
                permalink = "https://www.reddit.com" + child['data']['permalink']
                post_title = child['data']['title']
                text = child['data']['selftext']
                if keyword_list is None or find_keywords(keyword_list, text):
                    new_content.append(('post', post_id, created, permalink, post_title, text))

    time.sleep(.2)

    # get new comments
    if comment_enabled:
        result = requests.get(
            url='https://www.reddit.com/r/Eve/comments/.json?limit={}'.format(post_limit),
            headers={'User-Agent': USER_AGENT},
            timeout=3
        )
        comments_json = result.json()['data']['children']
        first_comment_id = base36decode(comments_json[0]['data']['id'].encode('ascii', 'ignore'))

        for child in comments_json:
            comment_id = base36decode(child['data']['id'].encode('ascii', 'ignore'))
            if comment_id > last_comment_id:
                created = int(child['data']['created_utc'])
                permalink = "https://reddit.com/r/Eve/comments/{}//{}/".format(
                    child['data']['link_id'][3:],
                    child['data']['id']
                )
                parent_title = child['data']['link_title']
                text = child['data']['body']
                if keyword_list is None or find_keywords(keyword_list, text):
                    new_content.append(('comment', comment_id, created, permalink, parent_title, text))

    return sorted(new_content, key=itemgetter(2)), first_post_id, first_comment_id


def reddit_main(display_content):
    last_post_id = 0
    last_comment_id = 0

    while True:
        # get configuration and account information
        with open(os.path.join(BASEDIR, 'reddit.conf')) as config_file:
            config_data = yaml.safe_load(config_file)

        if config_data['development']:
            print config_data

        [new_content, first_post_id, first_comment_id] = reddit_get_salt(
            keyword_list=config_data['keyword_list'],
            post_enabled=config_data['post_enabled'],
            comment_enabled=config_data['comment_enabled'],
            last_post_id=last_post_id,
            last_comment_id=last_comment_id,
            post_limit=config_data['post_limit']
        )

        last_post_id = first_post_id
        last_comment_id = first_comment_id

        if new_content:
            display_content(new_content)
        time.sleep(config_data['cycle_time'])


def display_content_simple(content):
    for items in content:
        print items


def main():
    reddit_main(display_content_simple)

if __name__ == "__main__":
    main()
