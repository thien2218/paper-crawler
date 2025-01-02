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
    "physics": "physics",
    "astro-ph": "astrophysics",
    "cond-mat": "condensed matter",
    "nlin": "nonlinear sciences",
}


class PaperSpider(scrapy.Spider):
    name = "paperspider"
    allowed_domains = ["arxiv.org"]
    start_urls = [
        "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&abstracts=show&size=200&order=-announced_date_first"
    ]

    def get_domain_from_tag(self, tag):
        domainTag = tag.split(".")[0]
        if domainTag in SUBJECTS_MAP:
            return SUBJECTS_MAP[domainTag]
        return "physics"

    def extract_info(self, paper):
        item = PaperscraperItem()

        title = paper.css("p.title::text").get()
        abstract_el = paper.css("span.abstract-full")
        abstract = abstract_el.xpath("text()").get()

        domain = self.get_domain_from_tag(paper.css("span.tag.is-link::text").get())
        main_subject = paper.css("span.tag.is-link::attr(data-tooltip)").get()
        subjects = paper.css("span.tag.is-grey::attr(data-tooltip)").getall()

        p_selector = paper.css("p.is-size-7")
        submitted_date = p_selector.xpath(
            ".//text()[preceding-sibling::span[contains(text(),'Submitted')]]"
        ).get()
        announced_date = p_selector.xpath(
            ".//text()[preceding-sibling::span[contains(text(),'originally announced')]]"
        ).get()

        item["title"] = title
        item["abstract"] = abstract
        item["main_subject"] = main_subject
        item["domain"] = domain
        item["subjects"] = subjects
        item["submitted_date"] = submitted_date
        item["announced_date"] = announced_date

        return item

    def parse(self, response):
        papers = [
            element
            for i, element in enumerate(response.css("li.arxiv-result"))
            if i % 10 == 0
        ]

        for paper in papers:
            yield self.extract_info(paper)

        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
