import logging
import os.path
import sys
import time

import praw

from sqlalchemy import exists

# fixes sys.argv launching ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logger import logger
from stores import microcenter, newegg
from models.post import Post
from database.sql_base import SessionMode, session_scope


BAD_LINKS = []


class Bot:
    """
    Bot that will initialize on given subreddit,
    and scan for products to search/parse for information
    Depending on site function configuration, will post comments to submissions
    :attr site_functions: dictionary that maps domain to its corresponding function in /stores
    """
    site_functions = {
        'microcenter.com': microcenter.mc_run,
        'newegg.com': newegg.ne_run,
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
            self.logger.info(f'found {submission.fullname}: {submission.title}')
            if submission.fullname in BAD_LINKS:
                self.logger.info('post already attempted this session')
                continue
            if self.already_replied_to(submission.fullname):
                self.logger.info('post already replied to')
                continue
            site_name, site_func = self.get_site_func(submission.url)
            if site_func:
                self.logger.info('gathering data...')
                BAD_LINKS.append(submission.fullname)
                post, markdown = site_func(submission)
                self.submit_reply(submission, markdown)
                self.log_reply(post)
                time.sleep(10)
            self.logger.info('waiting for next submission...')

    def get_site_func(self, url: str):
        """
        Looks for function in site_functions corresponding to url
        :param url: str, link to check for site pattern
        :return: tuple, name of site found and function to call to parse; None, None if not found
        """
        for site, func in self.site_functions.items():
            if site in url:
                self.logger.info(f'found {site}')
                return site, func
        self.logger.warning(f'No function mapped to {url[:url.find(".com")+4]}')
        return None, None

    def already_replied_to(self, submission_fullname: str):
        """
        Checks db for submission_fullname against reddit_fullname
        :param submission_fullname: str, praw.Reddit.submission.fullname
        :return: bool, true if found in db, else false
        """
        with session_scope(SessionMode.READ) as session:
            return session.query(exists().where(Post.reddit_fullname==submission_fullname)).scalar()

    def submit_reply(self, submission: praw.Reddit.submission, markdown: str):
        """
        Attempts to post comment to reddit submission; sleeps if ratelimit enforced by reddit
        :param submission: praw.Reddit.submission, submission to reply to
        :param markdown: str, formatted markdown for reddit
        :return: nothing
        """
        if markdown is None:
            self.logger.debug('skipping reply, markdown is None')
            return
        else:
            self.logger.info('attempting reply...')
            try:
                submission.reply(markdown)
            except praw.exceptions.APIException as e:
                self.logger.error(e.message)
                if e.error_type == 'RATELIMIT':
                    time.sleep(self.get_wait_time(e.message) * 60)
                    self.submit_reply(submission, markdown)
            else:
                self.logger.info('replied')

    def log_reply(self, post: Post):
        """
        Writes Post model to db
        :param post: Post, Post instance to write
        :return: nothing
        """
        if post is None:
            self.logger.debug('skipping write to db, post is None')
            return
        else:
            with session_scope(SessionMode.WRITE) as session:
                session.add(post)
            self.logger.info('written to db')

    def get_wait_time(self, message: str):
        """
        Determines time to sleep based on reddit ratelimit
        :param message: str, error string from reddit ratelimit exception
        :return: int, minutes to wait til ratelimit lifted
        """
        if 'seconds' in message:
            wait_mins = 1
        else:
            wait_mins = 1 + [int(c) for c in message.split() if c.isdigit()][0]
        self.logger.info(f'Waiting {wait_mins} mins, then resubmitting...')
        return wait_mins


def main(sub_to_stream: str):
    """
    Starts bot on sub_to_stream, attempts to handle exceptions and restart bot
    :param sub_to_stream: str, subreddit name ex 'buildapcsales'
    :return: nothing
    :attr wait_seconds: time to wait on 'unhandled' exception before restart attempt
    :attr max_uncaught: number of 'unhandled' to catch before exiting
    :attr attempts: starts at 1 to start at first attempt, increases after 'unhandled'
    """
    wrapper_logger = logger.get_logger('Wrapper', './logfile.log', logging.INFO)
    wait_seconds = 60
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
            time.sleep(wait_seconds * attempts * 2)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('buildapcsales')







