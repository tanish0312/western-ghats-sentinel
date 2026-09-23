import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from utils.data_loader import (
    load_annual_loss,
    load_state_analysis,
    load_lag_analysis
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Relationships | Western Ghats Sentinel",
    page_icon="🔗",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_names):
    """
    Find a column using several possible names.
    """

    if df is None or df.empty:
        return None

    columns = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in possible_names:

        key = str(name).strip().lower()

        if key in columns:
            return columns[key]

    return None


def find_column_contains(df, words):
    """
    Find a column if its name contains one of the
    supplied keywords.
    """

    if df is None or df.empty:
        return None

    for column in df.columns:

        name = str(column).strip().lower()

        for word in words:

            if word.lower() in name:
                return column

    return None


def make_numeric(series):

    return pd.to_numeric(
        series,
        errors="coerce"
    )


def strength(value):

    if pd.isna(value):
        return "Not available"

    value = abs(float(value))

    if value >= 0.90:
        return "Very strong"

    elif value >= 0.70:
        return "Strong"

    elif value >= 0.50:
        return "Moderate"

    elif value >= 0.30:
        return "Weak"

    else:
        return "Very weak"


def add_trend_line(fig, x, y):

    """
    Add a simple linear regression line using NumPy.
    This avoids statsmodels completely.
    """

    temp = pd.DataFrame({
        "x": make_numeric(x),
        "y": make_numeric(y)
    }).dropna()

    if len(temp) < 2:
        return fig

    try:

        slope, intercept = np.polyfit(
            temp["x"],
            temp["y"],
            1
        )

        x_line = np.linspace(
            temp["x"].min(),
            temp["x"].max(),
            100
        )

        y_line = (
            slope * x_line
            + intercept
        )

        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Linear trend",
                line=dict(
                    dash="dash",
                    width=3
                ),
                hoverinfo="skip"
            )
        )

    except Exception:
        pass

    return fig


# ============================================================
# LOAD DATA
# ============================================================

annual_raw = load_annual_loss()

state_raw = load_state_analysis()

lag_raw = load_lag_analysis()


# ============================================================
# PAGE STYLING
# ============================================================

st.html("""
<style>

.relationship-hero {

    padding: 42px 46px;

    border-radius: 23px;

    background:
        linear-gradient(
            135deg,
            #073628 0%,
            #0d4d39 55%,
            #1d7051 100%
        );

    color: white;

    margin-bottom: 32px;

    box-shadow:
        0 15px 35px
        rgba(7,54,40,0.14);
}


.relationship-kicker {

    color: #dcc66d;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 3px;

    margin-bottom: 10px;
}


.relationship-title {

    font-size: 44px;

    font-weight: 850;

    line-height: 1.05;
}


.relationship-subtitle {

    margin-top: 14px;

    max-width: 900px;

    font-size: 17px;

    line-height: 1.65;

    color: #e3eee9;
}


.section-kicker {

    margin-top: 36px;

    color: #ad9142;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 2.4px;
}


.section-title {

    margin-top: 4px;

    margin-bottom: 8px;

    color: #123d30;

    font-size: 27px;

    font-weight: 800;
}


.section-text {

    color: #63726b;

    line-height: 1.7;

    margin-bottom: 20px;
}


.metric-card {

    background: white;

    border:
        1px solid #e0e8e3;

    border-radius: 16px;

    padding: 21px;

    min-height: 125px;

    box-shadow:
        0 5px 18px
        rgba(20,60,48,0.05);
}


.metric-label {

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.5px;

    color: #9a8040;
}


.metric-value {

    font-size: 29px;

    font-weight: 850;

    color: #103d30;

    margin-top: 7px;
}


.metric-small {

    font-size: 13px;

    color: #6c7973;

    margin-top: 4px;
}


.insight {

    background: #eef7f3;

    border-left:
        5px solid #2f6f5e;

    border-radius: 12px;

    padding: 23px 25px;

    margin: 22px 0;

    line-height: 1.75;

    color: #294c40;
}


.note {

    background: #fff8df;

    border-left:
        5px solid #c9a33e;

    border-radius: 12px;

    padding: 21px 24px;

    margin: 22px 0;

    line-height: 1.7;

    color: #5c4a17;
}


.relationship-footer {

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
<div class="relationship-hero">

    <div class="relationship-kicker">
        ENVIRONMENTAL RELATIONSHIPS
    </div>

    <div class="relationship-title">
        Relationships
    </div>

    <div class="relationship-subtitle">
        Explore statistical relationships between tree-cover
        loss, carbon emissions and environmental patterns
        across the Western Ghats study region.
    </div>

</div>
""")


