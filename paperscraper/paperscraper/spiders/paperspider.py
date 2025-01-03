import scrapy
from paperscraper.items import PaperscraperItem

SUBJECTS_MAP = {
    "cs": "computer science",
    "eess": "electrical engineering and systems science",
    "econ": "economics",
    "q-bio": "quantitative biology",
    "q-fin": "quantitative finance",
    "stat": "statistics",
    "math": "mathematics",
}

SUBJ_URL_CLASSES = [
    "computer_science",
    "eess",
    "economics",
    "mathematics",
    "q_biology",
    "q_finance",
    "statistics",
]


class PaperSpider(scrapy.Spider):
    name = "paperspider"
    allowed_domains = ["arxiv.org"]
    start_urls = [
        f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-{subj}=y&classification-physics_archives=all&classification-include_cross_list=exclude&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&abstracts=show&size=200&order=-announced_date_first"
        for subj in SUBJ_URL_CLASSES
    ]

    def __init__(self):
        self.start_urls.append(
            "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-physics=y&classification-physics_archives=all&classification-include_cross_list=exclude&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&abstracts=show&size=200&order=-announced_date_first"
        )

    def get_domain_from_tag(self, tag):
        domainTag = tag.split(".")[0]
        if domainTag in SUBJECTS_MAP:
            return SUBJECTS_MAP[domainTag]
        return "physics"

    def extract_info(self, paper):
        item = PaperscraperItem()

        p_selector = paper.css("p.is-size-7")

        item["title"] = paper.css("p.title::text").get()
        item["abstract"] = paper.css("span.abstract-full").xpath("text()").get()
        item["main_subject"] = paper.css("span.tag.is-link::attr(data-tooltip)").get()
        item["domain"] = self.get_domain_from_tag(
            paper.css("span.tag.is-link::text").get()
        )
        item["subjects"] = paper.css("span.tag.is-grey::attr(data-tooltip)").getall()
        item["submitted_date"] = p_selector.xpath(
            ".//text()[preceding-sibling::span[contains(text(),'Submitted')]]"
        ).get()
        item["announced_date"] = p_selector.xpath(
            ".//text()[preceding-sibling::span[contains(text(),'originally announced')]]"
        ).get()

        return item

    def parse(self, response):
        papers = response.css("li.arxiv-result")

        for paper in papers:
            yield self.extract_info(paper)

        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
