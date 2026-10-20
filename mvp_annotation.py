from season_label import season_label

def mvp_annotation(mvps, counts, season):
    d = counts[counts["season"]==season]
    total = d["player_count"].sum()
    international = d.loc[d["iso3"] != "USA", "player_count"].sum()
    share_line = f"Born outside the USA: {international} of {total} players ({international / total:.0%})"
    
    m = mvps[mvps["season"] == season]
    
    if not m.empty:
        r = m.iloc[0]
        mvp_line = f"MVP: {r['mvp_player']} (born in {r['country_name']})"
    elif season < 1956:
        mvp_line = "No MVP award yet"
    else:
        mvp_line =""
    
    text = f"<b>{season_label(season)}</b><br>{share_line}"
    if mvp_line:
        text += f"<br>{mvp_line}"
    
    return [dict(text=text, x=0.01, y=0.12, xanchor="left", yanchor="bottom", xref="paper", yref="paper",
                 showarrow=False, align="left", font=dict(size=13, color="#1a1a1a"),
                 bgcolor="rgba(255,255,255,0.9)", bordercolor="#cccccc", borderwidth=1, borderpad=6)]