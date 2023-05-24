import tweepy
import configparser
import csv
import pandas as pd


class TwitterTweetGrepper:
    def __init__(
        self,
        conf_file="/Users/lucasdecastro/Documents/ESIEA/UoM/python/project/conf/config.ini",
    ):
        self.__load_conf(conf_file)
        self.__auth()

    def __load_conf(self, conf_file) -> None:
        config = configparser.ConfigParser()
        config.read(conf_file)

        self.__api_key = config["twitter"]["api_key"]
        self.__api_key_secret = config["twitter"]["api_key_secret"]
        self.__access_token = config["twitter"]["access_token"]
        self.__access_token_secret = config["twitter"]["access_token_secret"]
        print("Config successfuly loaded!")

    def __auth(self) -> None:
        auth = tweepy.OAuthHandler(self.__api_key, self.__api_key_secret)
        auth.set_access_token(self.__access_token, self.__access_token_secret)
        self.__api = tweepy.API(auth, wait_on_rate_limit=True)
        print("Successfuly authenticated to twitter API!")

    def get_tweets_by_tag(self, hashtag: str, limit: int = 300) -> pd.DataFrame():
        hashtag = "#" + hashtag
        data = []

        tweets = tweepy.Cursor(
            self.__api.search_tweets, q=hashtag, tweet_mode="extended"
        ).items(limit)

        # Iterate through the results and append them to the list
        for tweet in tweets:
            try:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.retweeted_status.full_text])
            except AttributeError:  # Not a Retweet
                data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

        return data

    def tweets_to_csv(self, tweets: list, filename: str = "output.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(tweets)
