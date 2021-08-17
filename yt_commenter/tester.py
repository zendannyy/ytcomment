#!/usr/bin/env python3

# tester script for api requests 
# from YTComment.yt_commenter.yt_commenter.settings import API_KEY
# from YTComment.yt_commenter.yt_commenter_app.views import comment
from django.http import response
import requests
from googleapiclient.discovery import build
from yt_commenter import secrets
from secrets import *
import argparse


def analyt(analytics):
    """making one off requests to YT Data API"""
    API_KEY = secrets.YT_KEY
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.channels().list(
    part='statistics',
    forUsername=analytics
    )
    response = request.execute()
    print(response)
    # response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    # print(response)

def get_comments(comments):
    """fetch comments for spefic video using videoId param"""
    API_KEY = secrets.YT_KEY
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part='replies',
        videoId=comments,
        textFormat="plainText"
    )
    # .execute()
    response = request.execute()

    # for i in response['items']:
    #     # print(i.values())
    #     snippet = i['kind']
    #     text = snippet[0]
    #     print(text)
        # comment = i['snippet']['textDisplay']
        # print("Top comments & replies: ", comment)
        
    
    # return request["items"]
    print(response)


def main():
    """argparser for cli options"""
    parser = argparse.ArgumentParser(description="""Tester for YT Data API and different inputs""")
    parser.add_argument('-a', '--analytics', help='Performs a basic analytics lookup for the user\'s channel entered')
    parser.add_argument('-c', '--comments', help='Performs a lookup of comments for the video id entered')
    args = parser.parse_args()

    if args.analytics:
        analytics = args.analytics
        analyt(analytics)

    if args.comments:
        comments = args.comments
        get_comments(comments)


if __name__ == '__main__':
    main()
