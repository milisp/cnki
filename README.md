# cnki

## 并行极速版本
> 使用 playwright 获取知网信息

## 安装

```sh
pip install -r requirements.txt
playwright install chromium

# 或者
# sh install.sh
```

## 运行

```sh
# 两位编码用英文逗号隔开，单个直接写
python main.py --sf 31,11
python main.py --sf 31
python main.py --sf 31 --logfile cnki.log  # 日志
python main.py --sf 31 --headless  # 无头

# 用 scrapy 的命令行
scrapy crawl ko --logfile ko.log -s SF="31,11"
```

## 模块说明

```md
main.py  # 主要是命令行
cnki/spiders/ko.py  # 主要爬虫代码
cnki/items.py   # 定义保存的列
cnki/pipeline.py  # save excel
cnki/settings.py  # 配置
```
