from season_label import season_label

def mvp_annotation(mvps, season):
    m = mvps[mvps["season"] == season]
    
    if not m.empty:
        r = m.iloc[0]
        text = f"{season_label(season)} MVP: {r['mvp_player']} (born in {r['country_name']})"
    elif season < 1956:
        text = f"{season_label(season)} MVP: No MVP awarded"
    else:
        text = f"{season_label(season)} MVP: No data available"
    
    return [dict(text=text, x=0.5, y=0.9, xref="paper", yref="paper", showarrow=False, font=dict(size=14, color="black"))]