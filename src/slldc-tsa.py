from slldclib.ttg import TwitterTweetGrepper

def main():
    ttg = TwitterTweetGrepper()
    tweets = ttg.get_tweets_by_tag('MonacoGP', limit=10000)
    ttg.tweets_to_csv(tweets)
    
if __name__ == "__main__":
    main()