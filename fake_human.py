import tweepy
import random
import time

# Tokens and access definition

auth = tweepy.OAuthHandler('XXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXX')
auth.set_access_token('XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXX')
api = tweepy.API(auth)

# Topic lists and creation of random topic selection

travel_list = ['Voyages', 'Lonely Planet', 'Travels']
food_list = ['foodie', 'food recipe', 'recette']
vg_list = ['video game', 'Kotaku', 'Gamespot', 'Jeuxvideo.com']

sequences = travel_list, food_list, vg_list
random_topic = random.choice(random.choice(sequences))

# Gets the random topic and for each of the 100 first items of the search results, posts a retweet with a comment
# related to the random topic selected, then waits a random amount of time between 10 seconds and 1 hour to post
# the next one

def fake_retweet():
    global fh_tweet
    for fh_tweet in tweepy.Cursor(api.search, random_topic, tweet_mode='extended').items(100):
        rand_pause = random.randrange(10, 3600)
        if random_topic in travel_list:
            random_line('travel_sentences.txt')
        elif random_topic in food_list:
            random_line('food_sentences.txt')
        else:
            random_line('it_sentences.txt')
        time.sleep(rand_pause)


def random_line(topic):
    with open(topic) as file:
        opened_file = file.read()
        random_sentence = random.choice(opened_file.splitlines())
        api.update_status(f'{random_sentence}', attachment_url=f'https://twitter.com/{fh_tweet.user.screen_name}/status/{fh_tweet.id}')