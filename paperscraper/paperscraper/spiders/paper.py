import scrapy


class PaperSpider(scrapy.Spider):
    name = "paperspider"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org/search/advanced"]

    def parse(self, response):
        pass
