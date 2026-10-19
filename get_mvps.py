import os
import pandas
from get_soup import get_soup
from constants import MVP_URL

def get_mvps(cache_path):
    if os.path.exists(cache_path):
        return pandas.read_csv(cache_path)
    
    soup = get_soup(MVP_URL)
    table = soup.find("table", {"id": "mvp_NBA"})
    
    if table is None:
        raise ValueError(f"No table found on {MVP_URL}")
    
    records = []
    
    for row in table.find("tbody").find_all("tr"):
        season_cell = row.find("th", {"data-stat": "season"})
        player_link = row.find("a", href=lambda h: h and h.startswith("/players/"))
        if season_cell is None or player_link is None:
            continue
        
        season = int(season_cell.get_text(strip=True)[:4]) + 1
        player_id = player_link["href"].split("/")[-1].replace(".html", "")
        
        records.append({"season": season, "player_id": player_id, "mvp_player": player_link.text.strip()})
    
    df = pandas.DataFrame(records)
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    df.to_csv(cache_path, index=False)
    return df
