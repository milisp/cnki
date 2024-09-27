import scrapy
from scrapy_playwright.page import PageMethod

from cnki.items import DetailItem, XztgItem
from cnki.utils import jump_to_start_page, load_progress, update_progress


class CnkiSpider(scrapy.Spider):
    name = "cnki"
    allowed_domains = ["cnki.net"]
    q = "31"
    headers = None

    def start_requests(self):
        user_agent = self.settings.get("USER_AGENT")
        self.headers = {"user-agent": user_agent}
        yield scrapy.Request(
            url="https://navi.cnki.net/knavi/",  # 列表页的 URL
            callback=self.parse,
            dont_filter=True,
            meta={
                "playwright": True,  # 使用 Playwright 加载页面
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("select_option", "#txt_1_sel", "CN|=?"),
                    PageMethod("fill", "#txt_1_value1", f"{self.q}-"),
                    PageMethod("click", "#btnSearch"),
                    PageMethod("wait_for_selector", "#lblPageCount"),
                ],
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        total_page = response.css("#lblPageCount::text").get()
        print(total_page)

        start_page = load_progress().get(self.q, 1)
        # 跳到上次页面或者第一页
        # await jump_to_start_page(page, start_page)
        # total = int(total_page)
        total = 5
        for page_num in range(start_page, total + 1):
            # 更新最后页数
            update_progress(self.q, page_num)
            results = await page.query_selector_all("dl.result")
            for i, result in enumerate(results):
                self.logger.info(f"result {i}")
                if await result.query_selector('b:has-text("Journal")'):
                    issn_span = await result.query_selector('li span:has-text("ISSN")')
                    issn_text = await issn_span.inner_text()
                    issn = issn_text.split("：")[-1].strip()
                    a = await result.query_selector("h1 a")
                    link = await a.get_attribute("href")
                    # print(issn, a, link)
                    yield scrapy.Request(
                        url=response.urljoin(link),
                        callback=self.parse_detail,
                    )

            next_button = await page.query_selector("a.next")
            if next_button:
                self.logger.info("click next page")
                await next_button.click()

    # 解析详情页内容
    def parse_detail(self, response):
        item = DetailItem()
        english_name = response.css("h3.titbox::text").get()  # 获取详情页的标题
        chinese_name = response.css("h3.titbox+p::text").get()  # 获取详情页的标题
        self.logger.info(english_name)
        for p in response.css("p.hostUnit"):
            label = p.css("label::text").get()
            span = p.css("span::text").get()
            if label and span and label in self.settings.get("DEITEM_KEYS"):
                if "影响因子" not in label:
                    item[label] = span.strip()
                elif "复合影响因子" in label:
                    item["复合影响因子"] = span.strip()
                elif "综合影响因子" in label:
                    item["综合影响因子"] = span.strip()
        item["english_name"] = english_name
        item["chinese_name"] = chinese_name
        item["database"] = "|".join(response.css("p.database::text").getall())
        item["journalType2"] = "|".join(
            response.css(".journalType2>span::text").getall()
        )
        baseId = response.url.split("/")[5]
        url = f"https://xztg.cnki.net/csjs-sj/JournalBaseInfo/getInfo?baseId={baseId}"
        yield item
        yield scrapy.Request(
            url, callback=self.parse_tg, meta={"baseId": baseId}, headers=self.headers
        )

    def parse_tg(self, response):
        item = XztgItem()
        resp_data = response.json()
        print(resp_data)
        data = resp_data["data"]
        item["hasFee"] = data["hasFee"]
        item["reviewCycle"] = data["reviewCycle"]
        item["timeLag"] = data["timeLag"]
        baseId = response.meta["baseId"]
        url = f"https://xztg.cnki.net/csjs-sj/JournalBaseInfo/getSubmissionInfo?baseId={baseId}"
        yield scrapy.Request(
            url,
            callback=self.parse_sub_mission_info,
            meta={"baseId": baseId, "item": item},
            headers=self.headers,
        )

    def parse_sub_mission_info(self, response):
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
        if resp_data["code"] == 20000:
            data = resp_data["data"]
            for key in keys:
                item[key] = data[key]
        else:
            for key in keys:
                item[key] = ""
        yield item
