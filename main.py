from classes.DataScraper import DataScraper
from classes.Entry import Entry


def main(year, month, day):
    scraper = DataScraper()
    entries = scraper.scrape_weekly_chart(year, month, day)
    entries = [Entry.from_dict(entry) for entry in entries]

    for entry in entries:
        entry.save_to_db()
