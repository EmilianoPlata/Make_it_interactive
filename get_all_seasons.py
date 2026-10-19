import os 
import pandas
from get_all_players import get_all_players

def get_all_seasons(first, last, cache_path):
    
    if os.path.exists(cache_path):
        return pandas.read_csv(cache_path)
    
    frames = []
    for year in range(first, last + 1):
        season_df = get_all_players(year)
        frames.append(season_df[["player_id", "player", "season"]])
        
    all_df = pandas.concat(frames, ignore_index=True)
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    all_df.to_csv(cache_path, index=False)
    return all_df
