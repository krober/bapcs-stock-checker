import time

import praw

from logger import logger


logger = logger.get_logger('RedditHandler', './logfile.log')


class RedditHandler:

    @staticmethod
    def get_subreddit(sub_to_init: str):
        reddit = praw.Reddit()
        subreddit = reddit.subreddit(sub_to_init)
        return subreddit

    @staticmethod
    def submit_reply(submission: praw.Reddit.submission, markdown: str):
        """
        Attempts to post comment to reddit submission; sleeps
        and retries if ratelimit enforced by reddit
        :param submission: praw.Reddit.submission, submission to reply to
        :param markdown: str, formatted markdown for reddit
        :return: nothing
        """
        if markdown is not None:
            logger.info('attempting reply...')
            try:
                submission.reply(markdown)
            except praw.exceptions.APIException as e:
                logger.error(e.message)
                if e.error_type == 'RATELIMIT':
                    wait_mins = RedditHandler.get_ratelimit(e.message) * 60
                    logger.info(f'Waiting {wait_mins} mins, then resubmitting...')
                    time.sleep(wait_mins)
                    RedditHandler.submit_reply(submission, markdown)
            else:
                logger.info('replied')
        logger.debug('skipping reply, markdown is None')

    @staticmethod
    def get_ratelimit(message: str):
        """
        Determines time to sleep based on reddit ratelimit message,
        ex. 'You're doing that too much, try again in 7 minutes/seconds)'
        :param message: str, error string from reddit ratelimit exception
        :return: int, minutes to wait til ratelimit lifted
        """
        if 'seconds' in message:
            wait_mins = 1
        else:
            wait_mins = 1 + [int(c) for c in message.split() if c.isdigit()][0]
        return wait_mins


