#!/usr/bin/env python3

# tester script for api requests 
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

def get_comments(comments):
    """fetch comments for spefic video using videoId param"""
    API_KEY = secrets.YT_KEY
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part='replies',
        videoId=comments,
        textFormat="plainText"
    )

    response = request.execute()

    video = response['items'][0]['replies']['comments']


    for i in video:
        print('\n')
        print(i['snippet']['textDisplay'])
    # print(response['items'][0].keys())


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
