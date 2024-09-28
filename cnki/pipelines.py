# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pathlib import Path

import pandas as pd

from .settings import ITEM_DICT, SAVE_FILE_NAME


def save_or_add_df(df, filename):
    new_columns = {v: k for k, v in ITEM_DICT.items()}
    if Path(filename).exists():
        old_df = pd.read_excel(filename)
        new_df = pd.concat([old_df, df])
        df = new_df.drop_duplicates(subset="issn")
        df = df.rename(columns=new_columns)
        df.to_excel(filename, index=False)
    else:
        df = df.rename(columns=new_columns)
        df.to_excel(filename, index=False)


class CnkiPipeline:
    def open_spider(self, spider):
        # 初始化一个空列表，保存爬取的数据
        self.data = []

    def close_spider(self, spider):
        # 爬虫结束时，将数据存入Excel
        df = pd.DataFrame(self.data)
        save_or_add_df(df, SAVE_FILE_NAME)

    def process_item(self, item, spider):
        # 每次处理item时，将其添加到data列表中
        self.data.append(item)
        return item
