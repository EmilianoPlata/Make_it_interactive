import os
import pandas as pd

from get_soup import get_soup

def league_prefix(year):
    return "BAA" if year <= 1949 else "NBA"

def get_all_players(year, cach_folder="data/players"):
    
    """
    This is almost the same function as other I've made. Which downloadall the data tha we need for this visualization
    """
    
    os.makedirs(cach_folder, exist_ok=True)
    cache_path = os.path.join(cach_folder, f"all_players_{year}.csv")
    
    if os.path.exists(cache_path):
        return pd.read_csv(cache_path)
    
    "This is the URL I could found that has almost all players in the NBA, in this case they will at least have one minute played"
    url = f"https://www.basketball-reference.com/leagues/{league_prefix(year)}_{year}_totals.html"
    
    "The same case as the previouse module, we need this library to search for the name in the table"
    soup = get_soup(url)
    
    table = soup.find("table", {"id": "totals_stats"})
    
    if table is None:
        raise ValueError(f"Table not found for year: {year}")
    
    rows = table.find("tbody").find_all("tr")
    records = []
    for row in rows:
        "Here is where we can find the name of the player, with the url to the profile of the player"
        player_cells = row.find_all("td", {"data-stat": "name_display"})
        
        if not player_cells:
            continue
        "To finde the player ID we will found it in a link after an <a> tag"
        player_link = player_cells[0].find("a")
        
        if player_link is None or "href" not in player_link.attrs:
            continue
        
        "We clean a bit of the way the player ID is written in the url"
        player_id = player_link["href"].split("/")[-1].replace(".html", "")
        player_name = player_link.text.strip()
        
        records.append({"player_id": player_id, "player": player_name})
    
    "If any player played for more than one team in the season the player will appear two times, making this line quite important"
    df = pd.DataFrame(records).drop_duplicates(subset="player_id", keep="first")
    
    df["season"] = year
    df = df.sort_values(by="player").reset_index(drop=True)
    df.to_csv(cache_path, index=False)
    return df