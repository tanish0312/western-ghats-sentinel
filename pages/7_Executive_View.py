import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Executive View | Western Ghats Sentinel",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

annual = pd.read_csv(
    "data/ANNUAL_TREE_COVER_LOSS.csv"
)

state = pd.read_csv(
    "data/FINAL_STATE_ANALYSIS.csv"
)

species_history = pd.read_csv(
    "data/SPECIES_STATUS_HISTORY.csv"
)

species_trends = pd.read_csv(
    "data/SPECIES_STATUS_TRENDS.csv"
)


# ============================================================
# HELPER
# ============================================================

def find_column(df, possible_names):

    lookup = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in possible_names:

        if name.lower() in lookup:
            return lookup[name.lower()]

    return None


# ============================================================
# IDENTIFY ANNUAL COLUMNS
# ============================================================

year_col = find_column(
    annual,
    [
        "year"
    ]
)

loss_col = find_column(
    annual,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "loss_ha",
        "total_loss"
    ]
)

emission_col = find_column(
    annual,
    [
        "total_emissions_Mg",
        "total_emissions_mg",
        "emissions_Mg",
        "emissions_mg"
    ]
)


# ============================================================
# IDENTIFY STATE COLUMNS
# ============================================================

state_col = find_column(
    state,
    [
        "state",
        "state_name"
    ]
)

state_loss_col = find_column(
    state,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "loss_ha",
        "total_loss"
    ]
)

state_intensity_col = find_column(
    state,
    [
        "loss_per_1000km2",
        "loss_per_1000_km2",
        "loss_intensity"
    ]
)

state_emission_col = find_column(
    state,
    [
        "total_emissions_Mg",
        "total_emissions_mg",
        "emissions_Mg",
        "emissions_mg"
    ]
)


# ============================================================
# PREPARE ANNUAL DATA
# ============================================================

annual_clean = pd.DataFrame()

if (
    year_col is not None
    and loss_col is not None
):

    annual_clean = pd.DataFrame({

        "year":
            pd.to_numeric(
                annual[year_col],
                errors="coerce"
            ),

        "loss":
            pd.to_numeric(
                annual[loss_col],
                errors="coerce"
            )

    })

    if emission_col is not None:

        annual_clean["emissions"] = pd.to_numeric(
            annual[emission_col],
            errors="coerce"
        )

    annual_clean = (
        annual_clean
        .dropna(subset=["year", "loss"])
        .sort_values("year")
    )


# ============================================================
# PREPARE STATE DATA
# ============================================================

state_clean = pd.DataFrame()

if (
    state_col is not None
    and state_loss_col is not None
):

    state_clean = pd.DataFrame({

        "state":
            state[state_col].astype(str),

        "loss":
            pd.to_numeric(
                state[state_loss_col],
                errors="coerce"
            )
    })

    if state_intensity_col is not None:

        state_clean["intensity"] = pd.to_numeric(
            state[state_intensity_col],
            errors="coerce"
        )

    if state_emission_col is not None:

        state_clean["emissions"] = pd.to_numeric(
            state[state_emission_col],
            errors="coerce"
        )

    state_clean = state_clean.dropna(
        subset=["state", "loss"]
    )


# ============================================================
# SPECIES DATA
# ============================================================

species_col = find_column(
    species_history,
    [
        "species",
        "species_name"
    ]
)

status_col = find_column(
    species_history,
    [
        "status",
        "conservation_status",
        "latest_status"
    ]
)

if species_col is not None:

    species_count = (
        species_history[species_col]
        .dropna()
        .nunique()
    )

else:

    species_count = 0


# ============================================================
# CALCULATE EXECUTIVE FINDINGS
# ============================================================

total_loss = annual_clean["loss"].sum()

average_loss = annual_clean["loss"].mean()

number_of_states = len(state_clean)


