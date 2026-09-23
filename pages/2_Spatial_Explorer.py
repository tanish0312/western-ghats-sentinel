import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Spatial Explorer | Western Ghats Sentinel",
    page_icon="🗺️",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_map():

    return gpd.read_file(
        "data/map_complete.geojson"
    )


@st.cache_data
def load_state_year():

    return pd.read_csv(
        "data/STATE_YEAR_TREE_LOSS.csv"
    )


try:

    map_df = load_map()
    state_year_df = load_state_year()

except Exception as e:

    st.error("Unable to load spatial datasets.")
    st.code(str(e))
    st.stop()


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

map_df.columns = [
    str(c).strip()
    for c in map_df.columns
]

state_year_df.columns = [
    str(c).strip()
    for c in state_year_df.columns
]


# ============================================================
# HELPER FUNCTION
# ============================================================

def find_column(df, possible_names):

    lower_map = {
        str(c).lower().strip(): c
        for c in df.columns
    }

    for name in possible_names:

        key = name.lower().strip()

        if key in lower_map:
            return lower_map[key]

    return None


# ============================================================
# IDENTIFY IMPORTANT COLUMNS
# ============================================================

state_col = find_column(
    map_df,
    [
        "state",
        "State",
        "STATE"
    ]
)

loss_col = find_column(
    map_df,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "total_tree_cover_loss_ha"
    ]
)

intensity_col = find_column(
    map_df,
    [
        "loss_per_1000km2",
        "loss_per_1000_km2"
    ]
)

emissions_col = find_column(
    map_df,
    [
        "total_emissions_Mg",
        "total_emissions_mg",
        "emissions_Mg"
    ]
)

co2_col = find_column(
    map_df,
    [
        "Mg_CO2e_per_ha",
        "mg_co2e_per_ha",
        "CO2e_per_ha"
    ]
)


if state_col is None:

    st.error(
        "The state column could not be identified in map_complete.geojson."
    )

    st.write(
        "Available columns:",
        list(map_df.columns)
    )

    st.stop()


# ============================================================
# PAGE STYLING
# ============================================================

st.html("""
<style>

.main {
    background: #F7F5EF;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}


/* PAGE HEADER */

.page-label {
    color: #A0802E;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}

.page-title {
    color: #153D2C;
    font-size: 40px;
    font-weight: 850;
    letter-spacing: -1px;
    margin-top: 5px;
}

.page-description {
    color: #69756E;
    font-size: 14px;
    line-height: 1.7;
    max-width: 1050px;
    margin-bottom: 25px;
}


/* CONTROL PANEL */

.control-panel {
    background: white;
    border: 1px solid #E3E2DA;
    border-radius: 16px;
    padding: 20px 24px;
    margin: 20px 0 30px 0;
    box-shadow: 0 5px 18px rgba(0,0,0,0.035);
}


/* METRIC CARDS */

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 20px 0 35px 0;
}

.metric-card {
    background: white;
    border: 1px solid #E3E2DA;
    border-radius: 16px;
    padding: 21px;
    min-height: 120px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.035);
}

.metric-label {
    color: #78827C;
    font-size: 9px;
    font-weight: 850;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.metric-value {
    color: #12372A;
    font-size: 25px;
    font-weight: 850;
    margin-top: 9px;
}

.metric-description {
    color: #929A95;
    font-size: 10px;
    margin-top: 5px;
}


/* SECTION */

.section-label {
    color: #A0802E;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 35px;
}

.section-title {
    color: #153D2C;
    font-size: 28px;
    font-weight: 850;
    margin-top: 4px;
}

.section-description {
    color: #69756E;
    font-size: 13px;
    line-height: 1.7;
}


/* PROFILE */

.profile-card {
    background: #12372A;
    color: white;
    border-radius: 18px;
    padding: 27px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(18,55,42,0.18);
}

.profile-label {
    color: #DCC56B;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.profile-title {
    color: white;
    font-size: 31px;
    font-weight: 850;
    margin-top: 5px;
}

.profile-text {
    color: #D3E2D8;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 8px;
}


/* INSIGHT */

.insight-box {
    background: #EFF5EF;
    border: 1px solid #D8E7D9;
    border-radius: 15px;
    padding: 20px;
    margin-top: 25px;
}

.insight-title {
    color: #245D3D;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.insight-text {
    color: #627067;
    font-size: 13px;
    line-height: 1.75;
    margin-top: 7px;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #929A95;
    font-size: 11px;
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid #DDDDD5;
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="page-label">
    Interactive Geography
</div>

<div class="page-title">
    Western Ghats Environmental Map
</div>

<div class="page-description">

Explore environmental indicators across the five-state
Western Ghats study region and inspect individual state
profiles.

</div>
""")


# ============================================================
# INDICATOR SELECTION
# ============================================================

