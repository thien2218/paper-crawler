import scrapy
from urllib.parse import urlencode


class PaperSpider(scrapy.Spider):
    name = "paperspider"
    allowed_domains = ["arxiv.org"]
    start_urls = [
        "https://arxiv.org/search/advanced?advanced=1&terms-0-term=&terms-0-operator=AND&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=announced_date_first"
    ]

    def parse(self, response):
        MAX_SIZE = 250000

        subjects_map = {
            "cs": "computer science",
            "eess": "electrical engineering and systems science",
            "econ": "economics",
            "q-bio": "quantitative biology",
            "q-fin": "quantitative finance",
            "stat": "statistics",
            "math": "mathematics",
            "physics": "physics",
        }

        physics_subclasses = {
            "astro-ph": "astrophysics",
            "cond-mat": "condensed matter",
            "gr-qc": "general relativity and quantum cosmology",
            "hep-ex": "high energy physics - experiment",
            "hep-lat": "high energy physics - lattice",
            "hep-ph": "high energy physics - phenomenology",
            "hep-th": "high energy physics - theory",
            "math-ph": "mathematical physics",
            "nlin": "nonlinear sciences",
            "nucl-ex": "nuclear experiment",
            "nucl-th": "nuclear theory",
            "quant-ph": "quantum physics",
        }

        pass
