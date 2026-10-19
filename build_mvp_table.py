import numpy as np 

def build_mvp_table(mvp_df, player_country_df, country_info_df):
    
    mvp = mvp_df.merge(player_country_df[["player_id", "country_code"]], on="player_id", how="left")
    
    mvp = mvp.merge(country_info_df, left_on="country_code", right_on="iso2", how="left")
    
    missing = mvp[mvp["iso3"].isna()]
    
    if not missing.empty:
        print(f"Warning: {len(missing)} MVPs have missing country information.")
        print(missing[["season", "mvp_player", "country_code"]])
    
    return mvp[["season", "mvp_player", "country_name", "iso3", "longitude", "latitude"]]
