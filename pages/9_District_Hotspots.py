import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

from utils.data_loader import (
    load_district_year_loss,
    load_district_map
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="District Hotspots | Western Ghats Sentinel",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F5F2EA;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .page-header {
        background:
            linear-gradient(
                135deg,
                #12372A,
                #1F5C45
            );

        padding: 40px;

        border-radius: 25px;

        color: white;

        margin-bottom: 30px;
    }

    .page-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #D7E6D8;
        font-weight: 600;
    }

    .page-title {
        font-size: 42px;
        font-weight: 800;
        margin-top: 8px;
    }

    .page-description {
        font-size: 16px;
        color: #D9E7DC;
        line-height: 1.7;
        max-width: 850px;
        margin-top: 12px;
    }

    .section-title {
        color: #12372A;
        font-size: 27px;
        font-weight: 750;
        margin-top: 35px;
        margin-bottom: 6px;
    }

    .section-description {
        color: #68756D;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .insight-card {
        background: #FFFDF8;
        border-left: 5px solid #C49A4A;
        padding: 22px 25px;
        border-radius: 12px;
        border-top: 1px solid #E5E0D5;
        border-right: 1px solid #E5E0D5;
        border-bottom: 1px solid #E5E0D5;
        margin-top: 20px;
    }

    .insight-title {
        color: #12372A;
        font-weight: 750;
        font-size: 17px;
        margin-bottom: 7px;
    }

    .insight-text {
        color: #5E6962;
        font-size: 14px;
        line-height: 1.6;
    }

    .hotspot-rank {
        display: inline-block;
        min-width: 26px;
        padding: 2px 8px;
        border-radius: 20px;
        background: #12372A;
        color: white;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
        margin-right: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

district_year = load_district_year_loss()
district_map = load_district_map()


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="page-header">

        <div class="page-label">
            District Intelligence
        </div>

        <div class="page-title">
            🎯 District Hotspots
        </div>

        <div class="page-description">
            Tree-cover loss at district granularity across the
            34 districts most relevant to Western Ghats habitat —
            naming the real places where forest is disappearing,
            not just the five broad states.
        </div>

    </div>
    """
)


# ============================================================
# FILTERS
# ============================================================

st.html(
    """
    <div class="section-title">
        Cumulative Loss by District
    </div>

    <div class="section-description">
        Select a year range to see which districts have lost the
        most tree cover within that window. Darker districts on
        the map have lost more forest.
    </div>
    """
)

year_min = int(district_year["year"].min())
year_max = int(district_year["year"].max())

year_range = st.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

filtered = district_year[
    (district_year["year"] >= year_range[0]) &
    (district_year["year"] <= year_range[1])
]

district_totals = (
    filtered
    .groupby(["state", "district"])
    .agg(
        tree_cover_loss_ha=("tree_cover_loss_ha", "sum"),
        co2_emissions_Mg=("co2_emissions_Mg", "sum")
    )
    .reset_index()
)

district_totals["district_key"] = (
    district_totals["state"] + "|" + district_totals["district"]
)


# ============================================================
# CHOROPLETH MAP
# ============================================================

map_plot = district_map.to_crs(epsg=4326).merge(
    district_totals,
    on="district_key",
    how="left",
    suffixes=("", "_agg")
)

fig_map = px.choropleth_map(
    map_plot,
    geojson=map_plot.__geo_interface__,
    locations=map_plot.index,
    color="tree_cover_loss_ha",
    hover_name="district",
    hover_data={
        "state": True,
        "tree_cover_loss_ha": ":,.0f"
    },
    color_continuous_scale=[
        "#E7F0E8",
        "#A8C5AD",
        "#5D8F6B",
        "#245D3D",
        "#12372A"
    ],
    map_style="white-bg",
    center={
        "lat": 13.5,
        "lon": 75.8
    },
    zoom=5.6,
    opacity=0.88
)

fig_map.update_layout(
    height=620,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(
        title="Tree-cover loss (ha)",
        thickness=14,
        len=0.65
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_map, use_container_width=True)


# ============================================================
# HOTSPOT RANKING TABLE
# ============================================================

st.html(
    """
    <div class="section-title">
        Ranked Hotspot Districts
    </div>

    <div class="section-description">
        The districts losing the most forest cover within the
        selected period, ranked highest to lowest.
    </div>
    """
)

ranked = district_totals.sort_values(
    "tree_cover_loss_ha", ascending=False
).reset_index(drop=True)

ranked.index = ranked.index + 1

display_table = ranked[
    ["state", "district", "tree_cover_loss_ha", "co2_emissions_Mg"]
].rename(columns={
    "state": "State",
    "district": "District",
    "tree_cover_loss_ha": "Tree-cover loss (ha)",
    "co2_emissions_Mg": "CO2e emissions (Mg)"
})

st.dataframe(
    display_table.style.format({
        "Tree-cover loss (ha)": "{:,.0f}",
        "CO2e emissions (Mg)": "{:,.0f}"
    }),
    use_container_width=True,
    height=460
)


# ============================================================
# INSIGHT CARD
# ============================================================

top_row = ranked.iloc[0]
top3 = ranked.head(3)
top3_names = ", ".join(
    f"{r['district']} ({r['state']})" for _, r in top3.iterrows()
)

st.html(
    f"""
    <div class="insight-card">

        <div class="insight-title">
            🔎 Hotspot signal
        </div>

        <div class="insight-text">

            <strong>{top_row['district']}, {top_row['state']}</strong>
            recorded the highest tree-cover loss of any district in
            the study region within the selected period, at
            approximately <strong>{top_row['tree_cover_loss_ha']:,.0f}
            hectares</strong>. The top three hotspot districts —
            {top3_names} — together account for a disproportionate
            share of total loss, suggesting that forest pressure in
            the Western Ghats is concentrated in specific corridors
            rather than spread evenly across the region.

        </div>

    </div>
    """
)
