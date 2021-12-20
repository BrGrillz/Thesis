import json
from bs4 import BeautifulSoup
import requests as req
import random as r
from googleapiclient.discovery import build
import Accounts as ac
import sqlite3 as sl
import os
import glob
import pandas as pd
import isodate

# os.chdir("D:\\DataSets")
# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')


first_video = ac.first_video1
account_number = 'account1'
account_cookie = ac.account_1



def insert_into_database(video_info):

    con = sl.connect('DataSet.sqlite')
    cursor = con.cursor()
    cursor.execute("insert into RECOMENDATION_DATA (account_id, video_id, video_title, channel_name, video_duration, date_of_publication, number_of_views, number_of_likes, video_category, number_of_dislikes, number_of_comments) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (video_info[0], video_info[1], video_info[2], video_info[3], video_info[4], video_info[5], video_info[6], video_info[7], video_info[8], video_info[9], video_info[10]))
    con.commit()
    cursor.close()
    return


def get_service():
    service = build('youtube', 'v3', developerKey=ac.API_KEY)
    return service


def get_random_video(array_of_ids):
    range_of_ids =len(array_of_ids)
    random_number = r.randrange(1, range_of_ids, 1)
    random_video = array_of_ids[random_number]
    return random_video


def get_html_data(video_id):
    url = "https://www.youtube.com/watch?v="+video_id
    response = req.get(url, cookies=account_cookie)
    soup = BeautifulSoup(response.text, 'lxml')
    prepared_html = soup.findAll("script")[40].text.partition('= ')[2].partition('};')[0] + '}'
    deserialized_html = json.loads(prepared_html)
    return deserialized_html


def get_array_of_video_id(html):
    htm_data = html['playerOverlays']['playerOverlayRenderer']['endScreen']['watchNextEndScreenRenderer']['results']
    array_of_video_id = []
    for i in htm_data:
        if i.__contains__('endScreenVideoRenderer'):
            array_of_video_id.append(i['endScreenVideoRenderer']['videoId'])
    return array_of_video_id


def get_channel_info():
    for video_id in ac.array_of_popular_channel_video_id:
        print(video_id)
        video_info = get_service().videos().list(id=video_id, part='snippet,statistics,contentDetails').execute()
        statistics = video_info['items'][0]['statistics']
        content_details = video_info['items'][0]["contentDetails"]
        snippet = video_info['items'][0]['snippet']
        video_duration = content_details["duration"]
        number_of_likes = None
        if statistics.__contains__('likeCount'):
            number_of_likes = statistics["likeCount"]
        number_of_comments = None
        if statistics.__contains__('commentCount'):
            number_of_comments = statistics["commentCount"]
        number_of_views = None
        if statistics.__contains__('viewCount'):
            number_of_views = statistics['viewCount']
        channel_id = snippet['channelId']
        get_channel_video_number = get_service().channels().list(id=channel_id, part='statistics').execute()
        channel_video_count = get_channel_video_number['items'][0]['statistics']['videoCount']
        con = sl.connect('DataSet.sqlite')
        cursor = con.cursor()
        cursor.execute(
            "insert into NewData (video_duration, number_of_likes, number_of_comments, number_of_views, channel_video_count) values (?, ?, ?, ?, ?)",
            (isodate.parse_duration(video_duration).seconds, number_of_likes, number_of_comments, number_of_views, channel_video_count))
        con.commit()
        cursor.close()


get_channel_info()

def get_video_info(video_id):
    video_info = get_service().videos().list(id=video_id, part='snippet,statistics,contentDetails').execute()
    snippet = video_info['items'][0]['snippet']
    statistics = video_info['items'][0]['statistics']
    account_id = account_number
    video_title = snippet['title']
    channel_name = snippet["channelTitle"]
    video_duration = video_info['items'][0]["contentDetails"]["duration"]
    date_of_publication = snippet['publishedAt']
    number_of_views = None
    if statistics.__contains__('viewCount'):
        number_of_views = statistics['viewCount']
    number_of_likes = None
    if statistics.__contains__('likeCount'):
        number_of_likes = statistics["likeCount"]
    video_category = snippet["categoryId"]
    number_of_dislikes = None
    if statistics.__contains__('dislikeCount'):
        number_of_dislikes = statistics["dislikeCount"]
    number_of_comments = None
    if statistics.__contains__('commentCount'):
        number_of_comments = statistics["commentCount"]
    return account_id, video_id, video_title, channel_name, video_duration, date_of_publication, number_of_views, number_of_likes, video_category, number_of_dislikes, number_of_comments


def next_video():
    html_data = get_html_data(first_video)
    i = 0
    while i<200:
        i += 1
        print(i)
        array_of_ids = get_array_of_video_id(html_data)
        for video_id in array_of_ids:
            video_info = get_video_info(video_id)
            insert_into_database(video_info)
        random_video_id = get_random_video(array_of_ids)
        html_data = get_html_data(random_video_id)

# for max and min video length

# def next_video():
#     html_data = get_html_data(first_video)
#     i = 0
#     while i<100:
#         i += 1
#         array_of_ids = get_array_of_video_id(html_data)
#         duration_array = []
#         for video_id in array_of_ids:
#             video_info = get_video_info(video_id)
#             insert_into_database(video_info)
#             duration_array.append(video_info[4])
#         video_duration_time = []
#         for duration_str in duration_array:
#             video_duration_time.append(isodate.parse_duration(duration_str))
#         least_duration_video_index = video_duration_time.index(min(video_duration_time))
#         least_duration_video = array_of_ids[least_duration_video_index]
#         html_data = get_html_data(least_duration_video)
#     print(i)
#     while i<200:
#         i += 1
#         array_of_ids = get_array_of_video_id(html_data)
#         duration_array = []
#         for video_id in array_of_ids:
#             video_info = get_video_info(video_id)
#             insert_into_database(video_info)
#             duration_array.append(video_info[4])
#         video_duration_time = []
#         for duration_str in duration_array:
#             video_duration_time.append(isodate.parse_duration(duration_str))
#         least_duration_video_index = video_duration_time.index(max(video_duration_time))
#         least_duration_video = array_of_ids[least_duration_video_index]
#         html_data = get_html_data(least_duration_video)



# next_video()