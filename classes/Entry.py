from pydantic import BaseModel, constr
import re
from classes.DBManager import db_manager


class Entry(BaseModel):
    ranking: int
    album: str
    artist: str
    album_units: int
    album_sales: int
    song_sales: int
    song_streams: int
    peak_position: int
    weeks_in_chart: int
    label: str
    date: constr(regex=r"\d{4}-\d{2}-\d{2}")


@classmethod
def from_dict(cls, data: dict):
    return cls(**data)


def save_to_db(self):
    fields = [
        "ranking",
        "album",
        "artist",
        "album_units",
        "album_sales",
        "song_sales",
        "song_streams",
        "peak_position",
        "weeks_in_chart",
        "label",
        "date",
    ]
    values = [
        self.ranking,
        self.album,
        self.artist,
        self.album_units,
        self.album_sales,
        self.song_sales,
        self.song_streams,
        self.peak_position,
        self.weeks_in_chart,
        self.label,
        self.date,
    ]
    db_manager.insert_entry("entries", values, fields)
