import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Conservation | Western Ghats Sentinel",
    page_icon="🐘",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    history = pd.read_csv(
        "data/SPECIES_STATUS_HISTORY.csv"
    )

    trends = pd.read_csv(
        "data/SPECIES_STATUS_TRENDS.csv"
    )

    transitions = pd.read_csv(
        "data/SPECIES_STATUS_TRANSITIONS.csv"
    )

    return history, trends, transitions


history, trends, transitions = load_data()


# ============================================================
# DATASET COLUMNS
# ============================================================

SPECIES = "species"
COMMON_NAME = "common_name"
ORDER = "order"
FAMILY = "family"
YEAR = "year_published"
RED_LIST = "red_list_category"
LATEST = "is_latest"
STATUS = "status_standardized"


# ============================================================
# REQUIRED COLUMN CHECK
# ============================================================

required_columns = [
    SPECIES,
    COMMON_NAME,
    YEAR,
    STATUS
]

missing = [
    col
    for col in required_columns
    if col not in history.columns
]


if missing:

    st.error(
        "Required columns are missing from "
        "SPECIES_STATUS_HISTORY.csv."
    )

    st.write("Missing columns:")
    st.write(missing)

    st.write("Available columns:")

    st.code(
        "\n".join(history.columns.tolist())
    )

    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

history = history.copy()

history[SPECIES] = (
    history[SPECIES]
    .astype(str)
    .str.strip()
)

history[COMMON_NAME] = (
    history[COMMON_NAME]
    .astype(str)
    .str.strip()
)

history[STATUS] = (
    history[STATUS]
    .astype(str)
    .str.strip()
)

history[YEAR] = pd.to_numeric(
    history[YEAR],
    errors="coerce"
)


# ============================================================
# BASIC INFORMATION
# ============================================================

species_list = sorted(
    history[SPECIES]
    .dropna()
    .unique()
    .tolist()
)

species_count = len(species_list)

status_count = (
    history[STATUS]
    .replace(
        {
            "nan": None,
            "None": None,
            "": None
        }
    )
    .dropna()
    .nunique()
)

valid_years = history[YEAR].dropna()

if not valid_years.empty:

    min_year = int(
        valid_years.min()
    )

    max_year = int(
        valid_years.max()
    )

else:

    min_year = "—"
    max_year = "—"


# ============================================================
# STANDARD STATUS ORDER
# ============================================================

STANDARD_STATUS_ORDER = [

    "Least Concern",

    "Near Threatened",

    "Vulnerable",

    "Endangered",

    "Critically Endangered",

    "Extinct in the Wild",

    "Extinct"

]


# ============================================================
# PAGE CSS
# ============================================================

