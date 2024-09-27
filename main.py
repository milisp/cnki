import argparse
import subprocess


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


def run_spider(sf, headless, logfile):
    # 构建命令
    command = [
        "scrapy",
        "crawl",
        "ko",
        "-a",
        f"sf={sf}",
        "-s",
        f"headless={headless}",
    ]
    if logfile:
        command += ["--logfile", f"{logfile}"]
    print(command)

    # 运行命令
    subprocess.run(command)


if __name__ == "__main__":
    # 获取命令行参数
    args = parse_args()

    headless = "True" if args.headless else ""
    run_spider(args.sf, args.headless, args.logfile)
