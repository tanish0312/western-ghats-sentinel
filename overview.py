import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Western Ghats Sentinel",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
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


# ============================================================
# HELPER
# ============================================================

def find_column(df, names):

    lookup = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in names:

        if name.lower() in lookup:
            return lookup[name.lower()]

    return None


def money_number(value):

    if pd.isna(value):
        return "—"

    return f"{value:,.0f}"


# ============================================================
# IDENTIFY ANNUAL COLUMNS
# ============================================================

annual_year_col = find_column(
    annual,
    [
        "year"
    ]
)

annual_loss_col = find_column(
    annual,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "loss_ha"
    ]
)

annual_emission_col = find_column(
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

state_name_col = find_column(
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
        "loss_ha"
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
    annual_year_col is not None
    and annual_loss_col is not None
):

    annual_clean = pd.DataFrame({

        "year":
            pd.to_numeric(
                annual[annual_year_col],
                errors="coerce"
            ),

        "loss":
            pd.to_numeric(
                annual[annual_loss_col],
                errors="coerce"
            )
    })

    if annual_emission_col is not None:

        annual_clean["emissions"] = pd.to_numeric(
            annual[annual_emission_col],
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
    state_name_col is not None
    and state_loss_col is not None
):

    state_clean = pd.DataFrame({

        "state":
            state[state_name_col].astype(str),

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
# CALCULATE KEY FINDINGS
# ============================================================

total_loss = annual_clean["loss"].sum()

average_annual_loss = annual_clean["loss"].mean()

peak_year_row = annual_clean.loc[
    annual_clean["loss"].idxmax()
]

peak_year = int(
    peak_year_row["year"]
)

peak_year_loss = peak_year_row["loss"]


# ------------------------------------------------------------
# YEAR-ON-YEAR CHANGE
# ------------------------------------------------------------

annual_clean["change"] = (
    annual_clean["loss"].pct_change()
    * 100
)

change_data = annual_clean.dropna(
    subset=["change"]
)

if not change_data.empty:

    largest_increase_row = change_data.loc[
        change_data["change"].idxmax()
    ]

    largest_decrease_row = change_data.loc[
        change_data["change"].idxmin()
    ]

else:

    largest_increase_row = None
    largest_decrease_row = None


# ------------------------------------------------------------
# HIGHEST LOSS STATE
# ------------------------------------------------------------

highest_loss_state = "—"
highest_loss_state_value = None

if not state_clean.empty:

    row = state_clean.loc[
        state_clean["loss"].idxmax()
    ]

    highest_loss_state = row["state"]

    highest_loss_state_value = row["loss"]


# ------------------------------------------------------------
# HIGHEST INTENSITY STATE
# ------------------------------------------------------------

highest_intensity_state = "—"
highest_intensity_value = None

if (
    "intensity" in state_clean.columns
    and
    state_clean["intensity"].notna().any()
):

    intensity_data = state_clean.dropna(
        subset=["intensity"]
    )

    row = intensity_data.loc[
        intensity_data["intensity"].idxmax()
    ]

    highest_intensity_state = row["state"]

    highest_intensity_value = row["intensity"]


# ------------------------------------------------------------
# HIGHEST EMISSIONS STATE
# ------------------------------------------------------------

highest_emission_state = "—"
highest_emission_value = None

if (
    "emissions" in state_clean.columns
    and
    state_clean["emissions"].notna().any()
):

    emission_data = state_clean.dropna(
        subset=["emissions"]
    )

    row = emission_data.loc[
        emission_data["emissions"].idxmax()
    ]

    highest_emission_state = row["state"]

    highest_emission_value = row["emissions"]


# ------------------------------------------------------------
# LOSS / EMISSIONS CORRELATION
# ------------------------------------------------------------

annual_correlation = None

if (
    "emissions" in annual_clean.columns
    and
    annual_clean["emissions"].notna().sum() >= 3
):

    correlation_data = annual_clean.dropna(
        subset=[
            "loss",
            "emissions"
        ]
    )

    if len(correlation_data) >= 3:

        annual_correlation = correlation_data[
            "loss"
        ].corr(
            correlation_data[
                "emissions"
            ],
            method="spearman"
        )


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

.hero {

    padding: 45px 48px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            #073628 0%,
            #0c4b37 55%,
            #1e7051 100%
        );

    color: white;

    margin-bottom: 30px;

    box-shadow:
        0 15px 35px
        rgba(7,54,40,0.16);
}


.hero-kicker {

    color: #dcc66d;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 3px;

    margin-bottom: 13px;
}


.hero-title {

    font-size: 48px;

    font-weight: 850;

    line-height: 1.02;

    margin: 0;
}


.hero-subtitle {

    font-size: 17px;

    color: #e4efea;

    line-height: 1.7;

    max-width: 850px;

    margin-top: 15px;
}


.hero-tag {

    display: inline-block;

    margin-top: 18px;

    padding: 7px 14px;

    border-radius: 20px;

    background: rgba(220,198,109,0.16);

    border: 1px solid rgba(220,198,109,0.35);

    color: #e4d47d;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.7px;
}


.section-kicker {

    color: #ad9142;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 2.4px;

    margin-top: 38px;
}


.section-title {

    color: #123d30;

    font-size: 28px;

    font-weight: 800;

    margin-top: 5px;

    margin-bottom: 8px;
}


.section-text {

    color: #66746d;

    line-height: 1.7;

    margin-bottom: 20px;
}


.kpi-card {

    background: white;

    border:
        1px solid #e1e8e4;

    border-radius: 16px;

    padding: 22px;

    min-height: 130px;

    box-shadow:
        0 5px 18px
        rgba(20,60,48,0.05);
}


.kpi-label {

    color: #9a8141;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.6px;
}


.kpi-value {

    color: #103d30;

    font-size: 29px;

    font-weight: 850;

    margin-top: 7px;
}


.kpi-description {

    color: #718078;

    font-size: 12px;

    margin-top: 5px;

    line-height: 1.5;
}


.finding-card {

    background: white;

    border: 1px solid #e1e8e4;

    border-radius: 18px;

    padding: 25px;

    min-height: 235px;

    box-shadow:
        0 7px 22px
        rgba(20,60,48,0.06);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.finding-icon {

    font-size: 28px;

    margin-bottom: 14px;
}


.finding-label {

    color: #9a8141;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.7px;
}


.finding-value {

    color: #103d30;

    font-size: 23px;

    font-weight: 850;

    margin-top: 7px;

    line-height: 1.25;
}


.finding-description {

    color: #65736c;

    font-size: 13px;

    line-height: 1.6;

    margin-top: 10px;
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

    padding: 25px 28px;

    margin-top: 20px;

    color: #294c40;

    line-height: 1.8;
}


.source-note {

    color: #7a8781;

    font-size: 12px;

    margin-top: 8px;
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

st.html("""
<div class="hero">

    <div class="hero-kicker">
        ENVIRONMENTAL INTELLIGENCE DASHBOARD
    </div>

    <div class="hero-title">
        Western Ghats Sentinel
    </div>

    <div class="hero-subtitle">
        An interactive research dashboard exploring
        tree-cover loss, carbon emissions and conservation
        patterns across the Western Ghats study region.
    </div>

    <div class="hero-tag">
        TREE COVER • CARBON • CONSERVATION
    </div>

</div>
""")


# ============================================================
# EXECUTIVE KPI STRIP
# ============================================================

st.markdown(
    '<div class="section-kicker">AT A GLANCE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">The region in numbers</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


with k1:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                TOTAL TREE-COVER LOSS
            </div>

            <div class="kpi-value">
                {total_loss:,.0f} ha
            </div>

            <div class="kpi-description">
                Combined loss recorded across
                the annual study series.
            </div>

        </div>
        """
    )


with k2:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                STUDY STATES
            </div>

            <div class="kpi-value">
                {len(state_clean)}
            </div>

            <div class="kpi-description">
                States included in the
                Western Ghats study region.
            </div>

        </div>
        """
    )


with k3:

    if not annual_clean.empty:

        start_year = int(
            annual_clean["year"].min()
        )

        end_year = int(
            annual_clean["year"].max()
        )

        period = f"{start_year}–{end_year}"

    else:

        period = "—"


    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                ANALYSIS PERIOD
            </div>

            <div class="kpi-value">
                {period}
            </div>

            <div class="kpi-description">
                Annual tree-cover-loss
                observation period.
            </div>

        </div>
        """
    )


with k4:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                ANNUAL AVERAGE
            </div>

            <div class="kpi-value">
                {average_annual_loss:,.0f} ha
            </div>

            <div class="kpi-description">
                Average tree-cover loss
                per recorded year.
            </div>

        </div>
        """
    )


# ============================================================
# KEY FINDINGS
# ============================================================

st.markdown(
    '<div class="section-kicker">AUTOMATED RESEARCH FINDINGS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">What stands out in the data?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
These findings are calculated directly from the project's
underlying datasets. They update automatically when the data
changes.
""",
    unsafe_allow_html=True
)


# ============================================================
# FINDING CARDS — ROW 1
# ============================================================

f1, f2, f3 = st.columns(3)


with f1:

    st.html(
        f"""
        <div class="finding-card">

            <div class="finding-icon">
                🌲
            </div>

            <div class="finding-label">
                PEAK LOSS YEAR
            </div>

            <div class="finding-value">
                {peak_year}
            </div>

            <div class="finding-description">
                The highest annual tree-cover
                loss recorded was
                <b>{peak_year_loss:,.0f} ha</b>.
            </div>

            <div class="source-note">
                Source: ANNUAL_TREE_COVER_LOSS.csv
            </div>

        </div>
        """
    )


with f2:

    st.html(
        f"""
        <div class="finding-card">

            <div class="finding-icon">
                🗺️
            </div>

            <div class="finding-label">
                HIGHEST TOTAL LOSS
            </div>

            <div class="finding-value">
                {highest_loss_state}
            </div>

            <div class="finding-description">
                This state has the highest
                recorded cumulative tree-cover
                loss among the study states.

                <br><br>

                <b>
                {highest_loss_state_value:,.0f} ha
                </b>
            </div>

            <div class="source-note">
                Source: FINAL_STATE_ANALYSIS.csv
            </div>

        </div>
        """
    )


with f3:

    intensity_text = (
        f"{highest_intensity_value:,.2f} ha / 1,000 km²"
        if highest_intensity_value is not None
        else "Not available"
    )

    st.html(
        f"""
        <div class="finding-card">

            <div class="finding-icon">
                📍
            </div>

            <div class="finding-label">
                HIGHEST LOSS INTENSITY
            </div>

            <div class="finding-value">
                {highest_intensity_state}
            </div>

            <div class="finding-description">
                Highest tree-cover loss relative
                to state area.

                <br><br>

                <b>{intensity_text}</b>
            </div>

            <div class="source-note">
                Area-normalized indicator
            </div>

        </div>
        """
    )


# ============================================================
# FINDING CARDS — ROW 2
# ============================================================

f4, f5, f6 = st.columns(3)


with f4:

    emission_text = (
        f"{highest_emission_value:,.0f} Mg"
        if highest_emission_value is not None
        else "Not available"
    )

    st.html(
        f"""
        <div class="finding-card">

            <div class="finding-icon">
                💨
            </div>

            <div class="finding-label">
                HIGHEST CO₂ EMISSIONS
            </div>

            <div class="finding-value">
                {highest_emission_state}
            </div>

            <div class="finding-description">
                Highest recorded total CO₂
                emissions among the study states.

                <br><br>

                <b>{emission_text}</b>
            </div>

            <div class="source-note">
                Source: FINAL_STATE_ANALYSIS.csv
            </div>

        </div>
        """
    )


with f5:

    if annual_correlation is not None:

        correlation_text = (
            f"{annual_correlation:.3f}"
        )

        correlation_description = (
            "Spearman rank association between "
            "annual tree-cover loss and emissions."
        )

    else:

        correlation_text = "—"

        correlation_description = (
            "Annual emissions data unavailable "
            "for correlation."
        )


    st.html(
        f"""
        <div class="finding-card">

            <div class="finding-icon">
                🔗
            </div>

            <div class="finding-label">
                LOSS ↔ EMISSIONS
            </div>

            <div class="finding-value">
                ρ = {correlation_text}
            </div>

            <div class="finding-description">
                {correlation_description}
            </div>

            <div class="source-note">
                Statistical association, not causation.
            </div>

        </div>
        """
    )


with f6:

    if largest_increase_row is not None:

        increase_year = int(
            largest_increase_row["year"]
        )

        increase_value = (
            largest_increase_row["change"]
        )

        change_text = (
            f"+{increase_value:.1f}%"
        )

        change_description = (
            f"Largest year-on-year increase "
            f"occurred in {increase_year}."
        )

    else:

        change_text = "—"

        change_description = (
            "Year-on-year change could not "
            "be calculated."
        )


    st.html(
        f"""
        <div class="finding-card">

            <div class="finding-icon">
                📈
            </div>

            <div class="finding-label">
                LARGEST ANNUAL INCREASE
            </div>

            <div class="finding-value">
                {change_text}
            </div>

            <div class="finding-description">
                {change_description}
            </div>

            <div class="source-note">
                Based on annual percentage change.
            </div>

        </div>
        """
    )


# ============================================================
# RESEARCH TAKEAWAY
# ============================================================

st.markdown(
    '<div class="section-kicker">RESEARCH TAKEAWAY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">What does the combined evidence show?</div>',
    unsafe_allow_html=True
)


if annual_correlation is not None:

    correlation_sentence = (
        f"The annual tree-cover-loss and CO₂-emissions "
        f"series show a Spearman association of "
        f"{annual_correlation:.3f}."
    )

else:

    correlation_sentence = (
        "A comparable annual loss–emissions correlation "
        "could not be calculated from the available data."
    )


st.html(
    f"""
    <div class="takeaway">

    <b>Western Ghats Sentinel brings together three
    analytical perspectives:</b>

    <br><br>

    <b>1. Temporal change</b> — annual tree-cover loss
    reveals how the forest-loss pattern changes over time.

    <br><br>

    <b>2. Spatial variation</b> — state-level analysis shows
    that the magnitude and intensity of loss are not uniform
    across the study region.

    <br><br>

    <b>3. Environmental relationships</b> —
    {correlation_sentence}

    <br><br>

    Together, these analyses provide a structured view of
    tree-cover change, carbon-related indicators and
    conservation patterns across the Western Ghats study region.

    </div>
    """
)


# ============================================================
# ANNUAL TREND
# ============================================================

st.markdown(
    '<div class="section-kicker">TEMPORAL PATTERN</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Tree-cover loss through time</div>',
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


annual_chart.update_traces(
    hovertemplate=
    "<b>%{x}</b><br>"
    "Tree-cover loss: %{y:,.0f} ha"
    "<extra></extra>"
)


annual_chart.update_layout(

    template="plotly_white",

    height=470,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=25
    ),

    hovermode="x unified"
)


st.plotly_chart(
    annual_chart,
    use_container_width=True
)


# ============================================================
# STATE COMPARISON
# ============================================================

st.markdown(
    '<div class="section-kicker">SPATIAL PATTERN</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Tree-cover loss by state</div>',
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
        "loss": "Tree-cover loss (ha)",
        "state": ""
    }
)


state_chart.update_layout(

    template="plotly_white",

    height=430,

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
# DATA TRANSPARENCY
# ============================================================

st.markdown(
    '<div class="section-kicker">DATA TRANSPARENCY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">How these findings are generated</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
The Key Findings section is calculated directly from the
project datasets rather than manually entered.

**Annual findings** use `ANNUAL_TREE_COVER_LOSS.csv`.

**State findings** use `FINAL_STATE_ANALYSIS.csv`.

**Relationship findings** use the annual loss and emissions
columns available in the project data.

This allows the dashboard to remain reproducible if the
underlying datasets are updated.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    <b>Western Ghats Sentinel</b><br>

    Tree Cover • Carbon • Conservation

</div>
""")