if not annual_clean.empty:

    start_year = int(
        annual_clean["year"].min()
    )

    end_year = int(
        annual_clean["year"].max()
    )

    peak_row = annual_clean.loc[
        annual_clean["loss"].idxmax()
    ]

    peak_year = int(
        peak_row["year"]
    )

    peak_loss = peak_row["loss"]

else:

    start_year = "—"
    end_year = "—"
    peak_year = "—"
    peak_loss = 0


# ============================================================
# HIGHEST LOSS STATE
# ============================================================

if not state_clean.empty:

    highest_loss_row = state_clean.loc[
        state_clean["loss"].idxmax()
    ]

    highest_loss_state = (
        highest_loss_row["state"]
    )

    highest_loss_value = (
        highest_loss_row["loss"]
    )

else:

    highest_loss_state = "—"
    highest_loss_value = 0


# ============================================================
# HIGHEST INTENSITY STATE
# ============================================================

if (
    "intensity" in state_clean.columns
    and
    state_clean["intensity"].notna().any()
):

    intensity_data = state_clean.dropna(
        subset=["intensity"]
    )

    intensity_row = intensity_data.loc[
        intensity_data["intensity"].idxmax()
    ]

    highest_intensity_state = (
        intensity_row["state"]
    )

    highest_intensity_value = (
        intensity_row["intensity"]
    )

else:

    highest_intensity_state = "—"
    highest_intensity_value = None


# ============================================================
# HIGHEST EMISSION STATE
# ============================================================

if (
    "emissions" in state_clean.columns
    and
    state_clean["emissions"].notna().any()
):

    emission_data = state_clean.dropna(
        subset=["emissions"]
    )

    emission_row = emission_data.loc[
        emission_data["emissions"].idxmax()
    ]

    highest_emission_state = (
        emission_row["state"]
    )

    highest_emission_value = (
        emission_row["emissions"]
    )

else:

    highest_emission_state = "—"
    highest_emission_value = None


# ============================================================
# CORRELATION
# ============================================================

correlation = None

if (
    "emissions" in annual_clean.columns
):

    corr_data = annual_clean.dropna(
        subset=[
            "loss",
            "emissions"
        ]
    )

    if len(corr_data) >= 3:

        correlation = corr_data[
            "loss"
        ].corr(
            corr_data[
                "emissions"
            ],
            method="spearman"
        )


# ============================================================
# STATUS DISTRIBUTION
# ============================================================

status_summary = pd.DataFrame()

if (
    status_col is not None
):

    status_summary = (
        species_history[
            status_col
        ]
        .dropna()
        .astype(str)
        .value_counts()
        .reset_index()
    )

    status_summary.columns = [
        "status",
        "count"
    ]


# ============================================================
# CSS
# ============================================================

