# 1. Fetch/Search @rahul_grover99 
# 2. Check if video is present in the tweet
# 3. Query the DB
# 4. Call classifier
# 5. Comment Fake or not

import pandas as pd
import requests
import cv2
from inference_scripts.predict_folder import classify
from requests_oauthlib import OAuth1
import threading

def searchTweetIDInFile(tweet_id):
    df = pd.read_csv('tweet_ids.csv')
    for id in df['tweet_id']:
        # print(id, tweet_id)
        if str(id) == str(tweet_id):
            return True
    return False

def insertTweetIDinFile(tweet_id):
    file1 = open("tweet_ids.csv", "a")  # append mode 
    file1.write(tweet_id + "\n") 
    file1.close() 


def getFrames(file_path):
    cap = cv2.VideoCapture(file_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length


def getTweets():
    url = "https://api.twitter.com/1.1/search/tweets.json?q=@rahul_grover99&count=100"

    payload={}
    headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAHZ7JwEAAAAAtMhQwVTRQtav1qbhreIQpx8mbH8%3Do5T9Gv462jf4MoJOAJ19oRnLMWmXmOeHqzpp0HzX9ovNm7I0SI',
    'Cookie': 'personalization_id="v1_VIUj6hiI6FiSRMW4xROMgQ=="; guest_id=v1%3A159091927093030167'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response)
    return response.json()

def getVideoLinks(response):
    video_links = []
    df = response["statuses"]
    for tweet in df:
        tweet_id_str = tweet["id_str"]
        if searchTweetIDInFile(tweet_id_str) == False:
            insertTweetIDinFile(tweet_id_str)
            print(tweet.keys())
            if "extended_entities" in tweet.keys():
                video_links.append((tweet["extended_entities"]["media"][0]["video_info"]["variants"][0]["url"], tweet_id_str))
    return video_links


def download_video(video_link):
    # url = 'https://www.facebook.com/favicon.ico'
    r = requests.get(video_link, allow_redirects=True)
    file_name = video_link.split("/")[-1]
    final_name = file_name.split("?")[0]
    open(final_name, 'wb').write(r.content)
    return final_name


def comment(id, message):
    url = 'https://api.twitter.com/1.1/statuses/update.json'

    auth = OAuth1("dVbvxSAZtYVTlxseQKWoBG2eI", "tgu6HAn8hV6W0JGNfJEWnGc778Zt06MOikkRIovpARq5vwuzFg",
                  "1060240040045903872-J4LIx2MarbGPiQ0OqHX2Y4x5apBhlY", "f6vGF9OBjtpzqR7cxVS7frIVOO5QpHi3wWb6gIVFCNTAP")
    params = {
        'status': message,
        'in_reply_to_status_id': id,
        'auto_populate_reply_metadata': 'true'
    }

    response = requests.post(url, auth=auth, params=params)
    print(response.status_code)

# print(searchTweetIDInFile(12))
# print(searchTweetIDInFile(1))
# insertTweetIDinFile("1")
# print(searchTweetIDInFile(1))



# comment("1330190028161642497", "Hi")
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def func():
    print("start")
    js = getTweets()

    for link, tweet_id in getVideoLinks(js):
        name = download_video(link)
        frames = getFrames(name)
        output = classify(name, frames)
        if (output > 0.5):
            msg = "Fake"
        else:
            msg = "Real"
        comment(tweet_id, msg)

    print("end")


set_interval(func, 600)