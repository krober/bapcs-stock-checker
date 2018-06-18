import datetime
import logging
import os.path
import sys
import time

import praw

from sqlalchemy import exists

# fixes sys.argv launching ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.formatters import formatters
from src.logger import logger
from src.stores import microcenter
from src.models.post import Post
from src.database.sql_base import SessionMode, session_scope


class Bot:
    site_funcs = {
        'microcenter.com': microcenter.mc_run
    }

    def __init__(self, sub_to_stream: str):
        self.logger = logger.get_logger('Bot', './logfile.log', logging.DEBUG)
        self.logger.info(f'initializing on {sub_to_stream}...')
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(sub_to_stream)
        self.logger.info('initialized')

    def run(self):
        self.logger.info('streaming...')
        for submission in self.subreddit.stream.submissions():
            self.logger.info(f'found {submission.id}: {submission.title}')
            if self.already_replied_to(submission.id):
                self.logger.info('post already replied to')
                continue
            url = submission.url
            site_name, site_func = self.get_func(url)
            if site_func:
                self.logger.info('gathering data...')
                inventories, metadata = site_func(url)
                markdown = formatters.build_markdown(inventories, metadata)
                self.submit_reply(submission, markdown)
                self.log_reply(submission, metadata, site_name)
            self.logger.info('waiting for next submission...')

    def get_func(self, url: str):
        for site, func in self.site_funcs.items():
            if site in url:
                self.logger.info(f'found {site}')
                return site, func
        self.logger.warning('No function mapped to this url')
        return None, None

    def already_replied_to(self, submission_id: str):
        with session_scope(SessionMode.READ) as session:
            return session.query(exists().where(Post.reddit_id==submission_id)).scalar()

    def submit_reply(self, submission, markdown: str):
        self.logger.info('attempting reply...')
        try:
            submission.reply(markdown)
        except praw.exceptions.APIException as e:
            self.logger.error(e.error_type, e.message)
            if e.error_type == 'RATELIMIT':
                time.sleep(self.get_wait_time(e.message) * 60)
                self.submit_reply(submission, markdown)
        else:
            self.logger.info('replied')

    def log_reply(self, submission, metadata: dict, site_name: str):
        post = Post(submission.id,
                    metadata.get('mpn'),
                    metadata.get('price'),
                    datetime.date.today(),
                    site_name)
        with session_scope(SessionMode.WRITE) as session:
            session.add(post)
        self.logger.info('written to db')

    def get_wait_time(self, message: str):
        if 'seconds' in message:
            wait_mins = 1
        else:
            wait_mins = 1 + [int(c) for c in message.split() if c.isdigit()][0]
        self.logger.info(f'Waiting {wait_mins} mins, then resubmitting...')
        return wait_mins


def main(sub_to_stream: str):
    wrapper_logger = logger.get_logger('Wrapper', './logfile.log', logging.INFO)
    wait_seconds = 90
    max_uncaught = 10
    attempts = 1
    bot = Bot(sub_to_stream)
    while attempts <= max_uncaught:
        wrapper_logger.info(f'starting attempt {attempts}...')
        try:
            bot.run()
        except Exception as e:
            wrapper_logger.critical(e)
            wrapper_logger.critical(f'restarting in {wait_seconds} seconds')
            attempts += 1
            time.sleep(wait_seconds)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('aJAPMASSOSCOS')







