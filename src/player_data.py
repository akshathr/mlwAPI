from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import tabulate 

from constants import PFR_DRAFT_URL, PFR_LAST_NAME_PAGE_URL
from utils import *

def get_draft_class(
        year, csv=False):
    
    response = get_response(PFR_DRAFT_URL.format(year))
    soup = BeautifulSoup(response.content, 'html.parser') 

    table = soup.find('table')
    df = pd.read_html(str(table))[0] 

    # clean the column names of the 'Unnamed' prefix and flatten
    draft_class = clean_column_names(df)
    
    # return as a csv file or markdown table
    if csv: 
        return draft_class.to_csv()
    else: 
        return draft_class.to_markdown()
    
def get_player_nfl_stats(
        name, stat_type=None, year=None, position=None):

    if name:
        if " " in name:
            # gather the last initial for the player
            last_initial = get_last_initial(name)
            response = get_response(PFR_LAST_NAME_PAGE_URL.format(last_initial))

            # get the path for the player's stat page
            player_path = get_player_path(response, name, position)

            # get response with player stat page
            player_page_response = get_response(PFR_BASE_URL.format(player_path))

            # TODO - add that one deprecated url edge case for the column cleaning logic 
            soup = BeautifulSoup(response.content, 'html.parser') 

            table = soup.find('table')
            df = pd.read_html(str(table))[0] 

            if stat_type:
                if stat_type in df.columns:
                    
                    if year:
                        final_df = df.loc[df['year'] == year, ['year', stat_type]]
                    else:
                        final_df = df.loc[:, ['year', stat_type]]

        else:
            print(f"Please add space to player name")
    else:
        print(f"Oops, player not found. Please confirm spelling/format")



def get_player_college_stats():
    
def get_player_combine_measurables():
    