st.html("""
<style>

.exec-hero {

    padding: 48px 52px;

    border-radius: 25px;

    background:
        linear-gradient(
            135deg,
            #062f24,
            #0d503a 55%,
            #217452
        );

    color: white;

    margin-bottom: 28px;

    box-shadow:
        0 16px 40px
        rgba(5,45,34,0.18);
}


.exec-kicker {

    color: #dcc66d;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 3px;
}


.exec-title {

    font-size: 46px;

    font-weight: 850;

    line-height: 1.05;

    margin-top: 10px;
}


.exec-subtitle {

    max-width: 900px;

    color: #e3eee9;

    font-size: 17px;

    line-height: 1.7;

    margin-top: 14px;
}


.exec-period {

    display: inline-block;

    margin-top: 18px;

    padding: 8px 15px;

    border-radius: 20px;

    background:
        rgba(220,198,109,0.15);

    border:
        1px solid
        rgba(220,198,109,0.35);

    color: #e6d57e;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.8px;
}


.section-kicker {

    color: #ad9142;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 2.5px;

    margin-top: 35px;
}


.section-title {

    color: #123d30;

    font-size: 28px;

    font-weight: 800;

    margin-top: 5px;

    margin-bottom: 8px;
}


.section-description {

    color: #66746d;

    line-height: 1.7;

    margin-bottom: 20px;
}


.big-card {

    background: white;

    border:
        1px solid #e0e8e4;

    border-radius: 17px;

    padding: 22px;

    min-height: 130px;

    box-shadow:
        0 6px 20px
        rgba(20,60,48,0.055);
}


.big-label {

    color: #9b8141;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.5px;
}


.big-value {

    color: #103d30;

    font-size: 30px;

    font-weight: 850;

    margin-top: 7px;
}


.big-description {

    color: #718078;

    font-size: 12px;

    margin-top: 4px;

    line-height: 1.5;
}


.signal {

    background: white;

    border:
        1px solid #e0e8e4;

    border-radius: 18px;

    padding: 25px;

    min-height: 230px;

    box-shadow:
        0 7px 23px
        rgba(20,60,48,0.055);
}


.signal-icon {

    font-size: 28px;

    margin-bottom: 12px;
}


.signal-label {

    color: #9b8141;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.6px;
}


.signal-title {

    color: #123d30;

    font-size: 22px;

    font-weight: 850;

    margin-top: 7px;
}


.signal-text {

    color: #66746d;

    line-height: 1.65;

    font-size: 13px;

    margin-top: 9px;
}


.takeaway {

    background:
        linear-gradient(
            135deg,
            #eef7f3,
            #f7faf8
        );

    border-left:
        5px solid #2f6f5e;

    border-radius: 13px;

    padding: 26px 29px;

    line-height: 1.8;

    color: #294c40;
}


.method-note {

    background: #fff8df;

    border-left:
        5px solid #c9a33e;

    border-radius: 12px;

    padding: 23px 27px;

    color: #5c4a17;

    line-height: 1.7;
}


.footer {

    margin-top: 55px;

    padding: 25px 0;

    border-top:
        1px solid #e1e8e4;

    color: #718078;

    font-size: 13px;
}

</style>
""")


# ============================================================
# HERO
# ============================================================

st.html(
    f"""
    <div class="exec-hero">

        <div class="exec-kicker">
            EXECUTIVE ENVIRONMENTAL VIEW
        </div>

        <div class="exec-title">
            Western Ghats Sentinel
        </div>

        <div class="exec-subtitle">
            A presentation-ready synthesis of tree-cover
            change, carbon indicators, spatial variation
            and conservation patterns across the
            Western Ghats study region.
        </div>

        <div class="exec-period">
            {start_year}–{end_year}
            &nbsp; • &nbsp;
            {number_of_states} STATES
            &nbsp; • &nbsp;
            TREE COVER • CARBON • CONSERVATION
        </div>

    </div>
    """
)


# ============================================================
# REGION AT A GLANCE
# ============================================================

st.markdown(
    '<div class="section-kicker">REGION AT A GLANCE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">The project in numbers</div>',
    unsafe_allow_html=True
)


a1, a2, a3, a4 = st.columns(4)


with a1:

    st.html(
        f"""
        <div class="big-card">

            <div class="big-label">
                TREE-COVER LOSS
            </div>

            <div class="big-value">
                {total_loss:,.0f} ha
            </div>

            <div class="big-description">
                Total recorded annual loss
                across the study period.
            </div>

        </div>
        """
    )


with a2:

    st.html(
        f"""
        <div class="big-card">

            <div class="big-label">
                STUDY STATES
            </div>

            <div class="big-value">
                {number_of_states}
            </div>

            <div class="big-description">
                States represented in the
                spatial analysis.
            </div>

        </div>
        """
    )


with a3:

    st.html(
        f"""
        <div class="big-card">

            <div class="big-label">
                SPECIES
            </div>

            <div class="big-value">
                {species_count}
            </div>

            <div class="big-description">
                Species represented in the
                conservation dataset.
            </div>

        </div>
        """
    )


