import scrapy
import re

# import pandas as pd

MAX_SIZE = 20

SUBJECTS_MAP = {
    "cs": "computer science",
    "eess": "electrical engineering and systems science",
    "econ": "economics",
    "q-bio": "quantitative biology",
    "q-fin": "quantitative finance",
    "stat": "statistics",
    "math": "mathematics",
    "physics": "physics",
}


class PaperSpider(scrapy.Spider):
    name = "paperspider"
    allowed_domains = ["arxiv.org"]
    start_urls = [
        "https://arxiv.org/search/advanced?advanced=1&terms-0-term=&terms-0-operator=AND&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=announced_date_first"
    ]

    current = 0
    output_file = "../../papers.csv"

    def text_cleaner(self, text):
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text

    def get_domain_from_tag(self, tag):
        splitted = tag.split(".")
        if len(splitted) == 2:
            return SUBJECTS_MAP[splitted[0]]
        return "physics"

    def extract_info(self, paper):
        title = paper.css("p.title::text").get().strip()
        abstract = paper.css("span.abstract-full::text").get().strip()
        abstract = self.text_cleaner(abstract)

        domain = self.get_domain_from_tag(paper.css("span.tag.is-link::text").get())
        main_subject = paper.css("span.tag.is-link::attr(data-tooltip)").get().lower()
        subjects = paper.css("span.tag.is-grey::attr(data-tooltip)").getall()
        subjects = [s.lower() for s in subjects]

        p_selector = paper.css("p.is-size-7")
        submitted_date = re.sub(
            r"[.;]",
            "",
            p_selector.xpath(
                ".//text()[preceding-sibling::span[contains(text(),'Submitted')]]"
            ).get(),
        ).strip()
        announced_date = re.sub(
            r"[.;]",
            "",
            p_selector.xpath(
                ".//text()[preceding-sibling::span[contains(text(),'originally announced')]]"
            ).get(),
        ).strip()

        return {
            "title": title,
            "abstract": abstract,
            "main_subject": main_subject,
            "domain": domain,
            "subjects": subjects,
            "submitted_date": submitted_date,
            "announced_date": announced_date,
        }

    def parse(self, response):
        papers = [
            element
            for i, element in enumerate(response.css("li.arxiv-result"))
            if i % 10 == 0
        ]

        self.current += len(papers)

        if self.current > MAX_SIZE:
            return

        for paper in papers:
            yield self.extract_info(paper)

        next_page = response.css("a.pagination-next::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

        pass
