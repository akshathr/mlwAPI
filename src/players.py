from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import datetime

def get_hitting_stats(
    _name, year=datetime.date.today().year, playoffs=False,
    stat_type=None):
    