import time
import sys
import random
import math
import json
import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "4mwWPLkDPGt1PFVV61YRhd4DO"
consumer_secret = "tZVLdbwRvYPee5wvQVGAiD0MKmuO8lm0Pdg2o3tnDqEvfSBWZC"
access_key = "709108657410052096-AspCZbUSsD9MLeYxjYC2CVJeZfFeWza"
access_secret = "rP6YlWhSeBPAG7e5RHrrGyFqGEq43LwOvb7p35INb8R5G"


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print("...%s tweets downloaded so far" % (len(alltweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 

    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.replace("&amp;", "and").replace(",","").replace(";","").replace("\n"," "), tweet.retweet_count] for tweet in alltweets]
    
    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text", "RT"])
        writer.writerows(outtweets)
    
    pass



tweeters = ['realDonaldTrump','BernieSanders', 'HillaryClinton', 'RealBenCarson', 'BarackObama','kanyewest','KimKardashian','mindykaling','officialjaden','ConanOBrien','karpathy','AndrewYNg','johnplattml','geoff_hinton','pmddomingos','god','chuck_facts','big_ben_clock','Lord_Voldemort7','BronxZooCobra']

for tweeter in tweeters:
    get_all_tweets(tweeter)
             