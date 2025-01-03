import re
from itemadapter import ItemAdapter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class PaperscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        only_alpha = re.compile(r"[^a-zA-Z\s]")

        # Strip all fields that are strings
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()

        # Remove redundant characters and spaces from the abstract
        abstract = only_alpha.sub("", adapter.get("abstract"))
        adapter["abstract"] = re.sub(r"\s+", " ", abstract)
        title = only_alpha.sub("", adapter.get("title"))
        adapter["title"] = re.sub(r"\s+", " ", title)

        # Convert all subjects to lowercase
        subjects = adapter.get("subjects")
        adapter["subjects"] = [subject.lower() for subject in subjects]
        main_subject = adapter.get("main_subject")
        adapter["main_subject"] = main_subject.lower()

        # Remove "." and ";" from the submitted_date and announced_date
        submitted_date = adapter.get("submitted_date")
        adapter["submitted_date"] = re.sub(r"[;]", "", submitted_date)
        announced_date = adapter.get("announced_date")
        adapter["announced_date"] = re.sub(r"[.]", "", announced_date)

        return item
