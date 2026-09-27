import os
import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Species Gallery | Western Ghats Sentinel",
    page_icon="🐆",
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

    .species-card-name {
        font-size: 16px;
        font-weight: 750;
        color: #12372A;
        margin-top: 10px;
        margin-bottom: 0px;
    }

    .species-card-common {
        font-size: 13px;
        color: #68756D;
        font-style: italic;
        margin-bottom: 8px;
    }

    .status-badge {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
        color: white;
    }

    .trend-tag {
        font-size: 12px;
        font-weight: 700;
        margin-left: 8px;
    }

    .no-photo-box {
        background: #e8ede9;
        border-radius: 12px;
        padding: 30px 10px;
        text-align: center;
        color: #5f6d64;
        font-size: 12px;
        font-style: italic;
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/SPECIES_STATUS_HISTORY.csv")


history = load_data().copy()

SPECIES = "species"
COMMON_NAME = "common_name"
ORDER = "order"
YEAR = "year_published"
STATUS = "status_standardized"

history[SPECIES] = history[SPECIES].astype(str).str.strip()
history[COMMON_NAME] = history[COMMON_NAME].astype(str).str.strip()
history[STATUS] = history[STATUS].astype(str).str.strip()
history[YEAR] = pd.to_numeric(history[YEAR], errors="coerce")
history = history.dropna(subset=[YEAR])


# ============================================================
# SEVERITY SCALE
# ============================================================

SEVERITY_ORDER = {
    "LC": 0,
    "NT": 1,
    "VU": 2,
    "EN": 3,
    "CR": 4,
    "EW": 5,
    "EX": 6,
}

STATUS_COLORS = {
    "LC": "#4C8A5E",
    "NT": "#D98A33",
    "VU": "#C9762E",
    "EN": "#B84A3A",
    "CR": "#8B1E1E",
    "EW": "#5A1414",
    "EX": "#2A0A0A",
    "DD": "#8D7945",
    "NE": "#8D7945",
}


# ============================================================
# BUILD PER-SPECIES SUMMARY
# ============================================================

@st.cache_data
def build_species_summary(history_df):
    rows = []

    for species, group in history_df.groupby(SPECIES):
        group = group.sort_values(YEAR)
        valid = group[group[STATUS].isin(SEVERITY_ORDER.keys())]

        if valid.empty:
            continue

        first_row = valid.iloc[0]
        latest_row = valid.iloc[-1]

        first_sev = SEVERITY_ORDER[first_row[STATUS]]
        latest_sev = SEVERITY_ORDER[latest_row[STATUS]]

        if latest_sev > first_sev:
            trend = "Worsened"
        elif latest_sev < first_sev:
            trend = "Improved"
        else:
            trend = "Stable"

        common_name = group[COMMON_NAME].iloc[0]
        order_name = group[ORDER].iloc[0] if ORDER in group.columns else "—"

        rows.append({
            "species": species,
            "common_name": common_name,
            "order": order_name,
            "latest_status": latest_row[STATUS],
            "first_status": first_row[STATUS],
            "first_year": int(first_row[YEAR]),
            "latest_year": int(latest_row[YEAR]),
            "trend": trend,
        })

    return pd.DataFrame(rows)


summary = build_species_summary(history)


# ============================================================
# IMAGE HELPER
# ============================================================

def get_species_image_path(species_name):
    base = species_name.lower().replace(" ", "_")
    for ext in [".jpg", ".jpeg", ".png"]:
        path = os.path.join("images", base + ext)
        if os.path.exists(path):
            return path
    return None


# ============================================================
# PAGE HEADER
# ============================================================

worsened_count = (summary["trend"] == "Worsened").sum()
total_count = len(summary)

st.html(
    f"""
    <div class="page-header">
        <div class="page-label">Species Gallery</div>
        <div class="page-title">🐆 Meet the Species</div>
        <div class="page-description">
            {total_count} mammal species tracked across the Western
            Ghats — a visual record of who is affected by habitat
            loss in this region. {worsened_count} of them have moved
            toward a more threatened status since their earliest
            recorded assessment.
        </div>
    </div>
    """
)


# ============================================================
# FILTERS
# ============================================================

col_filter, col_search = st.columns([2, 2])

with col_filter:
    trend_filter = st.radio(
        "Filter by trend",
        ["All", "Worsened", "Stable", "Improved"],
        horizontal=True
    )

with col_search:
    search_term = st.text_input(
        "Search species",
        placeholder="Search by name..."
    )


filtered = summary.copy()

if trend_filter != "All":
    filtered = filtered[filtered["trend"] == trend_filter]

if search_term:
    term = search_term.lower().strip()
    filtered = filtered[
        filtered["species"].str.lower().str.contains(term)
        | filtered["common_name"].str.lower().str.contains(term)
    ]

filtered = filtered.sort_values(
    "species"
).reset_index(drop=True)

st.markdown(
    f"**{len(filtered)}** species match your filters."
)


# ============================================================
# TREND TAG STYLING
# ============================================================

TREND_STYLE = {
    "Worsened": ("#8B1E1E", "▼ Worsened"),
    "Stable": ("#68756D", "→ Stable"),
    "Improved": ("#2E6B45", "▲ Improved"),
}


# ============================================================
# SPECIES GRID
# ============================================================

CARDS_PER_ROW = 4

rows_needed = (len(filtered) + CARDS_PER_ROW - 1) // CARDS_PER_ROW

for row_idx in range(rows_needed):

    cols = st.columns(CARDS_PER_ROW)

    for col_idx in range(CARDS_PER_ROW):

        item_idx = row_idx * CARDS_PER_ROW + col_idx

        if item_idx >= len(filtered):
            continue

        item = filtered.iloc[item_idx]

        with cols[col_idx]:

            with st.container(border=True):

                image_path = get_species_image_path(item["species"])

                if image_path:
                    st.image(image_path, use_container_width=True)
                else:
                    st.html(
                        """
                        <div class="no-photo-box">
                            📷 No verified photograph available
                        </div>
                        """
                    )

                status_color = STATUS_COLORS.get(
                    item["latest_status"], "#8D7945"
                )

                trend_color, trend_label = TREND_STYLE.get(
                    item["trend"], ("#68756D", item["trend"])
                )

                st.html(
                    f"""
                    <div class="species-card-name">{item['species']}</div>
                    <div class="species-card-common">{item['common_name']}</div>
                    <span class="status-badge" style="background:{status_color}">
                        {item['latest_status']}
                    </span>
                    <span class="trend-tag" style="color:{trend_color}">
                        {trend_label}
                    </span>
                    """
                )


if len(filtered) == 0:
    st.info("No species match your current filters. Try adjusting them.")
