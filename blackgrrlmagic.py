#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by Selina Musuta - @pumzi_code

# Goals:  I want to be able to follow all users that #blackgirlmagic (and other variations). I want to retweet those tweets
# Questions for Selina:  What are the parameters?
# .gitignore should include credentials.py (contains my keys and tokens that i do not want to share publicly)

# Challenges: Twitter has a rate limit.  Worried about being tagged as spam by Twitter.

# Notes 4 the Future: 
#Add StreamListener object to monitor tweets in real time and catches them.
# Build a chronjob
# Import credentials as a module

# Import Tweepy, time
# "Tweepy makes it easier to use the twitter streaming api by handling authentication, connection, creating and destroying the session, reading incoming messages, and partially routing messages."
import tweepy, time

# Import csv
import csv

# Import sys for use of sys.stdout (system specific parameters and functions)
import sys

# Configure Twitter API Throttle to every 15 seconds to avoid the fail whale
# https://dev.twitter.com/rest/reference/get/users/lookup
# API documentation:  Only 180 requests allowed per 15 minute interval
api_sleep = 15 

# up to 100 users fetched per request
api_user_page_size = 100

# Consumer key, consumer secret, access token, access secret allows access to the twitter API
cons_key =  " "
cons_secret =   " "
access_token =  " "
access_token_secret = " "

# Create an authorization variable that the OAuthHandler class passes the consumer key and consumer secret
auth = tweepy.OAuthHandler(cons_key, cons_secret)

# The auth variable has an attribute that passes the access token and the secret access token
auth.set_access_token(access_token, access_token_secret)

# Setting the API with authorization keys
api = tweepy.API(auth)

# Setting an empty list called Users
users = []

# Count will start as 1
count = 1

# Write a function that sets sleep limit
def throttleapi():
    time.sleep(api_sleep)

# In this example, call throttleapi() function that was set time.sleep(15)
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            throttleapi()

# Write a function that uses the blackgirlmagic query to fetch users name, the time/date they created the post and print out 100 unique user results. Later create a function to save user

def fetch_users(followers):
    for tweet in limit_handled(tweepy.Cursor(api.search, q=('blackgirlmagic')).items(api_user_page_size)):
        print "Name:", tweet.author.name.encode('utf8')
        print "Tweet created:", tweet.created_at
        user = tweet.author.screen_name.encode('utf8')
        print user
        print "//////////////////"
        if not users.__contains__(user):
            users.append(user)
            count += 1
            print count
    print '====================List of unique users in total' + str(len(users))
    for u in users:
        print u

# Future:  Write a function that will write followers meta-data and encode the output
def save_record(result):
    # Create the csv row, delimited by commas, text-qualified with double quotes
    # line continuations for readability (backslashes)
    record = '"'+ \
        u.screen_name+'", "'+ \
        u.name+'", "'+ \
        u.location+'", "'+ \
        u.description \
        +'"\n'
    # Encoding the output to avoid defaulting 'ascii' which generated an error upon output redirection
    sys.stdout.write(record.encode('utf-8'))