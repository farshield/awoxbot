"""
Reddit Monitor
"""
import threading
import time
import re
from operator import itemgetter
import yaml
import logging
import requests


class RedditM(threading.Thread):
    USER_AGENT = 'awoxbot'

    def __init__(self, config_path, display_content):
        threading.Thread.__init__(self)
        self.daemon = True
        self.config_path = config_path
        self.display_content = display_content
        self.config_data = None
        self.requests_ok = 0
        self.requests_error = 0
        self.last_post_id = 0
        self.last_comment_id = 0
        self.read_config()

    def read_config(self):
        with open(self.config_path) as config_file:
                self.config_data = yaml.safe_load(config_file)

    @staticmethod
    def base36decode(number):
        return int(number, 36)

    @staticmethod
    def find_keywords(keyword_list, text):
        if keyword_list and text:
            for keyword in keyword_list:
                if re.search(keyword, text, re.IGNORECASE):
                    return True
        return False

    def get_salt(
            self,
            keyword_list=None,
            post_enabled=True,
            comment_enabled=True,
            last_post_id=0,
            last_comment_id=0,
            post_limit=10
    ):
        new_content = []
        first_post_id = self.last_post_id
        first_comment_id = self.last_comment_id

        # get new posts
        if post_enabled:
            try:
                result = requests.get(
                    url='https://www.reddit.com/r/Eve/new/.json?limit={}'.format(post_limit),
                    headers={'User-Agent': RedditM.USER_AGENT},
                    timeout=3
                )
            except requests.exceptions.RequestException:
                self.requests_error += 1
                logging.warning("[Requests] error when trying to fetch new posts")
            else:
                if result.status_code == 200:
                    self.requests_ok += 1
                    posts_json = result.json()['data']['children']
                    first_post_id = RedditM.base36decode(posts_json[0]['data']['id'].encode('ascii', 'ignore'))

                    for child in posts_json:
                        post_id = RedditM.base36decode(child['data']['id'].encode('ascii', 'ignore'))
                        if post_id > last_post_id:
                            created = int(child['data']['created_utc'])
                            permalink = "https://www.reddit.com" + child['data']['permalink']
                            author = child['data']['author']
                            post_title = child['data']['title']
                            text = child['data']['selftext']

                            post_data = ('post', post_id, created, permalink, author, post_title, text)
                            if keyword_list:
                                if RedditM.find_keywords(keyword_list, post_title) or \
                                        RedditM.find_keywords(keyword_list, text):
                                    new_content.append(post_data)
                            else:
                                new_content.append(post_data)

        time.sleep(.2)

        # get new comments
        if comment_enabled:
            try:
                result = requests.get(
                    url='https://www.reddit.com/r/Eve/comments/.json?limit={}'.format(post_limit),
                    headers={'User-Agent': RedditM.USER_AGENT},
                    timeout=3
                )
            except requests.exceptions.RequestException:
                logging.warning("[Requests] error when trying to fetch new comments")
            else:
                if result.status_code == 200:
                    comments_json = result.json()['data']['children']
                    first_comment_id = RedditM.base36decode(comments_json[0]['data']['id'].encode('ascii', 'ignore'))

                    for child in comments_json:
                        comment_id = RedditM.base36decode(child['data']['id'].encode('ascii', 'ignore'))
                        if comment_id > last_comment_id:
                            created = int(child['data']['created_utc'])
                            permalink = "https://reddit.com/r/Eve/comments/{}/comment/{}/".format(
                                child['data']['link_id'][3:],
                                child['data']['id']
                            )
                            parent_title = child['data']['link_title']
                            author = child['data']['author']
                            text = child['data']['body']

                            comment_data = ('comment', comment_id, created, permalink, author, parent_title, text)
                            if keyword_list:
                                if RedditM.find_keywords(keyword_list, text):
                                    new_content.append(comment_data)
                            else:
                                new_content.append(comment_data)

        return sorted(new_content, key=itemgetter(2)), first_post_id, first_comment_id

    def main_loop(self):
        while True:
            # re-read configuration file
            self.read_config()
            if self.config_data['development']:
                print self.config_data

            [new_content, first_post_id, first_comment_id] = self.get_salt(
                keyword_list=self.config_data['keyword_list'],
                post_enabled=self.config_data['post_enabled'],
                comment_enabled=self.config_data['comment_enabled'],
                last_post_id=self.last_post_id,
                last_comment_id=self.last_comment_id,
                post_limit=self.config_data['post_limit']
            )
            self.last_post_id = first_post_id
            self.last_comment_id = first_comment_id

            if new_content:
                self.display_content(new_content)
            time.sleep(self.config_data['cycle_time'])

    def run(self):
        self.main_loop()
