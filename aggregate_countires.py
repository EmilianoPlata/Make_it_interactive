import numpy as np

from build_mvp_table import build_mvp_table

def aggregate_countries(season_players_df, player_country_df, country_info_df, mvp_table):
    
    """
    Here we track the players that dosn't have a country. We group the players with the same code into and making in a descending way
    """
    
    merged = season_players_df.merge(player_country_df[["player_id", "country_code"]], on="player_id", how="left")
    
    missing_share = merged.groupby("season")["country_code"].apply(lambda x: x.isna().mean())
    high = missing_share[missing_share > 0.1]
    
    if not high.empty:
        print("Warning: Some seasons have more than 10% of players with missing country information:")
        print(high)
    
    merged = merged.dropna(subset=["country_code"])
    
    counts = (
        merged.groupby(["season", "country_code"]).size().reset_index(name="player_count").merge(country_info_df, left_on="country_code", right_on="iso2", how="left")
    )
    
    unmatched = counts.loc[counts["iso3"].isna(), "country_code"].unique()
    if len(unmatched):
        print(f"Warning: The following country codes could not be matched to country information: {unmatched}")
    counts = counts.dropna(subset=["iso3"])
    
    counts = counts.merge(mvp_table[["season", "iso3", "mvp_player"]], on=["season", "iso3"], how="left")
    
    counts["mvp_line"] = np.where(counts["mvp_player"].notna(), "<br>⭐ MVP: " + counts["mvp_player"].fillna(""),"")
    
    return counts