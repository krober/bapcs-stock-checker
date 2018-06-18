import datetime
import os.path
import sys
import time

import praw

from sqlalchemy import exists

# fixes sys.argv launching ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.formatters import formatters
from src.stores import microcenter
from src.models.post import Post
from src.database.sql_base import SessionMode, session_scope


class Bot:
    site_funcs = {
        'microcenter.com': microcenter.mc_run
    }

    def __init__(self, sub_to_stream: str):
        print(f'initializing on {sub_to_stream}...')
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(sub_to_stream)
        print('initialized')

    def run(self):
        print('streaming...')
        for submission in self.subreddit.stream.submissions():
            print(f'found {submission.id}: {submission.title}')
            if self.already_preplied_to(submission.id):
                print('post already replied to')
                continue
            url = submission.url
            site_name, site_func = self.get_func(url)
            if site_func:
                print('gathering data...')
                inventories, metadata = site_func(url)
                markdown = formatters.build_markdown(inventories, metadata)
                self.submit_reply(submission, markdown)
                self.log_reply(submission, metadata, site_name)
            else:
                print('No function mapped to this url')

    def already_preplied_to(self, submission_id: str):
        with session_scope(SessionMode.READ) as session:
            return session.query(exists().where(Post.reddit_id==submission_id)).scalar()

    def submit_reply(self, submission, markdown: str):
        print('attempting reply...')
        try:
            submission.reply(markdown)
        except praw.exceptions.APIException as e:
            print(e.error_type, e.message)
            if e.error_type == 'RATELIMIT':
                time.sleep(self.get_wait_time(e.message))
                self.submit_reply(submission, markdown)
        else:
            print('replied')

    def log_reply(self, submission, metadata: dict, site_name: str):
        post = Post(submission.id,
                    metadata.get('mpn'),
                    metadata.get('price'),
                    datetime.date.today(),
                    site_name)
        with session_scope(SessionMode.WRITE) as session:
            session.add(post)
        print('logged')

    def get_wait_time(self, message: str):
        if 'seconds' in message:
            wait_mins = 1
        else:
            wait_mins = 1 + [int(c) for c in message.split() if c.isdigit()][0]
        print(f'Waiting {wait_mins} mins, then restarting...')
        return wait_mins

    def get_func(self, url: str):
        """
        given a url, if found in site_funcs, return corresponding site function
        :param url: str
        :return: site name, function; function to run to receive corresponding site data; None if not found
        """
        for site, func in self.site_funcs.items():
            if site in url:
                return site, func
        return None


if __name__ == '__main__':
    if len(sys.argv) > 1:
        subreddit = sys.argv[1]
    else:
        subreddit = 'aJAPMASSOSCOS'
    print(subreddit)
    bot = Bot(subreddit)
    bot.run()