st.html(
    """
    <style>

    .main {
        background: #F7F5EF;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    .page-label {
        color: #A0802E;
        font-size: 10px;
        font-weight: 850;
        letter-spacing: 2.6px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .page-title {
        color: #153D2C;
        font-size: 40px;
        font-weight: 850;
        letter-spacing: -1px;
        margin: 0;
    }

    .page-description {
        color: #69756E;
        font-size: 14px;
        line-height: 1.75;
        max-width: 950px;
        margin-top: 9px;
        margin-bottom: 25px;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 22px 0 38px 0;
    }

    .metric-card {
        background: white;
        border: 1px solid #E4E3DC;
        border-radius: 16px;
        padding: 22px;
        min-height: 125px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.045);
    }

    .metric-label {
        color: #78827C;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.6px;
        text-transform: uppercase;
    }

    .metric-value {
        color: #12372A;
        font-size: 28px;
        font-weight: 850;
        margin-top: 8px;
    }

    .metric-description {
        color: #929A95;
        font-size: 11px;
        margin-top: 5px;
    }

    .section-label {
        color: #A0802E;
        font-size: 10px;
        font-weight: 850;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-top: 30px;
    }

    .section-title {
        color: #153D2C;
        font-size: 28px;
        font-weight: 850;
        margin-top: 4px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #69756E;
        font-size: 13px;
        line-height: 1.7;
        max-width: 950px;
        margin-bottom: 18px;
    }

    .species-profile {
        background: linear-gradient(
            135deg,
            #12372A,
            #245D3D
        );
        border-radius: 18px;
        padding: 30px;
        color: white;
        box-shadow: 0 10px 28px rgba(18,55,42,0.15);
        margin-top: 18px;
        margin-bottom: 25px;
    }

    .species-label {
        color: #D9C77E;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .species-name {
        color: white;
        font-size: 30px;
        font-weight: 850;
        margin-top: 7px;
    }

    .species-common {
        color: #D8E7DC;
        font-size: 15px;
        margin-top: 3px;
    }

    .species-status {
        display: inline-block;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.15);
        color: #F3E9B5;
        padding: 8px 13px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 750;
        margin-top: 15px;
    }

    .insight {
        background: linear-gradient(
            90deg,
            #EEF5EE,
            #F5F7F1
        );
        border-left: 5px solid #2E6B45;
        border-radius: 12px;
        padding: 20px 23px;
        margin: 22px 0 30px 0;
    }

    .insight-label {
        color: #9A7B2F;
        font-size: 10px;
        font-weight: 850;
        letter-spacing: 1.7px;
        text-transform: uppercase;
    }

    .insight-title {
        color: #12372A;
        font-size: 16px;
        font-weight: 800;
        margin-top: 5px;
    }

    .insight-text {
        color: #59675E;
        font-size: 13px;
        line-height: 1.7;
        margin-top: 4px;
    }

    .validation {
        background: #F1F6F1;
        border: 1px solid #DCE9DE;
        border-radius: 13px;
        padding: 17px 20px;
        margin-top: 25px;
    }

    .validation-title {
        color: #245D3D;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .validation-text {
        color: #68766D;
        font-size: 12px;
        line-height: 1.65;
        margin-top: 5px;
    }

    .footer {
        text-align: center;
        color: #929A95;
        font-size: 11px;
        padding-top: 38px;
        margin-top: 45px;
        border-top: 1px solid #DDDDD5;
    }

    </style>
    """
)


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="page-label">
        Conservation Intelligence
    </div>

    <div class="page-title">
        Conservation
    </div>

    <div class="page-description">

        Explore species conservation-status patterns,
        historical trajectories, status transitions and
        species-level conservation signals across the
        Western Ghats study dataset.

    </div>
    """
)

# ============================================================
# FEATURED CASE STUDY — KOLAR LEAF-NOSED BAT
# ============================================================

spotlight = history[
    history[SPECIES] == "Hipposideros hypophyllus"
].sort_values(YEAR)

status_colors = {
    "NT": "#D98A33",
    "VU": "#C9762E",
    "EN": "#B84A3A",
    "CR": "#8B1E1E",
}

timeline_steps = "".join(
    f"""
    <div class="spotlight-step">
        <div class="spotlight-dot" style="background:{status_colors.get(row[STATUS], '#999')}"></div>
        <div class="spotlight-year">{int(row[YEAR])}</div>
        <div class="spotlight-status" style="color:{status_colors.get(row[STATUS], '#999')}">{row[STATUS]}</div>
    </div>
    """
    for _, row in spotlight.iterrows()
)

st.html(
    f"""
    <style>
    .spotlight-card {{
        margin: 30px 0 40px 0;
        padding: 32px 36px;
        border-radius: 22px;
        background: linear-gradient(135deg, #1F4D36, #0b4a36);
        color: white;
        box-shadow: 0 8px 30px rgba(20,60,48,0.2);
    }}
    .spotlight-label {{
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #dcc66d;
        font-weight: 700;
    }}
    .spotlight-title {{
        font-size: 28px;
        font-weight: 800;
        margin-top: 6px;
    }}
    .spotlight-sub {{
        font-size: 14px;
        color: #c9dad2;
        font-style: italic;
        margin-bottom: 18px;
    }}
    .spotlight-timeline {{
        display: flex;
        align-items: center;
        gap: 6px;
        margin: 24px 0 20px 0;
        flex-wrap: wrap;
    }}
    .spotlight-step {{
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 60px;
    }}
    .spotlight-dot {{
        width: 16px;
        height: 16px;
        border-radius: 50%;
        margin-bottom: 6px;
        border: 2px solid white;
    }}
    .spotlight-year {{
        font-size: 12px;
        color: #c9dad2;
    }}
    .spotlight-status {{
        font-size: 15px;
        font-weight: 800;
        margin-top: 2px;
    }}
    .spotlight-narrative {{
        font-size: 15px;
        line-height: 1.7;
        color: #e8f1ed;
        max-width: 820px;
    }}
    </style>

    <div class="spotlight-card">
        <div class="spotlight-label">Featured Case Study</div>
        <div class="spotlight-title">🦇 The Kolar Leaf-nosed Bat</div>
        <div class="spotlight-sub">Hipposideros hypophyllus — endemic to a single cave system in Karnataka</div>

        <div class="spotlight-timeline">
            {timeline_steps}
        </div>

        <div class="spotlight-narrative">
            In just twenty years, this bat's global status slid from
            <b>Near Threatened</b> to <b>Critically Endangered</b> — one of
            the steepest declines of any species in this dataset. Unlike
            wide-ranging mammals such as the tiger or elephant, the Kolar
            Leaf-nosed Bat depends on a single known roosting cave, making
            it acutely vulnerable to localized habitat disturbance from
            quarrying and encroachment. Its trajectory is a concentrated
            illustration of the pattern this dashboard traces at scale:
            habitat pressure translating directly into conservation risk.
        </div>
    </div>
    """
)

# ============================================================
# KPI CARDS
# ============================================================

total_transitions = 0

transition_records = []


for species in species_list:

    temp = history[
        history[SPECIES] == species
    ].sort_values(YEAR)

    if len(temp) < 2:
        continue

    for i in range(1, len(temp)):

        previous = str(
            temp.iloc[i - 1][STATUS]
        )

        current = str(
            temp.iloc[i][STATUS]
        )

        if previous != current:

            transition_records.append(
                {
                    "Species": species,
                    "Year": temp.iloc[i][YEAR],
                    "From": previous,
                    "To": current
                }
            )


total_transitions = len(
    transition_records
)


st.html(
    f"""
    <div class="metric-grid">

        <div class="metric-card">

            <div class="metric-label">
                Species
            </div>

            <div class="metric-value">
                {species_count}
            </div>

            <div class="metric-description">
                Species represented
            </div>

        </div>


        <div class="metric-card">

            <div class="metric-label">
                Status Categories
            </div>

            <div class="metric-value">
                {status_count}
            </div>

            <div class="metric-description">
                Recorded categories
            </div>

        </div>


        <div class="metric-card">

            <div class="metric-label">
                Recorded Transitions
            </div>

            <div class="metric-value">
                {total_transitions}
            </div>

            <div class="metric-description">
                Status changes identified
            </div>

        </div>


        <div class="metric-card">

            <div class="metric-label">
                Study Window
            </div>

            <div class="metric-value">
                {min_year}–{max_year}
            </div>

            <div class="metric-description">
                Available observations
            </div>

        </div>

    </div>
    """
)


# ============================================================
# CURRENT STATUS DISTRIBUTION
# ============================================================

st.html(
    """
    <div class="section-label">
        Conservation Landscape
    </div>

    <div class="section-title">
        Current Status Distribution
    </div>

    <div class="section-description">

        The latest available status record for each species
        is used to summarise the current distribution of
        recorded conservation categories.

    </div>
    """
)


# ============================================================
# LATEST RECORDS
# ============================================================

if LATEST in history.columns:

    latest_flag = (
        history[LATEST]
        .astype(str)
        .str.lower()
    )

    latest_history = history[
        latest_flag.isin(
            ["true", "1", "yes"]
        )
    ].copy()

    if latest_history.empty:

        latest_history = (
            history
            .sort_values(YEAR)
            .groupby(
                SPECIES,
                as_index=False
            )
            .tail(1)
        )

else:

    latest_history = (
        history
        .sort_values(YEAR)
        .groupby(
            SPECIES,
            as_index=False
        )
        .tail(1)
    )


latest_status_counts = (
    latest_history[STATUS]
    .value_counts()
    .reset_index()
)

latest_status_counts.columns = [
    "Status",
    "Species Count"
]


# ============================================================
# STATUS CHART
# ============================================================

fig_status = px.bar(
    latest_status_counts,
    x="Species Count",
    y="Status",
    orientation="h"
)


fig_status.update_traces(
    marker_color="#2E6B45",
    hovertemplate=
        "<b>%{y}</b><br>"
        "Species: %{x}"
        "<extra></extra>"
)


fig_status.update_layout(

    height=390,

    margin=dict(
        l=10,
        r=20,
        t=10,
        b=15
    ),

    paper_bgcolor="white",

    plot_bgcolor="white",

    font=dict(
        family="Arial",
        color="#5F6D64"
    ),

    xaxis=dict(
        title="Number of species",
        gridcolor="#E8E8E2",
        zeroline=False
    ),

    yaxis=dict(
        title=None,
        autorange="reversed",
        showgrid=False
    )
)


st.plotly_chart(
    fig_status,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# ============================================================
# SPECIES × YEAR HEATMAP
# ============================================================

st.html(
    """
    <div class="section-label">
        Conservation Timeline
    </div>

    <div class="section-title">
        Species × Year Status Heatmap
    </div>

    <div class="section-description">

        A compact view of how the recorded conservation
        status varies across species and observation years.
        Hover over any cell to inspect the underlying status.

    </div>
    """
)


heatmap_data = history[
    [
        SPECIES,
        YEAR,
        STATUS
    ]
].dropna().copy()


# ------------------------------------------------------------
# Assign numeric positions to status categories
# ------------------------------------------------------------

observed_statuses = (
    heatmap_data[STATUS]
    .astype(str)
    .unique()
    .tolist()
)


ordered_statuses = []


for status in STANDARD_STATUS_ORDER:

    if status in observed_statuses:

        ordered_statuses.append(status)


for status in observed_statuses:

    if status not in ordered_statuses:

        ordered_statuses.append(status)


status_number = {
    status: i
    for i, status
    in enumerate(ordered_statuses)
}


heatmap_data["Status Number"] = (
    heatmap_data[STATUS]
    .map(status_number)
)


# ------------------------------------------------------------
# Limit duplicate species-year records
# ------------------------------------------------------------

heatmap_data = (
    heatmap_data
    .sort_values(YEAR)
    .drop_duplicates(
        subset=[
            SPECIES,
            YEAR
        ],
        keep="last"
    )
)


# ------------------------------------------------------------
# Pivot
# ------------------------------------------------------------

heatmap_pivot = heatmap_data.pivot(
    index=SPECIES,
    columns=YEAR,
    values="Status Number"
)


if not heatmap_pivot.empty:

    heatmap_text = heatmap_data.pivot(
        index=SPECIES,
        columns=YEAR,
        values=STATUS
    )


    fig_heatmap = go.Figure(

        go.Heatmap(

            z=heatmap_pivot.values,

            x=heatmap_pivot.columns,

            y=heatmap_pivot.index,

            text=heatmap_text.values,

            customdata=heatmap_text.values,

            colorscale=[
                [0.00, "#DCEBDD"],
                [0.16, "#C4DCC7"],
                [0.32, "#A8C9AD"],
                [0.48, "#88B391"],
                [0.64, "#679977"],
                [0.80, "#3F7653"],
                [1.00, "#12372A"]
            ],

            colorbar=dict(

                title=dict(
                    text="Status level"
                ),

                tickmode="array",

                tickvals=list(
                    range(
                        len(ordered_statuses)
                    )
                ),

                ticktext=ordered_statuses

            ),

            hovertemplate=

                "<b>%{y}</b><br>"
                "Year: %{x}<br>"
                "Status: %{customdata}"
                "<extra></extra>"
        )
    )


    fig_heatmap.update_layout(

        height=max(
            500,
            len(heatmap_pivot) * 25
        ),

        margin=dict(
            l=10,
            r=20,
            t=15,
            b=20
        ),

        paper_bgcolor="white",

        font=dict(
            family="Arial",
            color="#5F6D64"
        ),

        xaxis=dict(
            title="Year",
            side="bottom"
        ),

        yaxis=dict(
            title="Species",
            autorange="reversed"
        )

    )


    st.plotly_chart(
        fig_heatmap,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# SPECIES EXPLORER
# ============================================================

st.html(
    """
    <div class="section-label">
        Species Explorer
    </div>

    <div class="section-title">
        Investigate an Individual Species
    </div>

    <div class="section-description">

        Select a species to inspect its taxonomy, latest
        recorded status and historical trajectory.

    </div>
    """
)


selected_species = st.selectbox(
    "Select a species",
    species_list
)


species_data = history[
    history[SPECIES]
    == selected_species
].copy()


species_data = species_data.sort_values(
    YEAR
)


latest_row = species_data.iloc[-1]

latest_status = latest_row[STATUS]

common_name = latest_row[COMMON_NAME]

family = (
    latest_row[FAMILY]
    if FAMILY in history.columns
    else "—"
)

order = (
    latest_row[ORDER]
    if ORDER in history.columns
    else "—"
)


# ============================================================
# SPECIES PROFILE
# ============================================================

st.html(
    f"""
    <div class="species-profile">

        <div class="species-label">
            Selected Species
        </div>

        <div class="species-name">
            {selected_species}
        </div>

        <div class="species-common">
            {common_name}
        </div>

        <div class="species-status">
            Latest recorded status:
            {latest_status}
        </div>

    </div>
    """
)


# ============================================================
# SPECIES DETAILS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Family",
        family
    )


with col2:

    st.metric(
        "Order",
        order
    )


with col3:

    st.metric(
        "Observations",
        len(species_data)
    )


# ============================================================
# HISTORICAL SPECIES TIMELINE
# ============================================================

st.html(
    """
    <div class="section-label">
        Historical Trajectory
    </div>

    <div class="section-title">
        Conservation Status Through Time
    </div>

    <div class="section-description">

        Each point represents a recorded conservation
        status for the selected species.

    </div>
    """
)


observed_species_statuses = (
    species_data[STATUS]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


species_status_order = []


for status in STANDARD_STATUS_ORDER:

    if status in observed_species_statuses:

        species_status_order.append(status)


for status in observed_species_statuses:

    if status not in species_status_order:

        species_status_order.append(status)


species_status_number = {
    status: i
    for i, status
    in enumerate(species_status_order)
}


species_data["status_number"] = (
    species_data[STATUS]
    .map(species_status_number)
)


fig_timeline = go.Figure()


fig_timeline.add_trace(

    go.Scatter(

        x=species_data[YEAR],

        y=species_data["status_number"],

        mode="lines+markers",

        line=dict(
            color="#2E6B45",
            width=3
        ),

        marker=dict(
            size=11
        ),

        customdata=species_data[
            [STATUS]
        ],

        hovertemplate=
            "<b>%{x}</b><br>"
            "Status: %{customdata[0]}"
            "<extra></extra>"
    )
)


fig_timeline.update_layout(

    height=420,

    margin=dict(
        l=15,
        r=20,
        t=15,
        b=15
    ),

    paper_bgcolor="white",

    plot_bgcolor="white",

    font=dict(
        family="Arial",
        color="#5F6D64"
    ),

    xaxis=dict(
        title="Year",
        dtick=1,
        showgrid=False
    ),

    yaxis=dict(

        title="Conservation status",

        tickmode="array",

        tickvals=list(
            range(
                len(species_status_order)
            )
        ),

        ticktext=species_status_order,

        gridcolor="#E8E8E2"
    )
)


st.plotly_chart(
    fig_timeline,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# ============================================================
# SPECIES TRANSITION SUMMARY
# ============================================================

selected_transition_count = 0


if len(species_data) >= 2:

    for i in range(
        1,
        len(species_data)
    ):

        previous = str(
            species_data.iloc[i - 1][STATUS]
        )

        current = str(
            species_data.iloc[i][STATUS]
        )

        if previous != current:

            selected_transition_count += 1


if selected_transition_count > 0:

    st.html(
        f"""
        <div class="insight">

            <div class="insight-label">
                Species Signal
            </div>

            <div class="insight-title">
                {selected_species} has
                {selected_transition_count}
                recorded status transition(s)
            </div>

            <div class="insight-text">

                The selected species has multiple recorded
                status observations and at least one change
                between consecutive observations in the
                prepared dataset.

            </div>

        </div>
        """
    )

else:

    st.html(
        f"""
        <div class="insight">

            <div class="insight-label">
                Species Signal
            </div>

            <div class="insight-title">
                No recorded status transition
            </div>

            <div class="insight-text">

                No change between consecutive recorded
                conservation-status observations was
                identified for <b>{selected_species}</b>.

            </div>

        </div>
        """
    )


# ============================================================
# STATUS TRANSITION FLOW
# ============================================================

st.html(
    """
    <div class="section-label">
        Conservation Dynamics
    </div>

    <div class="section-title">
        Conservation Status Flow
    </div>

    <div class="section-description">

        This flow diagram shows the direction and frequency
        of recorded transitions between conservation-status
        categories.

    </div>
    """
)


if transition_records:

    transition_df = pd.DataFrame(
        transition_records
    )


    flow_counts = (

        transition_df
        .groupby(
            [
                "From",
                "To"
            ]
        )
        .size()
        .reset_index(
            name="Count"
        )

    )


    # --------------------------------------------------------
    # REMOVE SELF-TRANSITIONS
    # --------------------------------------------------------

    flow_counts = flow_counts[
        flow_counts["From"]
        != flow_counts["To"]
    ]


    if not flow_counts.empty:

        nodes = sorted(
            set(
                flow_counts["From"]
            )
            |
            set(
                flow_counts["To"]
            )
        )


        node_index = {
            node: i
            for i, node
            in enumerate(nodes)
        }


        sources = [
            node_index[x]
            for x in flow_counts["From"]
        ]


        targets = [
            node_index[x]
            for x in flow_counts["To"]
        ]


        values = (
            flow_counts["Count"]
            .tolist()
        )


        sankey = go.Figure(

            go.Sankey(

                arrangement="snap",

                node=dict(

                    pad=18,

                    thickness=22,

                    line=dict(
                        color="white",
                        width=1
                    ),

                    label=nodes,

                    color="#2E6B45"

                ),

                link=dict(

                    source=sources,

                    target=targets,

                    value=values,

                    color="rgba(46,107,69,0.35)"

                )

            )

        )


        sankey.update_layout(

            height=550,

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20
            ),

            paper_bgcolor="white",

            font=dict(
                family="Arial",
                color="#5F6D64"
            )

        )


        st.plotly_chart(

            sankey,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


    else:

        st.info(
            "No cross-category transitions are available "
            "for the flow diagram."
        )

else:

    st.info(
        "No recorded conservation-status transitions "
        "were identified."
    )


# ============================================================
# SPECIES COMPARISON
# ============================================================

st.html(
    """
    <div class="section-label">
        Species Comparison
    </div>

    <div class="section-title">
        Species-Level Conservation Signals
    </div>

    <div class="section-description">

        Compare the number of available observations and
        recorded status transitions across the species
        represented in the dataset.

    </div>
    """
)


comparison_records = []


for species in species_list:

    temp = history[
        history[SPECIES] == species
    ].sort_values(YEAR)


    transitions_for_species = 0


    if len(temp) >= 2:

        for i in range(
            1,
            len(temp)
        ):

            if (
                str(
                    temp.iloc[i - 1][STATUS]
                )
                !=
                str(
                    temp.iloc[i][STATUS]
                )
            ):

                transitions_for_species += 1


    latest = temp.iloc[-1][STATUS]

    comparison_records.append(

        {
            "Species": species,

            "Observations": len(temp),

            "Transitions": transitions_for_species,

            "Latest Status": latest

        }

    )


comparison_df = pd.DataFrame(
    comparison_records
)


comparison_df = comparison_df.sort_values(
    "Transitions",
    ascending=False
)


fig_species_compare = go.Figure()


fig_species_compare.add_trace(

    go.Bar(

        name="Status transitions",

        x=comparison_df["Species"],

        y=comparison_df["Transitions"],

        marker_color="#2E6B45",

        hovertemplate=
            "<b>%{x}</b><br>"
            "Transitions: %{y}"
            "<extra></extra>"

    )

)


fig_species_compare.update_layout(

    height=470,

    margin=dict(
        l=10,
        r=20,
        t=25,
        b=100
    ),

    paper_bgcolor="white",

    plot_bgcolor="white",

    font=dict(
        family="Arial",
        color="#5F6D64"
    ),

    xaxis=dict(

        title=None,

        tickangle=-55,

        showgrid=False

    ),

    yaxis=dict(

        title="Recorded status transitions",

        gridcolor="#E8E8E2",

        zeroline=False

    )

)


st.plotly_chart(

    fig_species_compare,

    use_container_width=True,

    config={
        "displayModeBar": False
    }

)


# ============================================================
# SPECIES COMPARISON TABLE
# ============================================================

with st.expander(
    "View species comparison table"
):

    st.dataframe(

        comparison_df,

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# PREPARED TREND DATASET
# ============================================================

if not trends.empty:

    trend_column = None

    possible_trend_columns = [

        "trend",

        "Trend",

        "status_trend",

        "Status_Trend",

        "conservation_trend",

        "Conservation_Trend",

        "direction",

        "Direction"

    ]


    for column in possible_trend_columns:

        if column in trends.columns:

            trend_column = column

            break


    if trend_column is not None:

        st.html(
            """
            <div class="section-label">
                Prepared Analysis
            </div>

            <div class="section-title">
                Conservation Trend Categories
            </div>

            <div class="section-description">

                Summary of the trend categories contained
                in the prepared species-trend dataset.

            </div>
            """
        )


        trend_counts = (

            trends[trend_column]
            .astype(str)
            .value_counts()
            .reset_index()

        )


        trend_counts.columns = [
            "Trend",
            "Species Count"
        ]


        fig_trend = px.bar(

            trend_counts,

            x="Species Count",

            y="Trend",

            orientation="h"

        )


        fig_trend.update_traces(

            marker_color="#A0802E",

            hovertemplate=
                "<b>%{y}</b><br>"
                "Species: %{x}"
                "<extra></extra>"

        )


        fig_trend.update_layout(

            height=330,

            margin=dict(
                l=10,
                r=20,
                t=10,
                b=10
            ),

            paper_bgcolor="white",

            plot_bgcolor="white",

            font=dict(
                family="Arial",
                color="#5F6D64"
            ),

            xaxis=dict(
                title="Species count",
                gridcolor="#E8E8E2",
                zeroline=False
            ),

            yaxis=dict(
                title=None,
                autorange="reversed",
                showgrid=False
            )

        )


        st.plotly_chart(

            fig_trend,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


# ============================================================
# INTERPRETATION NOTE
# ============================================================

st.html(
    """
    <div class="validation">

        <div class="validation-title">
            Important Interpretation Note
        </div>

        <div class="validation-text">

            This module describes conservation-status
            patterns and recorded transitions contained
            in the prepared species datasets. A recorded
            status change should not automatically be
            interpreted as being caused by tree-cover loss.
            Establishing causation would require additional
            information such as species geographic ranges,
            habitat exposure and other ecological variables.

        </div>

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        <b>Western Ghats Sentinel</b>

        &nbsp;•&nbsp;

        Tree Cover • Carbon • Conservation

        <br>

        Conservation Intelligence Module

    </div>
    """
)