with a4:

    st.html(
        f"""
        <div class="big-card">

            <div class="big-label">
                PEAK LOSS YEAR
            </div>

            <div class="big-value">
                {peak_year}
            </div>

            <div class="big-description">
                {peak_loss:,.0f} ha recorded
                during the peak year.
            </div>

        </div>
        """
    )


# ============================================================
# FOUR ENVIRONMENTAL SIGNALS
# ============================================================

st.markdown(
    '<div class="section-kicker">FOUR ENVIRONMENTAL SIGNALS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">What matters most in the data?</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# SIGNAL 1 + 2
# ------------------------------------------------------------

s1, s2 = st.columns(2)


with s1:

    st.html(
        f"""
        <div class="signal">

            <div class="signal-icon">
                🌲
            </div>

            <div class="signal-label">
                FOREST LOSS
            </div>

            <div class="signal-title">
                {highest_loss_state}
            </div>

            <div class="signal-text">

                This state records the highest
                cumulative tree-cover loss in
                the state-level dataset.

                <br><br>

                <b>
                {highest_loss_value:,.0f} hectares
                </b>

                of recorded loss.

            </div>

        </div>
        """
    )


with s2:

    emission_value_text = (
        f"{highest_emission_value:,.0f} Mg"
        if highest_emission_value is not None
        else "Not available"
    )

    st.html(
        f"""
        <div class="signal">

            <div class="signal-icon">
                💨
            </div>

            <div class="signal-label">
                CARBON
            </div>

            <div class="signal-title">
                {highest_emission_state}
            </div>

            <div class="signal-text">

                This state has the highest
                recorded total CO₂ emissions
                in the state-level analysis.

                <br><br>

                <b>
                {emission_value_text}
                </b>

            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# SIGNAL 3 + 4
# ------------------------------------------------------------

s3, s4 = st.columns(2)


with s3:

    intensity_value_text = (
        f"{highest_intensity_value:,.2f} ha / 1,000 km²"
        if highest_intensity_value is not None
        else "Not available"
    )

    st.html(
        f"""
        <div class="signal">

            <div class="signal-icon">
                🗺️
            </div>

            <div class="signal-label">
                SPATIAL INTENSITY
            </div>

            <div class="signal-title">
                {highest_intensity_state}
            </div>

            <div class="signal-text">

                Area-normalized analysis identifies
                this state as having the highest
                tree-cover-loss intensity.

                <br><br>

                <b>
                {intensity_value_text}
                </b>

            </div>

        </div>
        """
    )


with s4:

    correlation_text = (
        f"{correlation:.3f}"
        if correlation is not None
        else "—"
    )

    st.html(
        f"""
        <div class="signal">

            <div class="signal-icon">
                🔗
            </div>

            <div class="signal-label">
                ENVIRONMENTAL RELATIONSHIP
            </div>

            <div class="signal-title">
                ρ = {correlation_text}
            </div>

            <div class="signal-text">

                Spearman correlation between
                annual tree-cover loss and
                CO₂ emissions.

                <br><br>

                This describes statistical
                association, not causation.

            </div>

        </div>
        """
    )


# ============================================================
# FOREST LOSS TREND
# ============================================================

st.markdown(
    '<div class="section-kicker">FOREST LOSS TRAJECTORY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Annual tree-cover loss</div>',
    unsafe_allow_html=True
)


annual_chart = px.area(

    annual_clean,

    x="year",

    y="loss",

    labels={
        "year": "Year",
        "loss": "Tree-cover loss (ha)"
    }
)


annual_chart.update_layout(

    template="plotly_white",

    height=390,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=25
    ),

    hovermode="x unified"
)


annual_chart.update_traces(
    hovertemplate=
    "<b>%{x}</b><br>"
    "Loss: %{y:,.0f} ha"
    "<extra></extra>"
)


st.plotly_chart(
    annual_chart,
    use_container_width=True
)


# ============================================================
# STATE COMPARISON
# ============================================================

st.markdown(
    '<div class="section-kicker">SPATIAL DISTRIBUTION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">How the states compare</div>',
    unsafe_allow_html=True
)


state_chart = px.bar(

    state_clean.sort_values(
        "loss",
        ascending=True
    ),

    x="loss",

    y="state",

    orientation="h",

    labels={
        "loss":
            "Tree-cover loss (ha)",

        "state":
            ""
    }
)


state_chart.update_layout(

    template="plotly_white",

    height=390,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=25
    )
)


st.plotly_chart(
    state_chart,
    use_container_width=True
)


# ============================================================
# CONSERVATION SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-kicker">CONSERVATION CONTEXT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Species-status snapshot</div>',
    unsafe_allow_html=True
)


if not status_summary.empty:

    left, right = st.columns(
        [1.35, 1]
    )


    with left:

        status_chart = px.bar(

            status_summary,

            x="count",

            y="status",

            orientation="h",

            labels={
                "count":
                    "Records",

                "status":
                    ""
            }
        )


        status_chart.update_layout(

            template="plotly_white",

            height=350,

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )


        st.plotly_chart(
            status_chart,
            use_container_width=True
        )


    with right:

        st.html(
            f"""
            <div class="signal">

                <div class="signal-icon">
                    🐘
                </div>

                <div class="signal-label">
                    CONSERVATION DATASET
                </div>

                <div class="signal-title">
                    {species_count} species
                </div>

                <div class="signal-text">

                    The conservation dataset provides
                    historical and/or latest species-status
                    information used by the Conservation
                    analysis.

                    <br><br>

                    Species-status patterns are presented
                    separately from the forest-loss analysis
                    unless comparable observations support
                    a statistical relationship.

                </div>

            </div>
            """
        )


else:

    st.info(
        "Species-status information is available on "
        "the Conservation page."
    )


# ============================================================
# THE ENVIRONMENTAL STORY
# ============================================================

st.markdown(
    '<div class="section-kicker">THE ENVIRONMENTAL STORY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Putting the evidence together</div>',
    unsafe_allow_html=True
)


st.html(
    f"""
    <div class="takeaway">

    <b>01 — Forest change</b>

    <br>

    The study records approximately
    <b>{total_loss:,.0f} hectares</b>
    of tree-cover loss across the available annual series,
    with the highest annual loss occurring in
    <b>{peak_year}</b>.

    <br><br>

    <b>02 — Spatial variation</b>

    <br>

    Tree-cover loss is not evenly distributed across the
    five-state study region. The state with the highest
    cumulative recorded loss is
    <b>{highest_loss_state}</b>.

    <br><br>

    <b>03 — Carbon relationship</b>

    <br>

    The available annual data shows a
    <b>{correlation:.3f}</b> Spearman association between
    tree-cover loss and CO₂ emissions.
    This is a statistical relationship in the dataset,
    rather than evidence of causation.

    <br><br>

    <b>04 — Conservation context</b>

    <br>

    Species-status information provides an additional
    conservation perspective and is examined separately
    through the Conservation analysis.

    </div>
    """
)


# ============================================================
# METHODOLOGICAL BOUNDARY
# ============================================================

st.markdown(
    '<div class="section-kicker">RESEARCH BOUNDARY</div>',
    unsafe_allow_html=True
)

st.html(
    """
    <div class="method-note">

    <b>How to interpret this executive view</b>

    <br><br>

    This page summarizes observed patterns and statistical
    associations in the project datasets.

    <br><br>

    Correlation does not establish causation. In particular,
    the available species-status data should not be interpreted
    as proof that tree-cover loss caused changes in species
    conservation status.

    <br><br>

    State-level tree-cover-loss values also represent
    state-level patterns and should not be interpreted as
    district-level measurements.

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        <b>Western Ghats Sentinel</b><br>

        Executive Environmental View ·
        Tree Cover · Carbon · Conservation

    </div>
    """
)