from pathlib import Path
import os

import pandas as pd
from Scweet.scweet import scrape
import Scweet
from Scweet.user import get_user_information, get_users_following, get_users_followers

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)

TARGET_TWITTER_ACCOUNT = 'europejskafirma'
PARQUET_PATH = f'final_output/{TARGET_TWITTER_ACCOUNT}.parquet'
TXT_PATH = f'final_output/{TARGET_TWITTER_ACCOUNT}.txt'
OUTPUT_DIR = 'outputs'
COOKIES_DIR = 'cookies'

def get_data():
    df = scrape(since="2026-01-09", until="2026-01-11", from_account ='europejskafirma', interval=1,
                  headless=True, display_type="", save_images=False,
                  resume=False, filter_replies=True, proximity=True, cookies_dir=COOKIES_DIR, cookie_id=None, outputs_dir=OUTPUT_DIR)


def merge_parquets():
    data_dir = Path(OUTPUT_DIR)
    full_df = pd.concat(
        pd.read_parquet(parquet_file)
        for parquet_file in data_dir.glob('*.parquet')
    )

    filtered_df = full_df.drop_duplicates(['Tweet URL']).reset_index()
    print(f'Dropped duplicates from: {len(full_df)} to {len(filtered_df)}')
    print(filtered_df.head(5))
    print(filtered_df.tail(5))
    print(filtered_df.columns)
    return filtered_df

def save(df):
    df['Embedded_text'] = df['Embedded_text'].str.replace('\n', ' ')
    df.to_parquet(PARQUET_PATH)
    with open(TXT_PATH, 'w') as f:
        for index, row in df.iterrows():
            # print(row['Embedded_text'])
            f.write(f"{row['Embedded_text']}\n")

get_data()
df = merge_parquets()
save(df)