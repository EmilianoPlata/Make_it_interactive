import os

from constants import (
    FIRST_SEASON, LAST_SEASON,
    SEASON_PLAYERS_CSV, PLAYER_COUNTRIES_CSV, COUNTRY_COUNTS_CSV,
    MVP_CSV, MVP_POSITION_CSV, COUNTRY_INFO_CSV,
    OUTPUT_PATH, OUTPUT_FILE,
)
from get_all_seasons import get_all_seasons
from get_all_player_countries import get_all_countries
from get_mvps import get_mvps
from get_geojson import get_geojson
from country_info import build_country_info
from aggregate_countires import aggregate_countries
from interactive_map import build_figure
from build_mvp_table import build_mvp_table

if __name__ == "__main__":
    season_players = get_all_seasons(FIRST_SEASON, LAST_SEASON, SEASON_PLAYERS_CSV)
    unique_players = season_players.drop_duplicates("player_id")[["player_id", "player"]]
    print(f"{len(unique_players)} unique players from {FIRST_SEASON} to {LAST_SEASON}")
    
    player_countries = get_all_countries(unique_players, PLAYER_COUNTRIES_CSV)
    
    pending = set(unique_players["player_id"]) - set(player_countries["player_id"])
    if pending:
        print(f"Missing {len(pending)} players. Execute main to continue")
        raise SystemExit
    
    mvps = get_mvps(MVP_CSV)
    geojson = get_geojson()
    country_info = build_country_info(geojson)
    country_info.to_csv(COUNTRY_INFO_CSV, index=False)
    
    mvp_table = build_mvp_table(mvps, player_countries, country_info)
    mvp_table.to_csv(MVP_POSITION_CSV, index=False)
    
    counts = aggregate_countries(season_players, player_countries, country_info, mvp_table)
    counts.to_csv(COUNTRY_COUNTS_CSV, index=False)
    
    
    fig = build_figure(counts, mvp_table)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    fig.write_html(os.path.join(OUTPUT_PATH, OUTPUT_FILE), include_plotlyjs="cdn")
    
    print("Map saved")