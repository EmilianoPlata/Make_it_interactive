import plotly.graph_objects as go

def mvp_trace(mvps, season):
    m = mvps[mvps["season"] == season]
    return go.Scattergeo(
        lon=m["longitude"],
        lat=m["latitude"],
        mode="markers",
        marker=dict(symbol="star", size=16, color="gold", line=dict(width=1.5, color="black")),
        customdata=m[["mvp_player", "country_name"]],
        hovertemplate="MVP: %{customdata[0]}<br>%{customdata[1]}<extra></extra>",
        showlegend=False
    )