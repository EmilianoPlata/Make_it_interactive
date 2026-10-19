import numpy as np
import plotly.graph_objects as go

def choropleth_trace(counts, season):
    d = counts[counts["season"] == season]
    return go.Choropleth(
        locations=d["iso3"],
        locationmode="ISO-3",
        z=np.log10(d["player_count"]),
        text=d["country_name"],
        customdata=d[["player_count", "mvp_line"]],
        coloraxis="coloraxis",
        marker_line_color="white",
        marker_line_width=0.5,
        hovertemplate="<b>%{text}</b><br>Players: %{customdata[0]}%{customdata[1]}<extra></extra>"
    )