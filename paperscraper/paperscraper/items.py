# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PaperscraperItem(Item):
    title = Field()
    abstract = Field()
    main_subject = Field()
    domain = Field()
    subjects = Field()
    submitted_date = Field()
    announced_date = Field()
