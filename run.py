from crawler import crawl
from analyser import get_sentiments
from sentiment_bot import run_sentiment_bot

def run():
    #data = ["so stupid", "hello", "i love this", "best one"]
    #report = get_sentiments(data, "random", "boonlong")
    run_sentiment_bot()


if __name__ == '__main__':
    run()