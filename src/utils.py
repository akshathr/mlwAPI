import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from constants import HEADERS, PFR_BASE_URL, PFR_DRAFT_URL, PFR_LAST_NAME_PAGE_URL

def get_response(
        url):

    session = requests.Session()
    try:
        return session.get(url, headers=HEADERS)
    except:
        print(f"Invalid access: ", session.get(url, headers=HEADERS).raise_for_status())


def clean_column_names(
        df):
    
    # flatten the Dataframe object
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    df.columns = df.columns.str.strip()

    # strip the 'Unnamed' prefix from each of the column names
    df.columns = df.columns.str.replace('Unnamed: \d+_level_\d+', '')

    return df

def get_last_initial(
        name):
    
    # each first_name last_name should be split by a space
    split_char = ' '

    # gather the first letter of the players last name
    last_initial = name.split(split_char, 1)[1]

    return last_initial

def get_player_path(
        response, name, position=None):

    # create a bs4 object to parse the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # get the HTML element for the player - if user provides a position, use both player and position in lookup
    if position:
        player = {'data-stat': 'player', 'csk': f'{name}, {position}'}
    else:
        player = {'data-stat': 'player', 'text': name}
    
    player_element = soup.find('td', player)

    # extract the path for the given player (and position i/a)
    if player_element:
        # Extract player name and player page path
        player_name_element = player_element.find('a')
        player_page_path = player_name_element['href']

        return player_page_path
    else: 
        return None 



