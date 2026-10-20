import numpy as np
import plotly.graph_objects as go

from choropleth_trace import choropleth_trace
from mvp_trace import mvp_trace
from mvp_annotation import mvp_annotation
from season_label import season_label
from discrete_colorscale import BIN_LABELS, discrete_colorscale

NO_DATA_COLOR = "lightgray"

TICKS = [1, 2, 5, 10, 20, 50, 100, 200, 500]

def build_figure(counts, mvps, height=540):
    
    seasons = sorted(counts["season"].unique())
    last = seasons[-1]
    max_count = counts["player_count"].max()
    ticks = [t for t in TICKS if t <= max_count]
    
    frames = [
        go.Frame(
            name=str(s),
            data=[
                choropleth_trace(counts, s),
                mvp_trace(mvps, s)
            ],
            traces=[0, 1],
            layout=dict(annotations = mvp_annotation(mvps, counts,s))
        ) 
        for s in seasons
    ] 
    
    fig = go.Figure(data=[choropleth_trace(counts, last), mvp_trace(mvps, last)], frames=frames)
    
    slider_steps = [
        dict(
            method="animate",
            label=season_label(s),
            args=[[str(s)], dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
        )
        for s in seasons
    ]
    
    fig.update_layout(
        title=dict(
            text="<b>From an American league to a global one: where NBA players were born</b><br>"
                 "<sup>Each country is coloured by how many players born there appeared in the selected season. "
                 "⭐ marks the MVP’s birthplace. Hover a country for exact numbers.</sup>",
            x=0.02, y=0.97,
            font=dict(size=18)
        ),
        coloraxis=dict(
            colorscale=discrete_colorscale(),
            cmin=-0.5,
            cmax=len(BIN_LABELS) - 0.5,
            colorbar=dict(title="Players", tickvals=list(range(len(BIN_LABELS))), ticktext=BIN_LABELS, len=0.6, thickness=14, x=0.98)
        ),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            showland=True,
            landcolor = NO_DATA_COLOR,
            showcountries=True,
            countrycolor="white",
            projection_type="natural earth",
            lataxis_range=[-58, 85],
            domain=dict(x=[0, 0.94], y=[0.08, 0.88])          
        ),
        annotations = mvp_annotation(mvps, counts,last),
        updatemenus=[dict(
            type="buttons", direction="left", x=0.0, y=-0.06, xanchor="left", yanchor="top", pad=dict(t=0, r=10),showactive=False,
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, dict(frame=dict(duration=250, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
                dict(label="❚❚ Pause", method="animate",
                     args=[[None], dict(mode="immediate", frame=dict(duration=0, redraw=False), transition=dict(duration=0))]),
            ],
        )],
        sliders=[dict(
            active=len(seasons) - 1,
            steps=slider_steps,
            x=0.14, len=0.84, y=0.08, yanchor="top", pad=dict(t=0, b=0),
            font=dict(color="rgba(0,0,0,0)"),
            currentvalue=dict(prefix="Season: ", font=dict(size=14, color="#1a1a1a")),
        )],
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
    )
    
    return fig
