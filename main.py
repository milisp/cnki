import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from cnki.spiders.ko import KoSpider


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--logfile", help="logfile")
    parser.add_argument(
        "--sf",
        required=True,
        help="两位编码如: 31 多个编码用逗号隔开如: 11,31",
    )
    args = parser.parse_args()
    return args


settings = get_project_settings()

if __name__ == "__main__":
    args = parse_args()
    settings["SF"] = args.sf
    settings["PLAYWRIGHT_LAUNCH_OPTIONS"] = {"headless": args.headless}
    settings["LOG_FILE"] = args.logfile

    process = CrawlerProcess(settings)
    process.crawl(KoSpider)
    process.start()