st.html("""
<div class="control-panel">
    <b style="color:#153D2C;">Map Indicator</b>
    <br>
    <span style="color:#69756E;font-size:12px;">
        Choose the environmental measure displayed on the map.
    </span>
</div>
""")


indicator_options = {}

if loss_col:
    indicator_options[
        "Tree-Cover Loss (ha)"
    ] = loss_col

if intensity_col:
    indicator_options[
        "Loss / 1,000 km²"
    ] = intensity_col

if emissions_col:
    indicator_options[
        "CO₂ Emissions (Mg)"
    ] = emissions_col

if co2_col:
    indicator_options[
        "CO₂e / ha"
    ] = co2_col


if not indicator_options:

    st.error(
        "No recognized environmental indicator columns were found."
    )

    st.write(
        "Available columns:",
        list(map_df.columns)
    )

    st.stop()


selected_indicator = st.selectbox(
    "Environmental indicator",
    list(indicator_options.keys())
)


selected_column = indicator_options[
    selected_indicator
]


# ============================================================
# MAP STATISTICS
# ============================================================

map_values = pd.to_numeric(
    map_df[selected_column],
    errors="coerce"
)

map_df["_map_value"] = map_values


# ============================================================
# TOP METRICS
# ============================================================

valid_values = map_values.dropna()


if len(valid_values) > 0:

    highest_value = valid_values.max()

    lowest_value = valid_values.min()

    average_value = valid_values.mean()

else:

    highest_value = 0
    lowest_value = 0
    average_value = 0


def format_value(value):

    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value/1_000:.1f}K"

    return f"{value:,.1f}"


st.html(
    f"""
<div class="metric-grid">

    <div class="metric-card">

        <div class="metric-label">
            States
        </div>

        <div class="metric-value">
            {map_df[state_col].nunique()}
        </div>

        <div class="metric-description">
            States represented
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Highest
        </div>

        <div class="metric-value">
            {format_value(highest_value)}
        </div>

        <div class="metric-description">
            Maximum selected indicator
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Lowest
        </div>

        <div class="metric-value">
            {format_value(lowest_value)}
        </div>

        <div class="metric-description">
            Minimum selected indicator
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Average
        </div>

        <div class="metric-value">
            {format_value(average_value)}
        </div>

        <div class="metric-description">
            Five-state average
        </div>

    </div>

</div>
"""
)


# ============================================================
# MAP
# ============================================================

st.html("""
<div class="section-label">
    Interactive Map
</div>

<div class="section-title">
    Spatial Distribution
</div>

<div class="section-description">

Darker areas represent higher values of the selected
indicator. Hover over a state to inspect its value.

</div>
""")


# Make geometry WGS84 for Plotly
map_plot = map_df.to_crs(epsg=4326).copy()


fig_map = px.choropleth_map(
    map_plot,
    geojson=map_plot.__geo_interface__,
    locations=map_plot.index,
    color="_map_value",
    hover_name=state_col,
    hover_data={
        "_map_value": ":,.2f"
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
        "lat": 15.5,
        "lon": 75.5
    },
    zoom=4.8,
    opacity=0.85
)


fig_map.update_layout(
    height=620,
    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    ),
    coloraxis_colorbar=dict(
        title=selected_indicator,
        thickness=14,
        len=0.65
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig_map,
    use_container_width=True
)


# ============================================================
# STATE PROFILE
# ============================================================

st.html("""
<div class="section-label">
    State Intelligence
</div>

<div class="section-title">
    Explore a State
</div>

<div class="section-description">

Select a state to generate an environmental profile using
the underlying state-level analytical data.

</div>
""")


