import os.path
import sys
import time

import praw

# fixes sys.argv launching ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import formatters
from src.stores import microcenter


def get_func(url: str):
    """
    given a url, if found in site_funcs, return corresponding site function
    :param url: str
    :return: function, function to run to receive corresponding site data; None if not found
    """
    site_funcs = {
        'microcenter.com': microcenter.mc_run
    }
    for site, func in site_funcs.items():
        if site in url:
            return func
    return None


class Bot:
    def __init__(self, sub_to_stream: str):
        print(f'initializing on {sub_to_stream}...')
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(sub_to_stream)
        print('initialized')

    def run(self):
        print('streaming...')
        for submission in self.subreddit.stream.submissions():
            print(f'found {submission.title}')
            url = submission.url
            site_func = get_func(url)
            if site_func:
                print('gathering data...')
                locations, metadata = site_func(url)
                markdown = formatters.build_markdown(locations, metadata)
                self.submit_reply(submission, markdown)
            else:
                print('No function mapped to this url')

    def submit_reply(self, submission: praw.Reddit.submission, markdown: str):
        print('attempting reply...')
        try:
            submission.reply(markdown)
        except praw.exceptions.APIException as e:
            print(e.error_type, e.message)
            if e.error_type == 'RATELIMIT':
                self.rate_limit_handler(e.message)
        print('replied')

    def rate_limit_handler(self, e: str):
        wait_mins = 1 + [int(c) for c in e.split() if c.isdigit()][0]
        print(f'Waiting {wait_mins} mins, then restarting...')
        time.sleep(wait_mins * 60)
        self.run()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        subreddit = sys.argv[1]
    else:
        subreddit = 'buildapcsales'
    print(subreddit)
    bot = Bot(subreddit)
    bot.run()






