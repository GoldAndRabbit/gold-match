import os
import requests
import unicodedata
import logging
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup

ROOT_PATH          = '/media/psdz/hdd/Download/movielens/ml-25m/'
PROJECT_ROOT_PATH  = '/home/psdz/repos/gold-match/imdb_movie_info_crawler/'
links_path         = ROOT_PATH + 'links.csv'
genome_scores_path = ROOT_PATH + 'genome-scores.csv'
genome_tags_path   = ROOT_PATH + 'genome-tags.csv'
movies_path        = ROOT_PATH + 'movies.csv'
ratings_path       = ROOT_PATH + 'ratings.csv'
tags_path          = ROOT_PATH + 'tags.csv'
links   = pd.read_csv(links_path)
ratings = pd.read_csv(ratings_path)

total_imdbids  = links['imdbId'].unique().tolist()
total_movieids = links['movieId'].unique().tolist()
print('length of imdbids :', len(total_imdbids))   # length of imdbids 62423
print('length of movieids:', len(total_movieids))  # length of movieid 62423

def get_movieid_to_imdbid_map():
    movie_dict = {}
    with open(links_path) as fb:
        fb.readline()
        for line in fb:
            line = line.strip()
            line = line.split(',')
            movie_dict[line[0]] = line[1]
    return movie_dict

def get_downloaded_movies():
    downloaded_movies = []
    for moive_id_jpg in os.listdir(ROOT_PATH + 'download_posters'):
        movie_id = int(moive_id_jpg.replace(".jpg", ""))
        downloaded_movies.append(movie_id)
    downloaded_movies = sorted(downloaded_movies)
    return downloaded_movies

movie_map          = get_movieid_to_imdbid_map()
downloaded_movies  = get_downloaded_movies()
missing_pic_movies = [movieid for movieid in total_movieids if movieid not in downloaded_movies]
print('the length of downloaded_movies' , len(downloaded_movies))  # the length of downloaded_movies : 62039
print('the length of missing_pic_movies', len(missing_pic_movies)) # the length of missing pic movies: 384

def get_release_year_from_time(time):
    import re
    year = 1900
    if type(time) is str:
        search_year = re.search('\d{4}', time)
        if search_year is not None:
            year = int(search_year.group())
    return year

def get_location_from_release(name):
    import re
    loc = 'other'
    if type(name) is str:
        usa_flag   = re.search('USA', name)
        uk_flag    = re.search('UK', name)
        # china_flag = re.search('China', name)
        if usa_flag is not None:
            loc = 'usa'
        # if china_flag is not None:
        #     loc = 'china'
        if uk_flag is not None:
            loc = 'uk'
    return loc

def get_pure_name(name):
    import re
    pure_name = 'unkown'
    if type(name) is str:
        pure_name = re.sub('\d', '', name)
        pure_name = pure_name.replace('(', '')
        pure_name = pure_name.replace(')', '')
    return pure_name

col_names = [
    'movieid',
    'name',
    'pic_url',
    'duration',
    'type',
    'release_time',
    'intro',
    'director',
    'screenwriter',
    'actor'
]

movie_infos = pd.read_csv(PROJECT_ROOT_PATH + 'infos/info.csv', names=col_names)
movie_infos['year']  = movie_infos['release_time'].apply(get_release_year_from_time)
movie_infos['loc']   = movie_infos['release_time'].apply(get_location_from_release)
movie_infos['name']  = movie_infos['name'].apply(get_pure_name)

# sample movies
# 这里需要增加一个筛选: 保留有poster的movie
sampled_movies_info = movie_infos[
    (movie_infos['year']   >= 1990)         # movie later than 1990
    & (movie_infos['loc']  != 'other')      # only from USA or UK
    & (movie_infos['name'] != 'unkown')     # must have movie name
]

# sampled_movies_info = sampled_movies_info[['movieid', 'name', 'type', 'intro', 'loc']]
sampled_movies = sampled_movies_info['movieid'].unique().tolist()

# exeute in 15 min: use tqdm to view realtime progress
from tqdm import tqdm
legal_flags = []
for movieid in tqdm(ratings['movieId'].tolist()):
    if movieid in sampled_movies:
        legal_flags.append(1)
    else:
        legal_flags.append(0)

ratings['flag'] = legal_flags
sampled_ratings = ratings[ratings['flag'] == 1]
print('the length of sampled_ratings: ', sampled_ratings.size())
