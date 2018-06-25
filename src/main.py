import datetime
import os
import sys
import time

import praw
import prawcore

from sqlalchemy import exists

# fixes sys.argv launching ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logger import logger
from database.base import SessionMode, session_scope
from models.post import Post
from database.sql_base import SessionMode, session_scope
from stores import registration


FOLLOWED_THIS_SESSION = []


class Bot:
    """
    Bot that will initialize on given subreddit,
    and scan for products to search/parse for information
    Depending on site function configuration, will post comments to submissions
    :attr site_functions: dictionary that maps domain to its corresponding function in /stores
    """
    site_functions = registration.site_functions

    def __init__(self, sub_to_stream: str):
        self.logger = logger.get_logger('Bot', './logfile.log')
        self.logger.info(f'initializing on {sub_to_stream}...')
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(sub_to_stream)
        self.logger.info('initialized')

    def run(self):
        load_stores()
        self.logger.info('streaming...')
        for submission in self.subreddit.stream.submissions():
            self.logger.info(f'found {submission.fullname}: {submission.title}')
            if self.has_been_parsed(submission):
                continue
            site_name, site_func = self.get_site_func(submission.url)
            if site_func is not None:
                self.logger.info('gathering data...')
                product_details, markdown = site_func(submission)
                post = Post(submission.fullname,
                            product_details.get('mpn', None),
                            product_details.get('price', None),
                            datetime.date.fromtimestamp(submission.created),
                            site_name)
                self.submit_reply(submission, markdown)
                self.save_data(post)
                time.sleep(10)
            self.logger.info('waiting for next submission...')

    def has_been_parsed(self, submission: praw.Reddit.submission):
        """
        Determines whether post has already been written to db or has
        been checked during the current bot session
        :param submission: praw.Reddit.submission, submission to test against
        :return: bool, True if has been parsed, else False
        """
        if submission.fullname in FOLLOWED_THIS_SESSION:
            self.logger.info('post already followed this session')
            return True
        elif self.already_replied_to(submission):
            self.logger.info('post already replied to')
            return True
        FOLLOWED_THIS_SESSION.append(submission.fullname)
        return False

    def already_replied_to(self, submission: praw.Reddit.submission):
        """
        Checks db for submission.fullname against reddit_fullname
        :param submission: praw.Reddit.submission, submission to test against
        :return: bool, true if found in db, else false
        """
        with session_scope(SessionMode.READ) as session:
            return session.query(exists().where(Post.reddit_fullname==submission.fullname)).scalar()

    def get_site_func(self, url: str):
        """
        Looks for function in site_functions corresponding to url
        :param url: str, link to check for site pattern
        :return: tuple, name of site found and function to call to parse;
        None, None if not found
        """
        for site, func in self.site_functions.items():
            if site in url:
                self.logger.info(f'found {site}')
                return site, func
        self.logger.warning(f'No func mapped to {url[url.find("//")+2:url.find(".com")+4]}')
        return None, None

    def submit_reply(self, submission: praw.Reddit.submission, markdown: str):
        """
        Attempts to post comment to reddit submission; sleeps if ratelimit enforced by reddit
        :param submission: praw.Reddit.submission, submission to reply to
        :param markdown: str, formatted markdown for reddit
        :return: nothing
        """
        if markdown is not None:
            self.logger.info('attempting reply...')
            try:
                submission.reply(markdown)
            except praw.exceptions.APIException as e:
                self.logger.error(e.message)
                if e.error_type == 'RATELIMIT':
                    time.sleep(self.get_wait_mins(e.message) * 60)
                    self.submit_reply(submission, markdown)
            else:
                self.logger.info('replied')

        self.logger.debug('skipping reply, markdown is None')

    def save_data(self, post: Post):
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

    def get_wait_mins(self, message: str):
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


def load_stores():
    """
    Iterates though /stores and imports all modules.  This process includes
    registration of store site functions decorated with @register.
    See /stores/registration.py for details on store registration.
    :return: nothing
    """
    path = './stores'
    sys.path.insert(0, path)
    for f in os.listdir(path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            __import__(fname)
    sys.path.pop(0)


def main(sub_to_stream: str):
    """
    Starts bot on sub_to_stream, attempts to handle exceptions and restart bot
    :param sub_to_stream: str, subreddit name ex 'buildapcsales'
    :return: nothing
    :attr wait_seconds: time to wait on 'unhandled' exception before restart attempt
    :attr max_uncaught: number of 'unhandled' to catch before exiting
    :attr attempts: starts at 1 to start at first attempt, increases after 'unhandled'
    """
    wrapper_logger = logger.get_logger('Wrapper', './logfile.log')
    wait_seconds = 60
    max_uncaught = 10
    attempts = 1
    bot = Bot(sub_to_stream)
    while attempts <= max_uncaught:
        wrapper_logger.info(f'starting attempt {attempts}...')
        try:
            bot.run()
        except prawcore.exceptions.ResponseException as e:
            # network/response error in the main loop, okay to restart
            wrapper_logger.critical(f'{e.__class__}: e')
            wrapper_logger.debug(f'likely just a network/praw error, '
                                 f'safe to restart immediately')
            wrapper_logger.critical(f'restarting in {wait_seconds} seconds')
            time.sleep(wait_seconds)
        except Exception as e:
            wait_time = wait_seconds * attempts * 2
            wrapper_logger.critical(f'{e.__class__}: e')
            wrapper_logger.critical(f'restarting in {wait_time} seconds')
            time.sleep(wait_time)
            attempts += 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('buildapcsales')







