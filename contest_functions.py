import re
import time
import tweepy

# Tokens and access definition

auth = tweepy.OAuthHandler('XXXXXXXXXXXX', 'XXXXXXXXXXXX')
auth.set_access_token('XXXXXXXXXXXX', 'XXXXXXXXXXXX')
api = tweepy.API(auth)

# Search function, with a sleep to avoid hitting the Twitter API request limit

def twitter_contest_search(search, numberoftweets):
    global count
    count = 1
    global nbt
    nbt = numberoftweets
    for tweet in tweepy.Cursor(api.search, search, tweet_mode='extended').items(numberoftweets):
        try:
            print(f'*****Parsing tweet {count}/{nbt}...*****')
            contest_participation(tweet)
            count += 1
            time.sleep(2)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# Parsing and RT/FAV/Friend mentions, excluding retweets to avoid false positives. Also ignoring a specific account name
# that's a contest bot troll account! A regex finds all occurrences of words starting with an at sign, that is,
# twitter account handles to follow

def contest_participation(tweet):
    global tusn
    tusn = tweet.user.screen_name
    if not tweet.full_text.startswith('RT ') and tusn != 'jflessauSpam' and tusn != 'rt_follow_like':
        print(f'*****Tweet {count}/{nbt} is a contest tweet! Parsing...*****')
        pattern = re.compile(r'@\w+')
        handles = pattern.findall(tweet.full_text)
        api.create_favorite(tweet.id)
        api.create_friendship(tweet.user.id)
        api.retweet(tweet.id)
        for handle in handles:
            api.create_friendship(handle)
        if 'Mentionne' in tweet.full_text:
            mention_management(tweet)
        if 'TWEET' in tweet.full_text:
            tweet_pattern = re.compile(r"TWEET #\w+")
            tp_verification = tweet_pattern.match(tweet.full_text)
            print(tp_verification[5:])
        print('*****Parsing done.*****\n')
        time.sleep(60)

# Parsing the number of mentions needed. Identifies the letter or number following "Mentionne", which will give away the
# number of accounts to mention in the answer ("u" is for "un", "d" is for "deux")

def mention_management(tweet):

    mention_text = tweet.full_text
    mention_number = mention_text.partition('Mentionne ')[2][0]
    try:
        if mention_number == 'u' or '1':
             api.update_status(f'@{tusn} @first_friend_account', in_reply_to_status_id=tweet.id)
        elif mention_number == 'd' or '2':
             api.update_status(f'@{tusn} @first_friend_account @second_friend_account', in_reply_to_status_id=tweet.id)
    except:
        print('Number out of range or incorrect')
        pass
