# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pathlib import Path

import pandas as pd

from .items import DetailItem, XztgItem


def save_or_add_df(df, filename):
    if Path(filename).exists():
        old_df = pd.read_excel(filename)
        new_df = pd.concat([old_df, df])
        new_df.to_excel(filename, index=False)
    else:
        df.to_excel(filename, index=False)


class CnkiPipeline:
    def process_item(self, item, spider):
        return item


class DetailExcelPipeline:
    def open_spider(self, spider):
        # 初始化一个空列表，保存爬取的数据
        self.data = []

    def close_spider(self, spider):
        # 爬虫结束时，将数据存入Excel
        df = pd.DataFrame(self.data)
        filename = "detail.xlsx"
        save_or_add_df(df, filename)

    def process_item(self, item, spider):
        # 每次处理item时，将其添加到data列表中
        if isinstance(item, DetailItem):
            self.data.append(item)
        return item


class XztgExcelPipeline:
    def open_spider(self, spider):
        # 初始化一个空列表，保存爬取的数据
        self.data = []

    def close_spider(self, spider):
        # 爬虫结束时，将数据存入Excel
        df = pd.DataFrame(self.data)
        filename = "xztg.xlsx"
        save_or_add_df(df, filename)

    def process_item(self, item, spider):
        # 每次处理item时，将其添加到data列表中
        if isinstance(item, XztgItem):
            self.data.append(item)
        return item
