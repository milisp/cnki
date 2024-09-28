import scrapy
from scrapy_playwright.page import PageMethod

from cnki.items import CnkiItem
from cnki.utils import jump_to_start_page, load_progress, update_progress


class KoSpider(scrapy.Spider):
    name = "ko"
    allowed_domains = ["cnki.net"]
    headers = None

    def start_requests(self):
        print("start")
        user_agent = self.settings.get("USER_AGENT")
        self.headers = {"user-agent": user_agent}
        for q in self.settings.get("SF").split(","):
            yield scrapy.Request(
                url="https://navi.cnki.net/knavi/",  # 列表页的 URL
                callback=self.parse,
                dont_filter=True,
                meta={
                    "q": q,
                    "playwright": True,  # 使用 Playwright 加载页面
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("select_option", "#txt_1_sel", "CN|=?"),
                        PageMethod("fill", "#txt_1_value1", f"{q}-"),
                        PageMethod("click", "#btnSearch"),
                        PageMethod("wait_for_selector", "#lblPageCount"),
                    ],
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        q = response.meta["q"]
        total_page = response.css("#lblPageCount::text").get()
        total = int(total_page)
        print("total page", total_page)

        start_page = load_progress().get(q, 1)
        end_page = self.settings.get("END_PAGE")
        end_page = int(end_page)
        if end_page < start_page and end_page == 0:
            # 跳到上次页面或者第一页
            if total != start_page:
                await jump_to_start_page(page, start_page)
        else:
            start_page, total = 1, end_page
        for page_num in range(start_page, total + 1):
            # 更新最后页数
            update_progress(q, page_num)
            self.logger.info(f"page {page_num}")
            results = await page.query_selector_all("dl.result")
            for i, result in enumerate(results):
                self.logger.info(f"results item {i}")
                if await result.query_selector('b:has-text("Journal")'):
                    a = await result.query_selector("h1 a")
                    link = await a.get_attribute("href")
                    yield scrapy.Request(
                        url=response.urljoin(link),
                        callback=self.parse_detail,
                    )
            next_button = await page.wait_for_selector("a.next", timeout=10000)
            if page_num != total:
                print(f"to click next page {page_num+1}/{total}")
                self.logger.info(f"click next page {page_num+1} / {total}")
                await next_button.click()

    # 解析详情页内容
    def parse_detail(self, response):
        print("detail", response.url)
        item = CnkiItem()
        english_name = response.css("h3.titbox::text").get().strip()
        chinese_name = response.css("h3.titbox+p::text").get()
        item_dict = self.settings.get("ITEM_DICT")
        for p in response.css("p.hostUnit"):
            label = p.css("label::text").get()
            span = p.css("span::text").get()
            if label and span:
                try:
                    item[item_dict[label]] = span.strip()
                except Exception:
                    pass
        item["englishName"] = english_name
        item["chineseName"] = chinese_name
        item["database"] = ";".join(
            [text.strip() for text in response.css("p.database::text").getall()]
        )
        item["journalType2"] = ";".join(
            response.css(".journalType2>span::text").getall()
        )
        baseId = response.url.split("/")[5]
        item["baseId"] = baseId
        url = f"https://xztg.cnki.net/csjs-sj/JournalBaseInfo/getInfo?baseId={baseId}"
        yield item
        yield scrapy.Request(
            url,
            callback=self.parse_tg,
            meta={"item": item, "baseId": baseId},
        )

    def parse_tg(self, response):
        # 投稿
        item = response.meta["item"]
        baseId = response.meta["baseId"]
        print(baseId, "tg")
        resp_data = response.json()
        data = resp_data["data"]
        keys = [
            "englishName",
            "chineseName",
            "hasFee",
            "reviewCycle",
            "timeLag",
            "comprehensiveImpactFactors",
            "impactFactors",
        ]
        for key in keys:
            item[key] = data[key]
        url = f"https://xztg.cnki.net/csjs-sj/JournalBaseInfo/getSubmissionInfo?baseId={baseId}"
        # print("parse tg ok")
        yield scrapy.Request(
            url,
            callback=self.parse_sub_mission_info,
            meta={"item": item},
            # headers=self.headers,
        )

    def parse_sub_mission_info(self, response):
        # 投稿补充
        item = response.meta["item"]
        resp_data = response.json()
        keys = [
            "website",
            "phone",
            "sponsor",
            "submissionEmail",
            "deputyEditor",
            "editorInChief",
            "hostUnit",
        ]
        # print("parse sub code")
        if resp_data["code"] == 20000:
            data = resp_data["data"]
            for key in keys:
                item[key] = data[key]
        else:
            for key in keys:
                item[key] = ""
        yield item
