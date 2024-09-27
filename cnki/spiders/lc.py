import scrapy


class LcSpider(scrapy.Spider):
    name = "lc"

    def start_requests(self):
        yield scrapy.Request(
            url="http://localhost:8000",
            meta={"playwright": True, "playwright_include_page": True},
            callback=self.parse,
        )

    async def parse(self, response):
        detail_links = response.css("a::attr(href)").getall()
        for link in detail_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_detail,
                meta={"playwright": True},  # 每个详情页使用 Playwright 处理
            )

    async def parse_detail(self, response):
        title = response.css("h1::text").get()  # 获取详情页的标题
        content = response.css(".content::text").get()  # 获取页面内容
        yield {"title": title, "content": content}
