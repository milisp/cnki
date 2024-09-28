# Scrapy settings for cnki project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging

from loguru import logger

BOT_NAME = "cnki"

SPIDER_MODULES = ["cnki.spiders"]
NEWSPIDER_MODULE = "cnki.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "cnki (+http://www.yourdomain.com)"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "cnki.middlewares.CnkiSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "cnki.middlewares.CnkiDownloaderMiddleware": 543,
# }
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "cnki.pipelines.CnkiPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_CONNECT_KWARGS = {"slow_mo": 1000, "timeout": 1_000_000}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 1000 * 1000  # 10 seconds


def should_abort_request(request):
    return request.resource_type == "image" or ".jpg" in request.url


PLAYWRIGHT_ABORT_REQUEST = should_abort_request
PLAYWRIGHT_CONTEXTS1 = {
    "default": {},
    "persistent": {
        "user_data_dir": "/tmp/cnki-chrome",  # will be a persistent context
    },
}

PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": False, "timeout": 1000_1000}
ITEM_DICT = {
    "中文名": "chineseName",
    "英文名": "englishName",
    "主办单位": "hostUnit",
    "出版周期": "journalType",
    "ISSN": "issn",
    "CN": "cn",
    "出版地": "publicationPlace",
    "语种": "languageName",
    "开本": "size",
    "创刊时间": "launchYear",
    "专辑名称": "album",
    "专题名称": "topic",
    "出版文献量": "publicCount",
    "总下载次数": "downloadsAmount",
    "总被引次数": "totalCites",
    "是否收费": "hasFee",
    "复合影响因子": "impactFactors",
    "综合影响因子": "comprehensiveImpactFactors",
    "平均审稿周期": "reviewCycle",
    "主编": "editorInChief",
    "副主编": "deputyEditor",
    "E-mail": "submissionEmail",
    "电话": "phone",
    "主管单位": "sponsor",
    "网址": "website",
    "平均出版时滞": "timeLag",
    "数据库": "database",
    "认证": "journalType2",
}

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3  # Number of times to retry a failed request
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]  # HTTP codes that trigger a retry
PLAYWRIGHT_MAX_CONTEXTS = 2
SF = "31"
SAVE_FILE_NAME = "cnki.xlsx"
END_PAGE = 0  # 限制页数, 单个查询最多页数


# 添加 InterceptHandler() 类
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # ✓ corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# 使用 InterceptHandler() 类
# logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 添加
# logger.add("logs/cnki_{time}.log", level="ERROR", rotation="10 MB")