# ============================================================
# PREPARE ANNUAL DATA
# ============================================================

year_col = find_column(
    annual_raw,
    [
        "year"
    ]
)

loss_col = find_column(
    annual_raw,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "tree_loss_ha",
        "loss_ha",
        "loss"
    ]
)

emission_col = find_column(
    annual_raw,
    [
        "total_emissions_Mg",
        "total_emissions_mg",
        "emissions_Mg",
        "emissions_mg",
        "co2_emissions_mg",
        "co2_mg"
    ]
)


annual = pd.DataFrame()


if (
    year_col is not None
    and loss_col is not None
    and emission_col is not None
):

    annual = pd.DataFrame({

        "year":
            make_numeric(
                annual_raw[year_col]
            ),

        "tree_cover_loss":
            make_numeric(
                annual_raw[loss_col]
            ),

        "co2_emissions":
            make_numeric(
                annual_raw[emission_col]
            )

    }).dropna()


    annual = (
        annual
        .groupby(
            "year",
            as_index=False
        )
        .agg({
            "tree_cover_loss": "sum",
            "co2_emissions": "sum"
        })
        .sort_values("year")
    )


# ============================================================
# DATA CHECK
# ============================================================

if annual.empty:

    st.error(
        "The annual relationship dataset could not be prepared."
    )

    st.write(
        "Available columns in ANNUAL_TREE_COVER_LOSS.csv:"
    )

    st.write(
        list(annual_raw.columns)
    )

    st.stop()


# ============================================================
# CORRELATIONS
# ============================================================

pearson = annual[
    "tree_cover_loss"
].corr(
    annual[
        "co2_emissions"
    ],
    method="pearson"
)


spearman = annual[
    "tree_cover_loss"
].corr(
    annual[
        "co2_emissions"
    ],
    method="spearman"
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    '<div class="section-kicker">ANALYTICAL OVERVIEW</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">What relationships are being examined?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
This page examines whether environmental indicators move
together across time and across the five Western Ghats states.

The primary relationship is:

**Tree-cover loss ↔ CO₂ emissions**

The analysis then extends this comparison to state-level
patterns and prepared time-lag results.
""",
    unsafe_allow_html=True
)


# ============================================================
# KPI ROW
# ============================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                PEARSON r
            </div>

            <div class="metric-value">
                {pearson:.3f}
            </div>

            <div class="metric-small">
                Linear association
            </div>

        </div>
        """
    )


with k2:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                SPEARMAN ρ
            </div>

            <div class="metric-value">
                {spearman:.3f}
            </div>

            <div class="metric-small">
                Rank association
            </div>

        </div>
        """
    )


with k3:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ANNUAL OBSERVATIONS
            </div>

            <div class="metric-value">
                {len(annual)}
            </div>

            <div class="metric-small">
                Matched years
            </div>

        </div>
        """
    )


with k4:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                RELATIONSHIP STRENGTH
            </div>

            <div class="metric-value">
                {strength(spearman)}
            </div>

            <div class="metric-small">
                Based on |Spearman ρ|
            </div>

        </div>
        """
    )


# ============================================================
# RELATIONSHIP 01 — SCATTER
# ============================================================

st.markdown(
    '<div class="section-kicker">RELATIONSHIP 01</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Tree-cover loss ↔ CO₂ emissions</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
Each point represents one year. The horizontal axis shows
tree-cover loss and the vertical axis shows associated CO₂
emissions. The dashed line represents the linear trend.
""",
    unsafe_allow_html=True
)


fig = go.Figure()


fig.add_trace(
    go.Scatter(

        x=annual[
            "tree_cover_loss"
        ],

        y=annual[
            "co2_emissions"
        ],

        mode="markers+text",

        text=annual[
            "year"
        ].astype(int).astype(str),

        textposition="top center",

        marker=dict(
            size=10
        ),

        name="Annual observation",

        customdata=np.column_stack(
            [
                annual["year"],
                annual["tree_cover_loss"],
                annual["co2_emissions"]
            ]
        ),

        hovertemplate=
        "<b>%{customdata[0]:.0f}</b><br>"
        "Tree-cover loss: %{customdata[1]:,.0f} ha<br>"
        "CO₂ emissions: %{customdata[2]:,.0f} Mg"
        "<extra></extra>"
    )
)


