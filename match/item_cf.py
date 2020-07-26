import math
import numpy as np
from tqdm import tqdm
from collections import defaultdict

def make_item_time_tuple(group_df, user_col='user_id', item_col='item_id', time_col='time'):
    # group_df = group_df.drop_duplicates(subset=[user_col, item_col], keep='last')
    item_time_tuples = list(zip(group_df[item_col], group_df[time_col]))
    return item_time_tuples

def get_user_item_time_dict(df, user_col='user_id', item_col='item_id', time_col='time', is_drop_duplicated=False):
    user_item_ = df.sort_values(by=[user_col, time_col])

    if is_drop_duplicated:
        print('drop duplicates...')
        user_item_ = user_item_.drop_duplicates(subset=['user_id', 'item_id'], keep='last')

    user_item_ = user_item_.groupby(user_col).apply(
        lambda group: make_item_time_tuple(group, user_col, item_col, time_col)).reset_index().rename(
        columns={0: 'item_id_time_list'})
    user_item_time_dict = dict(zip(user_item_[user_col], user_item_['item_id_time_list']))
    return user_item_time_dict


def get_time_dir_aware_sim_item(df):
    user_item_time_dict = get_user_item_time_dict(df)

    sim_item = {}
    item_cnt = defaultdict(int)
    for user, item_time_list in tqdm(user_item_time_dict.items()):
        for loc_1, (i, i_time) in enumerate(item_time_list):
            item_cnt[i] += 1
            sim_item.setdefault(i, {})
            for loc_2, (relate_item, related_time) in enumerate(item_time_list):
                if i == relate_item:
                    continue
                loc_alpha = 1.0 if loc_2 > loc_1 else 0.7
                loc_weight = loc_alpha * (0.8 ** (np.abs(loc_2 - loc_1) - 1))
                time_weight = np.exp(-15000 * np.abs(i_time - related_time))

                sim_item[i].setdefault(relate_item, 0)
                sim_item[i][relate_item] += loc_weight * time_weight / math.log(1 + len(item_time_list))

    sim_item_corr = sim_item.copy()
    for i, related_items in tqdm(sim_item.items()):
        for j, cij in related_items.items():
            sim_item_corr[i][j] = cij / math.sqrt(item_cnt[i] * item_cnt[j])

    return sim_item_corr, user_item_time_dict