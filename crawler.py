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
            # do not scrape any comments with links (likely to be a generated message) or comments that were deleted/removed
            elif re.search('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', top_level_comment.body) or\
                top_level_comment.body == "[deleted]" or top_level_comment.body == "[removed]":
                continue
            # ignore posts with other module codes inside
            elif re.search('[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}', top_level_comment.body) and\
                (module.lower() not in re.findall('[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}', top_level_comment.body) and\
                    module.upper() not in re.findall('[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}', top_level_comment.body)):
                continue
            # ignore short comments - high chance not related
            elif len(top_level_comment.body.split(" ")) <= 10:
                continue
            result.append(top_level_comment.body)

    print('crawling ended: {} posts crawled '.format(len(result)))
    return result