states = sorted(
    map_df[state_col]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


selected_state = st.selectbox(
    "Select state",
    states
)


# ============================================================
# SELECT STATE DATA
# ============================================================

state_record = map_df[
    map_df[state_col].astype(str)
    == selected_state
].iloc[0]


# ============================================================
# PROFILE HEADER
# ============================================================

st.html(
    f"""
<div class="profile-card">

    <div class="profile-label">
        State Profile
    </div>

    <div class="profile-title">
        {selected_state}
    </div>

    <div class="profile-text">

        Environmental indicators for {selected_state}
        within the Western Ghats study region.

    </div>

</div>
"""
)


# ============================================================
# STATE METRICS
# ============================================================

profile_metrics = []


if loss_col:

    value = pd.to_numeric(
        state_record[loss_col],
        errors="coerce"
    )

    if pd.notna(value):

        profile_metrics.append(
            (
                "TREE-COVER LOSS",
                f"{value:,.1f} ha",
                "Total recorded loss"
            )
        )


if intensity_col:

    value = pd.to_numeric(
        state_record[intensity_col],
        errors="coerce"
    )

    if pd.notna(value):

        profile_metrics.append(
            (
                "LOSS INTENSITY",
                f"{value:,.1f}",
                "ha per 1,000 km²"
            )
        )


if emissions_col:

    value = pd.to_numeric(
        state_record[emissions_col],
        errors="coerce"
    )

    if pd.notna(value):

        profile_metrics.append(
            (
                "CO₂ EMISSIONS",
                f"{value:,.1f} Mg",
                "Total estimated emissions"
            )
        )


if co2_col:

    value = pd.to_numeric(
        state_record[co2_col],
        errors="coerce"
    )

    if pd.notna(value):

        profile_metrics.append(
            (
                "CO₂e / HA",
                f"{value:,.2f}",
                "Emissions intensity"
            )
        )


if profile_metrics:

    cards_html = '<div class="metric-grid">'

    for label, value, description in profile_metrics:

        cards_html += f"""

        <div class="metric-card">

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-description">
                {description}
            </div>

        </div>

        """

    cards_html += "</div>"

    st.html(cards_html)


# ============================================================
# STATE VS AVERAGE
# ============================================================

if loss_col:

    state_loss = pd.to_numeric(
        state_record[loss_col],
        errors="coerce"
    )

    overall_average = pd.to_numeric(
        map_df[loss_col],
        errors="coerce"
    ).mean()


    if pd.notna(state_loss) and pd.notna(overall_average):

        difference_percent = (
            (state_loss - overall_average)
            / overall_average
        ) * 100


        if difference_percent > 0:

            comparison_text = (
                f"{selected_state} records "
                f"{abs(difference_percent):.1f}% more "
                f"tree-cover loss than the five-state "
                f"average."
            )

        elif difference_percent < 0:

            comparison_text = (
                f"{selected_state} records "
                f"{abs(difference_percent):.1f}% less "
                f"tree-cover loss than the five-state "
                f"average."
            )

        else:

            comparison_text = (
                f"{selected_state} is approximately equal "
                f"to the five-state average."
            )


        st.html(
            f"""
<div class="insight-box">

    <div class="insight-title">
        State Comparison
    </div>

    <div class="insight-text">
        {comparison_text}
    </div>

</div>
"""
        )


# ============================================================
# STATE TIME SERIES
# ============================================================

year_col = find_column(
    state_year_df,
    [
        "year",
        "Year",
        "YEAR"
    ]
)

state_year_state_col = find_column(
    state_year_df,
    [
        "state",
        "State",
        "STATE"
    ]
)

state_year_loss_col = find_column(
    state_year_df,
    [
        "tree_cover_loss_ha",
        "total_loss_ha",
        "loss_ha"
    ]
)


if (
    year_col
    and state_year_state_col
    and state_year_loss_col
):

    state_history = state_year_df[
        state_year_df[state_year_state_col]
        .astype(str)
        == selected_state
    ].copy()


    state_history[year_col] = pd.to_numeric(
        state_history[year_col],
        errors="coerce"
    )


    state_history[state_year_loss_col] = pd.to_numeric(
        state_history[state_year_loss_col],
        errors="coerce"
    )


    state_history = (
        state_history
        .dropna(
            subset=[
                year_col,
                state_year_loss_col
            ]
        )
        .sort_values(year_col)
    )


    if not state_history.empty:

        st.html("""
        <div class="section-label">
            Temporal Profile
        </div>

        <div class="section-title">
            Tree-Cover Loss Through Time
        </div>

        <div class="section-description">

        Annual recorded tree-cover loss for the selected state.

        </div>
        """)


        fig_history = px.area(
            state_history,
            x=year_col,
            y=state_year_loss_col
        )


        fig_history.update_traces(
            line=dict(
                color="#245D3D",
                width=3
            ),
            fillcolor="rgba(36,93,61,0.18)",
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Tree-Cover Loss: %{y:,.1f} ha"
                "<extra></extra>"
            )
        )


        fig_history.update_layout(
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            xaxis_title="Year",
            yaxis_title="Tree-Cover Loss (ha)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified"
        )


        st.plotly_chart(
            fig_history,
            use_container_width=True
        )


# ============================================================
# RESEARCH NOTE
# ============================================================

st.html(
    """
<div class="insight-box">

    <div class="insight-title">
        Interpretation Note
    </div>

    <div class="insight-text">

        The map displays state-level environmental indicators.
        It should not be interpreted as a district-level
        measurement of tree-cover loss.

        Normalized indicators such as loss per 1,000 km² help
        provide geographic context when comparing states of
        different sizes.

    </div>

</div>
"""
)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    <b>Western Ghats Sentinel</b>

    &nbsp;•&nbsp;

    Tree Cover • Carbon • Conservation

    <br><br>

    Interactive Spatial Intelligence

</div>
""")