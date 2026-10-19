import os 
import pandas 

from get_soup import get_soup
from get_player_country import get_player_country
from RateLimitError import RateLimitError

def read_countries_csv(path):
    return pandas.read_csv(path, keep_default_na=False, na_values=[""])

def get_all_countries(player_df, cache_path):
    
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    
    if not os.path.exists(cache_path):
        pandas.DataFrame(columns=["player_id", "player","country_code"]).to_csv(cache_path, index=False)
    
    done_df = read_countries_csv(cache_path)
    "We keep track of the players ID we already search, this is more for the user to be calm with a long running code. (See notes)"
    done_ids = set(done_df["player_id"])
    pending_df = player_df[~player_df["player_id"].isin(done_ids)]
    total = len(pending_df)
    print(f"Processing {len(pending_df)} players...")
    
    "This is the core of the function we use this part to actually search for every player that hasn't been in the cache"
    for i,(_, row) in enumerate(pending_df.iterrows(), start=1):
        try:
            country_code = get_player_country(row["player_id"])
        except RateLimitError as e:
            print (e)
            print(f"Rate limited while retrieving country for {row['player_id']}: {e}")
            break
        except Exception as e:
            print(f"Error retrieving country for {row['player_id']}: {e}")
            continue
        
        pandas.DataFrame([{"player_id": row["player_id"], 
                           "player": row["player"], 
                           "country_code": country_code}]).to_csv(cache_path, mode='a', header=False, index=False)
        
        if i % 100 == 0: 
            print(f"{i}/{total}")
    return read_countries_csv(cache_path)