fig = add_trend_line(
    fig,

    annual[
        "tree_cover_loss"
    ],

    annual[
        "co2_emissions"
    ]
)


fig.update_layout(

    template="plotly_white",

    height=530,

    xaxis_title="Tree-cover loss (ha)",

    yaxis_title="CO₂ emissions (Mg)",

    margin=dict(
        l=20,
        r=20,
        t=25,
        b=25
    ),

    hoverlabel=dict(
        bgcolor="#0B3D2E",
        font_color="white"
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CORRELATION INTERPRETATION
# ============================================================

if spearman > 0:
    direction = "positive"

elif spearman < 0:
    direction = "negative"

else:
    direction = "near-zero"


st.html(
    f"""
    <div class="insight">

    <b>Observed relationship</b>

    <br><br>

    Tree-cover loss and CO₂ emissions show a
    <b>{direction}</b> statistical association across
    <b>{len(annual)}</b> annual observations.

    <br><br>

    <b>Pearson r:</b> {pearson:.3f}

    <br>

    <b>Spearman ρ:</b> {spearman:.3f}

    <br><br>

    Pearson captures the linear association, while Spearman
    captures whether the two variables generally move together
    in rank order.

    </div>
    """
)


# ============================================================
# RELATIONSHIP 02 — TIME COMPARISON
# ============================================================

st.markdown(
    '<div class="section-kicker">RELATIONSHIP 02</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">How do the two indicators change over time?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
Because tree-cover loss and emissions use different units,
both series are normalized to a 0–100 index for visual
comparison.
""",
    unsafe_allow_html=True
)


comparison = annual.copy()


# Normalize loss

loss_min = comparison[
    "tree_cover_loss"
].min()

loss_max = comparison[
    "tree_cover_loss"
].max()


if loss_max != loss_min:

    comparison[
        "loss_index"
    ] = (
        (
            comparison["tree_cover_loss"]
            - loss_min
        )
        /
        (
            loss_max
            - loss_min
        )
    ) * 100

else:

    comparison[
        "loss_index"
    ] = 100


# Normalize emissions

emission_min = comparison[
    "co2_emissions"
].min()

emission_max = comparison[
    "co2_emissions"
].max()


if emission_max != emission_min:

    comparison[
        "emission_index"
    ] = (
        (
            comparison["co2_emissions"]
            - emission_min
        )
        /
        (
            emission_max
            - emission_min
        )
    ) * 100

else:

    comparison[
        "emission_index"
    ] = 100


comparison_long = comparison[
    [
        "year",
        "loss_index",
        "emission_index"
    ]
].melt(
    id_vars="year",
    value_vars=[
        "loss_index",
        "emission_index"
    ],
    var_name="indicator",
    value_name="index"
)


comparison_long[
    "indicator"
] = comparison_long[
    "indicator"
].replace({

    "loss_index":
        "Tree-cover loss",

    "emission_index":
        "CO₂ emissions"

})


time_fig = px.line(

    comparison_long,

    x="year",

    y="index",

    color="indicator",

    markers=True,

    labels={
        "year": "Year",
        "index": "Normalized index (0–100)",
        "indicator": ""
    },

    title="Normalized annual pattern"
)


time_fig.update_layout(

    template="plotly_white",

    height=450,

    hovermode="x unified",

    margin=dict(
        l=20,
        r=20,
        t=55,
        b=25
    )
)


st.plotly_chart(
    time_fig,
    use_container_width=True
)


# ============================================================
# RELATIONSHIP 03 — STATE LEVEL
# ============================================================

state_name_col = find_column(
    state_raw,
    [
        "state",
        "state_name"
    ]
)

state_loss_col = find_column(
    state_raw,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "loss_ha",
        "total_loss"
    ]
)

state_emission_col = find_column(
    state_raw,
    [
        "total_emissions_Mg",
        "total_emissions_mg",
        "emissions_Mg",
        "emissions_mg",
        "co2_emissions_mg"
    ]
)


if (
    state_name_col is not None
    and state_loss_col is not None
    and state_emission_col is not None
):

    states = pd.DataFrame({

        "state":
            state_raw[
                state_name_col
            ].astype(str),

        "loss":
            make_numeric(
                state_raw[
                    state_loss_col
                ]
            ),

        "emissions":
            make_numeric(
                state_raw[
                    state_emission_col
                ]
            )

    }).dropna()


    if len(states) >= 3:

        state_pearson = states[
            "loss"
        ].corr(
            states[
                "emissions"
            ],
            method="pearson"
        )


        state_spearman = states[
            "loss"
        ].corr(
            states[
                "emissions"
            ],
            method="spearman"
        )


        st.markdown(
            '<div class="section-kicker">RELATIONSHIP 03</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">State-level relationship</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
The same relationship can be examined spatially across the
five states in the study region.
""",
            unsafe_allow_html=True
        )


        s1, s2, s3 = st.columns(3)


        with s1:

            st.metric(
                "STATES",
                len(states)
            )


        with s2:

            st.metric(
                "PEARSON r",
                f"{state_pearson:.3f}"
            )


        with s3:

            st.metric(
                "SPEARMAN ρ",
                f"{state_spearman:.3f}"
            )


        state_fig = go.Figure()


        state_fig.add_trace(
            go.Scatter(

                x=states["loss"],

                y=states["emissions"],

                mode="markers+text",

                text=states["state"],

                textposition="top center",

                marker=dict(
                    size=14
                ),

                name="State",

                hovertemplate=
                "<b>%{text}</b><br>"
                "Tree-cover loss: %{x:,.0f} ha<br>"
                "CO₂ emissions: %{y:,.0f} Mg"
                "<extra></extra>"
            )
        )


        state_fig = add_trend_line(
            state_fig,

            states["loss"],

            states["emissions"]
        )


        state_fig.update_layout(

            template="plotly_white",

            height=480,

            xaxis_title="Tree-cover loss (ha)",

            yaxis_title="CO₂ emissions (Mg)",

            margin=dict(
                l=20,
                r=20,
                t=25,
                b=25
            )
        )


        st.plotly_chart(
            state_fig,
            use_container_width=True
        )


# ============================================================
# RELATIONSHIP 04 — LAG ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-kicker">RELATIONSHIP 04</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Lag analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
Lag analysis examines how the prepared statistical relationship
changes when observations are shifted across different numbers
of years.
""",
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# ROBUST LAG COLUMN DETECTION
# ------------------------------------------------------------

lag_column = None

correlation_column = None


# First: exact expected names

lag_column = find_column(
    lag_raw,
    [
        "lag",
        "lag_year",
        "lag_years",
        "year_lag",
        "years_lag",
        "shift",
        "years"
    ]
)


correlation_column = find_column(
    lag_raw,
    [
        "spearman_correlation",
        "spearman_corr",
        "spearman_r",
        "spearman_rho",
        "correlation",
        "correlation_coefficient",
        "rho",
        "corr"
    ]
)


# Second: search by keywords

if lag_column is None:

    lag_column = find_column_contains(
        lag_raw,
        [
            "lag",
            "shift"
        ]
    )


if correlation_column is None:

    correlation_column = find_column_contains(
        lag_raw,
        [
            "correlation",
            "spearman",
            "rho",
            "corr"
        ]
    )


# ------------------------------------------------------------
# FALLBACK: NUMERIC COLUMNS
# ------------------------------------------------------------

numeric_columns = []

for column in lag_raw.columns:

    converted = pd.to_numeric(
        lag_raw[column],
        errors="coerce"
    )

    if converted.notna().sum() >= 2:

        numeric_columns.append(
            column
        )


# If lag wasn't found, use the first numeric
# column that looks like a small lag series.

if lag_column is None:

    for column in numeric_columns:

        values = pd.to_numeric(
            lag_raw[column],
            errors="coerce"
        ).dropna()

        if len(values) > 0:

            if values.min() >= -20 and values.max() <= 20:

                lag_column = column
                break


# If correlation wasn't found, use another numeric column.

if correlation_column is None:

    for column in numeric_columns:

        if column == lag_column:
            continue

        values = pd.to_numeric(
            lag_raw[column],
            errors="coerce"
        ).dropna()

        if len(values) > 0:

            if (
                values.min() >= -1.01
                and
                values.max() <= 1.01
            ):

                correlation_column = column
                break


# ------------------------------------------------------------
# BUILD LAG DATA
# ------------------------------------------------------------

if (
    lag_column is not None
    and correlation_column is not None
):

    lag_data = pd.DataFrame({

        "lag":
            make_numeric(
                lag_raw[
                    lag_column
                ]
            ),

        "correlation":
            make_numeric(
                lag_raw[
                    correlation_column
                ]
            )

    }).dropna()


    if not lag_data.empty:

        lag_data = lag_data.sort_values(
            "lag"
        )


        # ====================================================
        # LAG KPI
        # ====================================================

        strongest_row = lag_data.loc[
            lag_data[
                "correlation"
            ].abs().idxmax()
        ]


        l1, l2, l3 = st.columns(3)


        with l1:

            st.metric(
                "LAG OBSERVATIONS",
                len(lag_data)
            )


        with l2:

            st.metric(
                "LAG RANGE",
                f"{int(lag_data['lag'].min())}–"
                f"{int(lag_data['lag'].max())}"
            )


        with l3:

            st.metric(
                "STRONGEST LAG",
                f"{int(strongest_row['lag'])} years"
            )


        # ====================================================
        # LAG CHART
        # ====================================================

        lag_fig = px.line(

            lag_data,

            x="lag",

            y="correlation",

            markers=True,

            labels={
                "lag":
                    "Lag (years)",

                "correlation":
                    "Correlation"
            },

            title="Correlation across time lags"
        )


        lag_fig.add_hline(
            y=0,
            line_dash="dash"
        )


        lag_fig.update_layout(

            template="plotly_white",

            height=430,

            margin=dict(
                l=20,
                r=20,
                t=55,
                b=25
            ),

            hovermode="x unified"
        )


        st.plotly_chart(
            lag_fig,
            use_container_width=True
        )


        # ====================================================
        # LAG FINDING
        # ====================================================

        st.html(
            f"""
            <div class="insight">

            <b>Lag finding</b>

            <br><br>

            The strongest absolute association in the prepared
            lag-analysis results occurs at a
            <b>{int(strongest_row["lag"])}-year lag</b>.

            <br><br>

            Correlation:
            <b>{strongest_row["correlation"]:.3f}</b>

            </div>
            """
        )


        # ====================================================
        # LAG TABLE
        # ====================================================

        with st.expander(
            "View lag-analysis values"
        ):

            st.dataframe(
                lag_data,
                use_container_width=True,
                hide_index=True
            )


    else:

        st.warning(
            "The lag-analysis file was found, but it does not "
            "contain usable numerical lag values."
        )


else:

    # This should only happen if the actual CSV
    # contains something completely unexpected.

    st.warning(
        "The lag-analysis structure could not be interpreted automatically."
    )

    with st.expander(
        "Show LAG_ANALYSIS.csv columns"
    ):

        st.write(
            list(lag_raw.columns)
        )


# ============================================================
# RESEARCH INTERPRETATION
# ============================================================

st.markdown(
    '<div class="section-kicker">RESEARCH INTERPRETATION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">How should these relationships be read?</div>',
    unsafe_allow_html=True
)

st.html(
    """
    <div class="note">

    <b>Correlation describes association, not causation.</b>

    <br><br>

    A strong correlation means that two variables tend to move
    together in the available observations. It does not by itself
    establish that changes in one variable caused changes in the
    other.

    <br><br>

    The lag analysis is similarly exploratory: a stronger
    association at a particular lag identifies a statistical
    pattern in the prepared data, not proof of an ecological
    cause-and-effect delay.

    </div>
    """
)


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown(
    '<div class="section-kicker">RESEARCH OUTPUT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Download relationship data</div>',
    unsafe_allow_html=True
)


download = annual.copy()

download[
    "pearson_r"
] = pearson

download[
    "spearman_rho"
] = spearman


st.download_button(

    label="⬇️ Download annual relationship dataset",

    data=download.to_csv(
        index=False
    ).encode("utf-8"),

    file_name=
    "western_ghats_relationship_analysis.csv",

    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="relationship-footer">

    <b>Western Ghats Sentinel</b><br>

    Relationships · Tree Cover · Carbon · Conservation

</div>
""")