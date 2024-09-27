# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkiItem(scrapy.Item):
    pass


class DetailItem(scrapy.Item):
    # 中英文
    english_name = scrapy.Field()
    chinese_name = scrapy.Field()

    # 收录
    journalType2 = scrapy.Field()
    # 数据库
    database = scrapy.Field()

    # 复合影响因子
    impactFactors = scrapy.Field()
    # 综合影响因子
    comprehensiveImpactFactors = scrapy.Field()

    # "主办单位": "
    hostUnit = scrapy.Field()
    # "出版周期": "
    publicationPlace = scrapy.Field()
    issn = scrapy.Field()
    cn = scrapy.Field()
    # "出版地": "
    publicationPlace = scrapy.Field()
    # 语种": "
    languageName = scrapy.Field()
    # 开本":
    size = scrapy.Field()
    # 创刊时间": "
    launchYear = scrapy.Field()
    # 专辑名称": "album",
    album = scrapy.Field()
    # "专题名称": "topic",
    topic = scrapy.Field()
    # "出版文献量": "
    publicCount = scrapy.Field()
    # "总下载次数": "
    downloadAmount = scrapy.Field()
    # "总被引次数": "
    quoteAmount = scrapy.Field()


class XztgItem(scrapy.Item):
    baseId = scrapy.Field()
    reviewCycle = scrapy.Field()
    publicationCycle = scrapy.Field()
    hostUnit = scrapy.Field()
    editorInChief = scrapy.Field()
    deputyEditor = scrapy.Field()
    submissionEmail = scrapy.Field()
    phone = scrapy.Field()
    sponsor = scrapy.Field()
    website = scrapy.Field()
    hasFee = scrapy.Field()
    timeLag = scrapy.Field()