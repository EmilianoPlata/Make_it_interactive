import pandas as pd
import streamlit as st

from constants import COUNTRY_COUNTS_CSV, MVP_POSITION_CSV
from interactive_map import build_figure

st.set_page_config(page_title="NBA Birth Countries", layout="wide")

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
    footer {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data

def load_data():
    counts = pd.read_csv(COUNTRY_COUNTS_CSV, keep_default_na=False, na_values=[""])
    counts["mvp_line"] = counts["mvp_line"].fillna("")
    mvps = pd.read_csv(MVP_POSITION_CSV, keep_default_na=False, na_values=[""])
    return counts, mvps

counts, mvps = load_data()

st.plotly_chart(build_figure(counts, mvps), config={"displayModeBar": False})
st.caption(
    "Data: Basketball-Reference.com (Sports Reference LLC). Base map: Natural Earth via Plotly. "
    "Country = birth country, not sporting nationality."
)