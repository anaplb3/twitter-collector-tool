import tweepy, random, time, json
from unicodedata import normalize
from tweetcollector.db import Database
from tweetcollector.report import Report
from tweetcollector.senticnet_instance import Sentiment
from auth import access_token, access_token_secret, consumer_key, consumer_secret
import tweetcollector.json_utils as js
from environment import set_env
from config import GLOBAL_CFG
import snscrape.modules.twitter as sntwitter
from datetime import date

class Collector():
    def __init__(self):
        self.db = Database()
        self.st = Sentiment()
        self.rp = Report()
        #self.auth = tweepy.OAuthHandler(GLOBAL_CFG['consumer_key'], GLOBAL_CFG['consumer_secret'])
        #self.auth.set_access_token(GLOBAL_CFG['access_token'], GLOBAL_CFG['access_token_secret'])
        self.index = 0
        self.state = ""
        self.count_tweets = 0   

    def collect(self, min_per_query = 15, min_search = 1440):
        search_time = time.time() + min_search * 60
        print("Collect began at {}".format(time.asctime(time.localtime(time.time()))))
        while time.time() < search_time:
            timeout = time.time() + min_per_query * 60
            query = self.creating_query()
            try:
                self.doing(timeout, query)
            except tweepy.error.TweepError:
                error_time = time.time()
                print("Rate limit exception. Time: {}".format(error_time))
                time.sleep(30)
                #time.sleep(30)
                #min_search = (search_time - error_time) / 60
                self.collect(min_per_query,min_search)

            print("tweets for state {}: {}".format(self.state, self.count_tweets))

    def doing(self,timeout, query):
        #api = self.auth_()
        #last = self.rp.last_id(query)
        last = js.get_last_id(self.state)
        since = self.db.get_since_date(self.state)
        today_date = date.today()
        print('collecting tweets with key %s' %normalize('NFKD', query).encode('ASCII', 'ignore').decode('ASCII'))
        print("last: {}".format(last))
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('{} since:{} until:{} since_id:{}'.format(query, js, since, today_date)).get_items()):
            if i > 100:
                print("bateu 100 tweets")
                break
            if tweet:
                self.count_tweets += 1
                self.db.save(tweet, query, self.state)
                #self.rp.last_id_tweet(query,tweet.id)
                js.save_last_id(self.state, tweet.id)
        self.db.set_since_date(since, self.state)

    def auth_(self):
        api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        return api

    def creating_query(self):
        data = self.st.getData()[self.index]
        self.update_index()
        self.state = data[0]
        return "vacinas OR vacina OR vacinacao OR vacinação ({} OR {})".format(data[1], data[2])

    def update_index(self):
        if self.index == 13:
            self.index = 0 
        else: 
            self.index += 1