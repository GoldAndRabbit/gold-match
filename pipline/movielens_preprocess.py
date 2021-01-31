import pandas as pd

ROOT_PATH          = '/media/psdz/hdd/Download/movielens/ml-25m/'
links_path         = ROOT_PATH + 'links.csv'
genome_scores_path = ROOT_PATH + 'genome-scores.csv'
genome_tags_path   = ROOT_PATH + 'genome-tags.csv'
movies_path        = ROOT_PATH + 'movies.csv'
ratings_path       = ROOT_PATH + 'ratings.csv'
tags_path          = ROOT_PATH + 'tags.csv'

links = pd.read_csv(links_path)
