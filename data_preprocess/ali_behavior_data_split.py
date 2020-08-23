import time
import pickle
from pathlib import Path
import pandas as pd


def timestamp2date(x):
    format = '%Y%m%d'
    value = time.localtime(x)
    dt = time.strftime(format, value)
    return dt

def timestamp2time(x):
    format = '%H%M%S'
    value = time.localtime(x)
    dt = time.strftime(format, value)
    return dt

def generate_train_test_pkl():
    INPUT_PATH = '/media/psdz/hdd/Download/ali_behavior/'
    OUTPUT_PATH = '/media/psdz/hdd/Download/ali_behavior/sample_data/'
    train_pkl_file = Path(OUTPUT_PATH + 'train.pkl')
    test_pkl_file = Path(OUTPUT_PATH + 'train.pkl')

    if train_pkl_file.is_file() and test_pkl_file.is_file():
        print('train and test pkl files are exit.')
        df_train = pickle.load(open(OUTPUT_PATH + 'train.pkl', 'rb'))
        df_test = pickle.load(open(OUTPUT_PATH + 'test.pkl', 'rb'))
    else:
        print('train and test pkl files are not exit. start dump...')
        cols = ['user_id', 'item_id', 'cate_id', 'type', 'timestamp']
        used_cols = ['user_id', 'item_id', 'type', 'timestamp']
        df_total = pd.read_csv(INPUT_PATH + 'UserBehavior.csv', names=cols)
        df_total = df_total[used_cols]
        # df_total = df_total.head(100)
        df_total['date'] = df_total['timestamp'].apply(timestamp2date)
        df_total['time'] = df_total['timestamp'].apply(timestamp2time)
        df_total = df_total.drop(['timestamp'],axis=1)
        df_train = df_total.loc[df_total['date'] <= '20171202']
        df_train = df_train.reset_index(drop=True)
        df_test = df_total.loc[df_total['date'] == '20171203']
        df_test = df_test.reset_index(drop=True)
        pickle.dump(df_train,open(OUTPUT_PATH + 'train.pkl','wb'))
        pickle.dump(df_test,open(OUTPUT_PATH + 'test.pkl','wb'))


if __name__ == '__main__':
    generate_train_test_pkl()

