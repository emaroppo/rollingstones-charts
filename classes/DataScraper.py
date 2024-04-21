import requests
from bs4 import BeautifulSoup
import datetime
import json


class DataScraper:
    def __init__(self):
        self.endpoint_top = "https://www.rollingstone.com/charts/albums/{}-{}-{}/"
        self.endpoint_data = "https://www.rollingstone.com/wp-admin/admin-ajax.php?counter=15&chart=albums&results_per=185&chart_date={}%20{}%2C%20{}&is_eoy=0&eoy_year=0&action=rscharts_fetch_subchart"
        self.top_class = (
            "l-section__charts c-chart__table--single c-chart__table--first"
        )
        self.album_class = "l-section__charts c-chart__table--single"
        self.ranking_class = "c-chart__table--rank"
        self.album_class = "c-chart__table--title"
        self.artist_class = "c-chart__table--caption"
        self.album_units_class = "c-chart__table--stat-base c-chart__table--album-units"
        self.album_sales_class = "c-chart__table--stat-base c-chart__table--album-sales"
        self.song_sales_class = "c-chart__table--stat-base c-chart__table--song-sales"
        self.song_streams_class = (
            "c-chart__table--stat-base c-chart__table--song-streams"
        )
        self.peak_position_class = "c-chart__table--stat-base c-chart__table--peak"
        self.weeks_in_chart_class = (
            "c-chart__table--stat-base c-chart__table--weeks-present"
        )
        self.label_class = "c-chart__table--label"

    def get_monday(self, year, month, day):
        date_ = datetime.date(year, month, day)
        monday = date_ + datetime.timedelta(days=-date_.weekday())
        return monday

    def clean_performance(self, string):
        if "K" in string:
            return int(float(string[:-1]) * 1000)
        elif "M" in string:
            return int(float(string[:-1]) * 1000000)
        else:
            return int(float(string))

    def stringify_date(self, year, month, day):
        year_str = str(year)

        if month < 10:
            month_str = "0" + str(month)
        if day < 10:
            day_str = "0" + str(day)

        return year_str, month_str, day_str

    def parse_weekly_chart(self, chart, year, month, day):

        year, month, day = self.stringify_date(year, month, day)

        entries = list()

        for album in chart:
            soup = BeautifulSoup(album, "html.parser")
            entry = {
                "ranking": int(soup.find(class_=self.ranking_class).getText()),
                "album": soup.find(class_=self.album_class).find("p").getText(),
                "artist": soup.find(class_=self.artist_class).getText(),
                "album_units": self.clean_performance(
                    soup.find(class_=self.album_units_class).find("span").getText()
                ),
                "album_sales": self.clean_performance(
                    soup.find(class_=self.album_sales_class).find("span").getText()
                ),
                "song_sales": self.clean_performance(
                    soup.find(class_=self.song_sales_class).find("span").getText()
                ),
                "song_streams": self.clean_performance(
                    soup.find(class_=self.song_streams_class).find("span").getText()
                ),
                "peak_position": int(
                    soup.find(class_=self.peak_position_class).find("span").getText()
                ),
                "weeks_in_chart": int(
                    soup.find(class_=self.weeks_in_chart_class).find("span").getText()
                ),
                "label": soup.find(class_=self.label_class).find("span").getText(),
                "date": f"{year}-{month}-{day}",
            }
            entries.append(entry)
        return entries

    def scrape_weekly_chart(self, year, month, day):

        year_str, month_str, day_str = self.stringify_date(year, month, day)

        url = self.endpoint_top.format(year_str, month_str, day_str)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        top = soup.find(class_=self.top_class)
        chart = soup.find_all("section", class_=self.album_class)
        chart.append(top)
        monday = self.get_monday(year, month, day)

        url = self.endpoint_data.format(
            monday.strftime("%B")[:3], str(monday.day), str(monday.year)
        )
        further_req = requests.get(url)
        data = json.loads(further_req.content)
        data = data["data"]
        soup = BeautifulSoup(data, "html.parser")
        further_chart = soup.find_all("section", class_=self.album_class)

        chart.extend(further_chart)
        return self.parse_weekly_chart(chart, monday.year, monday.month, monday.day)
