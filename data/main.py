# This is a sample Python script.
import time

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import praw
import pandas as pd
import numpy as np
import requests
from requests import HTTPError, ConnectionError, Timeout, RequestException
from PIL import Image
import pathlib
import os

# use saved post csv to download images
def just_download():
    advice_df = pd.read_csv('advice.csv')
    memes_df = pd.read_csv('memes.csv')
    # bad_animals = save_images(advice_df, path="images/advice2")
    bad_memes = save_images(memes_df, path="images/memes2")
    with open("bad_links.txt", 'w') as f:
        f.write("bad advice animal links")
        # f.writelines(bad_animals)
        f.write("bad memes links")
        f.writelines(bad_memes)


def main():
    reddit = praw.Reddit("my_app")
    # get posts from advice animals
    subreddit = reddit.subreddit("adviceanimals").top(time_filter="all", limit=100)
    # put in dataframe
    posts = [{"title":submission.title, "permalink":submission.permalink, "url":submission.url} for submission in subreddit]
    advice_frame = pd.DataFrame(posts)
    # fix imgur links to be direct to image
    advice_frame["url"] = np.where(
        advice_frame["url"].str.startswith("https://imgur.com"),
        "https://i.imgur.com" + "/" + advice_frame["url"].apply(lambda x: x.rsplit("/", 1)[-1]) + ".jpeg",advice_frame["url"])
    # save dataframe
    advice_frame.to_csv("advice.csv", index=False)
    # save images
    save_images(advice_frame)
    # repeat above but for memes subreddit
    subreddit = reddit.subreddit("memes").top(time_filter="all", limit=100)
    posts = [{"title":submission.title, "permalink":submission.permalink, "url":submission.url} for submission in subreddit]
    memes_frame = pd.DataFrame(posts)
    memes_frame["url"] = np.where(
        memes_frame["url"].str.startswith("https://imgur.com"),
        "https://i.imgur.com" + "/" + memes_frame["url"].apply(lambda x: x.rsplit("/", 1)[-1]) + ".jpeg", memes_frame["url"])
    memes_frame.to_csv("memes.csv", index=False)
    # save_images(memes_frame)

# returns set of bad links to investigate later
def save_images(dataframe, path="images/advice"):
    path = os.path.join(os.getcwd(), path)
    bad_links = []
    for row in dataframe.iterrows():
        # try 10 times to download images
        data = None
        attempts = 0
        while attempts < 10:
            try:
                response = requests.get(row[1]["url"], timeout=3)
                time.sleep(1)
                data = response.content
                response.raise_for_status()
                # if we get to this point, presumably we have a successful download
                break
            except (ConnectionError, HTTPError, RequestException, Timeout) as err:
                attempts += 1
                time.sleep(2)
        if data is not None:
            print(row[1]["url"])
            with open(os.path.join(path, row[1]["url"].rsplit('/', 1)[-1]), "wb") as f:
                f.write(data)
        else:
            # keep track of bad links for later comparisons
            bad_links.append(row[1]["url"])
    return bad_links


        # f = open(path + row[1]["permalink"] + "jpg", "wb")
        # f.write(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main()
    just_download()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
