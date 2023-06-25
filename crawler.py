import os
import praw
from praw.models import MoreComments
from dotenv import load_dotenv
import re

load_dotenv()

REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
REDDIT_SECRET = os.environ.get('REDDIT_SECRET')
REDDIT_CLIENTID = os.environ.get('REDDIT_CLIENTID')

def crawl(module):
    reddit = praw.Reddit(client_id=REDDIT_CLIENTID, client_secret=REDDIT_SECRET, 
                         user_agent="Comment Extraction (by /" + REDDIT_USERNAME + ")")
    result = []
    print('crawling started...')
    for submission in reddit.subreddit('nus').search(module):
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            # do not scrape any comments with links (likely to be a generated message)
            elif re.search('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', top_level_comment.body):
                continue
            # ignore deleted comments
            elif top_level_comment.body == "[deleted]":
                continue
            result.append(top_level_comment.body)

    print('crawling ended: {} posts crawled '.format(len(result)))
    return result


