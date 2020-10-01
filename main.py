from contest_functions import *
from fake_human import *
from threading import Thread

def main():
    contest_thread = Thread(target=twitter_contest_search, args=('#Concours RT', 5000))
    fake_human_thread = Thread(target=fake_retweet)

    fake_human_thread.start()
    contest_thread.start()

if __name__ == '__main__':
    main()