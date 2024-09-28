import argparse
import time

from scrapy.crawler import CrawlerProcess

# from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from twisted.internet.error import ReactorNotRestartable


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


def run_spider(spider, settings, args):
    settings["SF"] = args.sf
    settings["PLAYWRIGHT_LAUNCH_OPTIONS"] = {
        "headless": args.headless,
        "timeout": 1000_000,
    }
    settings["LOG_FILE"] = args.logfile
    process = CrawlerProcess(settings)
    process.crawl(spider)
    process.start()


if __name__ == "__main__":
    spider_name = "ko"  # 替换为您自己的爬虫名称

    args = parse_args()

    retry_count = 0
    max_retries = 5
    delay_between_retries = 10  # 每次重试之间的延迟时间，单位为秒
    settings = get_project_settings()

    while retry_count < max_retries:
        try:
            print(f"启动爬虫 (第 {retry_count + 1} 次)...")
            run_spider(spider_name, settings, args)
            print("爬虫运行完成。")
            break  # 如果爬虫成功运行，退出循环
        except ReactorNotRestartable:
            print("Scrapy 爬虫无法重新启动，因为 reactor 不支持重新启动。")
            break
        except Exception as e:
            retry_count += 1
            print(f"爬虫运行出错: {e}")
            print(
                f"将在 {delay_between_retries} 秒后重试 ({retry_count}/{max_retries}).."
            )
            time.sleep(delay_between_retries)

    if retry_count == max_retries:
        print("达到最大重试次数，爬虫终止。")

    print("run finished")
