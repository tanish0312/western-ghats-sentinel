import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats

from utils.data_loader import (
    load_annual_loss,
    load_state_year_loss
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Forecast | Western Ghats Sentinel",
    page_icon="📈",
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
        margin-bottom: 18px;
    }

    .caveat-box {
        background: #FBF3E3;
        border: 1px solid #E9D9AE;
        border-radius: 16px;
        padding: 18px 22px;
        color: #6F5740;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="page-header">
        <div class="page-label">Projection</div>
        <div class="page-title">Forecast</div>
        <div class="page-description">
            A forward-looking projection of tree cover loss,
            based on a linear trend fitted to observed
            2001&ndash;2025 data. Shaded bands show the 95%
            confidence interval of the projection.
        </div>
    </div>
    """
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    annual = load_annual_loss()
    state_year = load_state_year_loss()
    return annual, state_year


annual, state_year = load_data()

YEAR = "year"
LOSS = "total_loss_ha"

STATE = "state"
STATE_YEAR = "year"
STATE_LOSS = "tree_cover_loss_ha"


# ============================================================
# FORECAST HELPER
# ============================================================

def fit_forecast(years, values, horizon_years):
    """
    Fits a simple linear trend and projects it forward,
    returning projected years, point forecast, and a
    95% confidence band for the projection.
    """

    years = np.array(years, dtype=float)
    values = np.array(values, dtype=float)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        years, values
    )

    last_year = int(years.max())

    future_years = np.arange(
        last_year + 1,
        last_year + 1 + horizon_years
    )

    future_pred = intercept + slope * future_years

    # Residual-based prediction interval
    fitted = intercept + slope * years
    residuals = values - fitted
    residual_std = residuals.std(ddof=2) if len(years) > 2 else 0

    n = len(years)
    mean_year = years.mean()
    ss_x = np.sum((years - mean_year) ** 2)

    t_val = stats.t.ppf(0.975, df=max(n - 2, 1))

    se_pred = residual_std * np.sqrt(
        1 + 1 / n + (future_years - mean_year) ** 2 / ss_x
    )

    margin = t_val * se_pred

    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "future_years": future_years,
        "future_pred": np.clip(future_pred, a_min=0, a_max=None),
        "lower": np.clip(future_pred - margin, a_min=0, a_max=None),
        "upper": np.clip(future_pred + margin, a_min=0, a_max=None),
    }


# ============================================================
# CONTROLS
# ============================================================

st.html(
    """
    <div class="section-title">Regional Forecast</div>
    <div class="section-description">
        Projected total tree cover loss across all five
        Western Ghats states.
    </div>
    """
)

horizon = st.slider(
    "Years to project forward",
    min_value=3,
    max_value=10,
    value=5
)


# ============================================================
# REGIONAL FORECAST CHART
# ============================================================

annual_sorted = annual.sort_values(YEAR)

result = fit_forecast(
    annual_sorted[YEAR],
    annual_sorted[LOSS],
    horizon
)

fig = go.Figure()

# Observed data
fig.add_trace(
    go.Scatter(
        x=annual_sorted[YEAR],
        y=annual_sorted[LOSS],
        mode="lines+markers",
        name="Observed",
        line=dict(color="#1F5C45", width=3),
        marker=dict(size=6)
    )
)

# Confidence band
fig.add_trace(
    go.Scatter(
        x=np.concatenate([result["future_years"], result["future_years"][::-1]]),
        y=np.concatenate([result["upper"], result["lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(217,138,51,0.18)",
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        name="95% confidence interval",
        showlegend=True
    )
)

# Projection line
fig.add_trace(
    go.Scatter(
        x=result["future_years"],
        y=result["future_pred"],
        mode="lines+markers",
        name="Projected",
        line=dict(color="#D98A33", width=3, dash="dash"),
        marker=dict(size=7, symbol="diamond")
    )
)

fig.update_layout(
    height=460,
    margin=dict(l=15, r=20, t=15, b=15),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", color="#5F6D64"),
    xaxis=dict(title="Year", showgrid=False),
    yaxis=dict(title="Tree cover loss (hectares)", gridcolor="#E8E8E2"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0)
)

st.plotly_chart(fig, use_container_width=True)


# ============================================================
# KEY FORECAST METRICS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        f"Projected loss in {int(result['future_years'][-1])}",
        f"{result['future_pred'][-1]:,.0f} ha"
    )

with col2:
    cumulative = result["future_pred"].sum()
    st.metric(
        f"Cumulative projected loss ({horizon}-yr)",
        f"{cumulative:,.0f} ha"
    )

with col3:
    st.metric(
        "Trend fit (R²)",
        f"{result['r_squared']:.2f}"
    )


# ============================================================
# STATE-LEVEL FORECAST
# ============================================================

st.html(
    """
    <div class="section-title">State-Level Forecast</div>
    <div class="section-description">
        Select a state to view its individual projected
        trajectory.
    </div>
    """
)

states_available = sorted(state_year[STATE].unique().tolist())

selected_state = st.selectbox(
    "Select a state",
    states_available
)

state_data = state_year[
    state_year[STATE] == selected_state
].sort_values(STATE_YEAR)

state_result = fit_forecast(
    state_data[STATE_YEAR],
    state_data[STATE_LOSS],
    horizon
)

fig_state = go.Figure()

fig_state.add_trace(
    go.Scatter(
        x=state_data[STATE_YEAR],
        y=state_data[STATE_LOSS],
        mode="lines+markers",
        name="Observed",
        line=dict(color="#2E6B45", width=3),
        marker=dict(size=6)
    )
)

fig_state.add_trace(
    go.Scatter(
        x=np.concatenate([state_result["future_years"], state_result["future_years"][::-1]]),
        y=np.concatenate([state_result["upper"], state_result["lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(217,138,51,0.18)",
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        name="95% confidence interval"
    )
)

fig_state.add_trace(
    go.Scatter(
        x=state_result["future_years"],
        y=state_result["future_pred"],
        mode="lines+markers",
        name="Projected",
        line=dict(color="#D98A33", width=3, dash="dash"),
        marker=dict(size=7, symbol="diamond")
    )
)

fig_state.update_layout(
    height=420,
    margin=dict(l=15, r=20, t=15, b=15),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", color="#5F6D64"),
    xaxis=dict(title="Year", showgrid=False),
    yaxis=dict(title="Tree cover loss (hectares)", gridcolor="#E8E8E2"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0)
)

st.plotly_chart(fig_state, use_container_width=True)

trend_direction = "increasing" if state_result["slope"] > 0 else "decreasing"

st.markdown(
    f"**{selected_state}** shows an {trend_direction} trend of "
    f"**{abs(state_result['slope']):,.0f} ha/year** "
    f"(R² = {state_result['r_squared']:.2f}, "
    f"p = {state_result['p_value']:.3f})."
)


# ============================================================
# METHODOLOGICAL CAVEAT
# ============================================================

st.html(
    """
    <div class="caveat-box">
        <b>Note on methodology:</b> this forecast uses a simple
        linear extrapolation of the historical trend and does
        not account for policy interventions, climate variability,
        or non-linear acceleration/deceleration in loss rates.
        It should be read as an indicative continuation of current
        conditions, not a precise prediction. Confidence intervals
        widen for years further from the observed data, reflecting
        increasing uncertainty.
    </div>
    """
)