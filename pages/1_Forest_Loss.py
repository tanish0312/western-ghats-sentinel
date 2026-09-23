import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_loader import (
    load_annual_loss,
    load_state_year_loss,
    load_state_analysis
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Forest Loss | Western Ghats Sentinel",
    page_icon="🌲",
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

    .filter-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E5E0D5;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 25px;
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

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

annual_loss = load_annual_loss()

state_year = load_state_year_loss()

state_analysis = load_state_analysis()


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="page-header">

        <div class="page-label">
            Forest Analysis
        </div>

        <div class="page-title">
            🌲 Forest Loss
        </div>

        <div class="page-description">
            Explore how tree-cover loss has changed over time
            and how the pattern differs across the five
            Western Ghats study states.
        </div>

    </div>
    """
)


# ============================================================
# PREPARE ANNUAL DATA
# ============================================================

annual_chart = annual_loss.copy()


# Convert year to numeric

if "year" in annual_chart.columns:

    annual_chart["year"] = pd.to_numeric(
        annual_chart["year"],
        errors="coerce"
    )


# Find loss column

loss_columns = [
    col
    for col in annual_chart.columns
    if "loss" in col.lower()
]


if loss_columns:

    loss_column = loss_columns[0]

else:

    loss_column = None


# ============================================================
# FILTERS
# ============================================================

st.html(
    """
    <div class="section-title">
        Explore the Data
    </div>

    <div class="section-description">
        Use the filters below to investigate different
        parts of the forest-loss record.
    </div>
    """
)


filter_col1, filter_col2 = st.columns(2)


# ------------------------------------------------------------
# YEAR FILTER
# ------------------------------------------------------------

with filter_col1:

    if "year" in annual_chart.columns:

        valid_years = (
            annual_chart["year"]
            .dropna()
            .astype(int)
            .sort_values()
            .unique()
        )

        if len(valid_years) > 0:

            min_available_year = int(
                valid_years.min()
            )

            max_available_year = int(
                valid_years.max()
            )

            year_range = st.slider(
                "Analysis period",
                min_value=min_available_year,
                max_value=max_available_year,
                value=(
                    min_available_year,
                    max_available_year
                )
            )

        else:

            year_range = None

    else:

        year_range = None


# ------------------------------------------------------------
# STATE FILTER
# ------------------------------------------------------------

with filter_col2:

    if "state" in state_year.columns:

        available_states = sorted(
            state_year["state"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_states = st.multiselect(
            "States",
            options=available_states,
            default=available_states
        )

    else:

        selected_states = []


# ============================================================
# APPLY YEAR FILTER
# ============================================================

if (
    year_range is not None
    and "year" in annual_chart.columns
):

    annual_filtered = annual_chart[
        annual_chart["year"].between(
            year_range[0],
            year_range[1]
        )
    ].copy()

else:

    annual_filtered = annual_chart.copy()


# ============================================================
# ANNUAL LOSS CHART
# ============================================================

st.html(
    """
    <div class="section-title">
        Annual Tree-Cover Loss
    </div>

    <div class="section-description">
        Total recorded tree-cover loss for each year
        in the selected period.
    </div>
    """
)


if (
    loss_column
    and "year" in annual_filtered.columns
):

    annual_filtered = annual_filtered.dropna(
        subset=[
            "year",
            loss_column
        ]
    )

    annual_filtered = annual_filtered.sort_values(
        "year"
    )


    fig = px.area(
        annual_filtered,

        x="year",

        y=loss_column,

        markers=True,

        labels={
            "year": "Year",
            loss_column:
                "Tree-Cover Loss (ha)"
        }
    )


    fig.update_traces(

        hovertemplate=
        "<b>Year:</b> %{x}<br>"
        "<b>Tree-cover loss:</b> %{y:,.2f} ha"
        "<extra></extra>"
    )


    fig.update_layout(

        height=480,

        margin=dict(
            l=20,
            r=20,
            t=25,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            color="#12372A"
        ),

        xaxis=dict(
            title="Year",
            showgrid=False
        ),

        yaxis=dict(
            title="Tree-Cover Loss (ha)",
            showgrid=True,
            gridcolor="#E6E1D8"
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.warning(
        "Annual tree-cover-loss data could not be identified."
    )


# ============================================================
# STATE-YEAR ANALYSIS
# ============================================================

st.html(
    """
    <div class="section-title">
        Tree-Cover Loss by State and Year
    </div>

    <div class="section-description">
        Compare annual tree-cover loss across the
        selected states.
    </div>
    """
)


# ------------------------------------------------------------
# PREPARE STATE-YEAR DATA
# ------------------------------------------------------------

state_year_chart = state_year.copy()


if "year" in state_year_chart.columns:

    state_year_chart["year"] = pd.to_numeric(
        state_year_chart["year"],
        errors="coerce"
    )


# ------------------------------------------------------------
# APPLY STATE FILTER
# ------------------------------------------------------------

if (
    selected_states
    and "state" in state_year_chart.columns
):

    state_year_chart = state_year_chart[
        state_year_chart["state"].isin(
            selected_states
        )
    ]


# ------------------------------------------------------------
# APPLY YEAR FILTER
# ------------------------------------------------------------

if (
    year_range is not None
    and "year" in state_year_chart.columns
):

    state_year_chart = state_year_chart[
        state_year_chart["year"].between(
            year_range[0],
            year_range[1]
        )
    ]


# ------------------------------------------------------------
# FIND LOSS COLUMN
# ------------------------------------------------------------

state_year_loss_columns = [
    col
    for col in state_year_chart.columns
    if "loss" in col.lower()
]


if state_year_loss_columns:

    state_year_loss_column = (
        state_year_loss_columns[0]
    )

else:

    state_year_loss_column = None


# ============================================================
# STATE-YEAR CHART
# ============================================================

if (
    state_year_loss_column
    and "state" in state_year_chart.columns
    and "year" in state_year_chart.columns
):

    state_year_chart = state_year_chart.dropna(
        subset=[
            "state",
            "year",
            state_year_loss_column
        ]
    )


    fig_state_year = px.line(

        state_year_chart,

        x="year",

        y=state_year_loss_column,

        color="state",

        markers=True,

        labels={
            "year": "Year",
            state_year_loss_column:
                "Tree-Cover Loss (ha)",
            "state":
                "State"
        }
    )


    fig_state_year.update_traces(

        hovertemplate=
        "<b>%{fullData.name}</b><br>"
        "Year: %{x}<br>"
        "Loss: %{y:,.2f} ha"
        "<extra></extra>"
    )


    fig_state_year.update_layout(

        height=480,

        margin=dict(
            l=20,
            r=20,
            t=25,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            color="#12372A"
        ),

        xaxis=dict(
            title="Year",
            showgrid=False
        ),

        yaxis=dict(
            title="Tree-Cover Loss (ha)",
            showgrid=True,
            gridcolor="#E6E1D8"
        ),

        legend=dict(
            title="State",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )


    st.plotly_chart(
        fig_state_year,
        use_container_width=True
    )


else:

    st.warning(
        "State-year tree-cover-loss data could not be identified."
    )


# ============================================================
# STATE TOTALS
# ============================================================

st.html(
    """
    <div class="section-title">
        Total Tree-Cover Loss by State
    </div>

    <div class="section-description">
        Total recorded tree-cover loss for each selected state.
    </div>
    """
)


state_totals = state_analysis.copy()


# Find loss column

state_total_loss_columns = [
    col
    for col in state_totals.columns
    if "loss" in col.lower()
]


if state_total_loss_columns:

    state_total_loss_column = (
        state_total_loss_columns[0]
    )

else:

    state_total_loss_column = None


if (
    state_total_loss_column
    and "state" in state_totals.columns
):

    if selected_states:

        state_totals = state_totals[
            state_totals["state"].isin(
                selected_states
            )
        ]


    state_totals = state_totals.sort_values(
        state_total_loss_column,
        ascending=True
    )


    fig_totals = px.bar(

        state_totals,

        x=state_total_loss_column,

        y="state",

        orientation="h",

        text=state_total_loss_column,

        labels={
            state_total_loss_column:
                "Tree-Cover Loss (ha)",
            "state":
                "State"
        }
    )


    fig_totals.update_traces(

        texttemplate="%{text:,.0f}",

        textposition="outside",

        hovertemplate=
        "<b>%{y}</b><br>"
        "Total loss: %{x:,.2f} ha"
        "<extra></extra>"
    )


    fig_totals.update_layout(

        height=400,

        margin=dict(
            l=20,
            r=80,
            t=20,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            color="#12372A"
        ),

        xaxis=dict(
            title="Tree-Cover Loss (ha)",
            showgrid=True,
            gridcolor="#E6E1D8"
        ),

        yaxis=dict(
            title="",
            showgrid=False
        )
    )


    st.plotly_chart(
        fig_totals,
        use_container_width=True
    )


# ============================================================
# KEY METRICS
# ============================================================

st.html(
    """
    <div class="section-title">
        Selected Period Summary
    </div>
    """
)


metric1, metric2, metric3 = st.columns(3)


# ------------------------------------------------------------
# Total loss in selected period
# ------------------------------------------------------------

with metric1:

    if (
        loss_column
        and not annual_filtered.empty
    ):

        selected_total_loss = (
            annual_filtered[
                loss_column
            ].sum()
        )

        st.metric(
            "Tree-Cover Loss",
            f"{selected_total_loss:,.0f} ha"
        )

    else:

        st.metric(
            "Tree-Cover Loss",
            "—"
        )


# ------------------------------------------------------------
# Peak loss year
# ------------------------------------------------------------

with metric2:

    if (
        loss_column
        and not annual_filtered.empty
    ):

        peak_row = annual_filtered.loc[
            annual_filtered[
                loss_column
            ].idxmax()
        ]

        peak_year = int(
            peak_row["year"]
        )

        st.metric(
            "Peak Loss Year",
            str(peak_year)
        )

    else:

        st.metric(
            "Peak Loss Year",
            "—"
        )


# ------------------------------------------------------------
# Average annual loss
# ------------------------------------------------------------

with metric3:

    if (
        loss_column
        and not annual_filtered.empty
    ):

        average_loss = (
            annual_filtered[
                loss_column
            ].mean()
        )

        st.metric(
            "Average Annual Loss",
            f"{average_loss:,.0f} ha"
        )

    else:

        st.metric(
            "Average Annual Loss",
            "—"
        )


# ============================================================
# INSIGHT
# ============================================================

if (
    loss_column
    and not annual_filtered.empty
):

    peak_row = annual_filtered.loc[
        annual_filtered[
            loss_column
        ].idxmax()
    ]

    peak_year = int(
        peak_row["year"]
    )

    peak_value = peak_row[
        loss_column
    ]


    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🔎 Forest-loss signal
            </div>

            <div class="insight-text">

                Within the selected analysis period,
                the highest annual tree-cover loss occurred
                in <strong>{peak_year}</strong>,
                with approximately
                <strong>{peak_value:,.0f} hectares</strong>
                recorded that year.

                Use the state-level view above to examine
                how the annual pattern differs across
                the study states.

            </div>

        </div>
        """
    )