import GetOldTweets3 as got
import snscrape.modules.twitter as sntwitter

def extract_tweets(query): 
      
    gettweet= got.manager.TweetCriteria().setQuerySearch(query).setSince("2021-01-17").setUntil("2021-05-01").setMaxTweets(5) 
      
    # Creation of list that contains all tweets 
    tweets = got.manager.TweetManager.getTweets(gettweet) 
      
    # Creating list of chosen tweet data 
    text_tweets = [[tweet.text] for tweet in tweets] 
    print(text_tweets) 


def snl():
    last = 1373977398891450374
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('vacinas OR vacina OR vacinacao OR vacinacao (@FlavioDino OR @GovernoMA) max_id:{} since:2021-01-17 until:2021-05-01'.format(last)).get_items()):
        if i>5:
            break
        last = tweet.id
        print("\n")
        print("tweet id: {}".format(tweet.id))
        print("tweet text: {}".format(tweet.content))
        print("tweet date: {}".format(tweet.date))
    #tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
  
# calling the function 
#extract_tweets("vacinas OR vacina OR vacinacao OR vacinacao (@FlavioDino OR @GovernoMA)") 
snl()