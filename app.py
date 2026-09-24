import streamlit as st


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
# GLOBAL DESIGN SYSTEM
# ============================================================

st.html("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

html, body, [class*="css"] {

    font-family:
        "Inter",
        "Segoe UI",
        sans-serif;
}


.stApp {

    background:
        #f7f9f7;
}


/* =========================================================
   MAIN CONTENT
   ========================================================= */

.block-container {

    padding-top: 2rem;

    padding-bottom: 4rem;

    max-width: 1500px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #062f24 0%,
            #083b2c 55%,
            #0b4935 100%
        );

    border-right:
        1px solid
        rgba(255,255,255,0.08);
}


/* Sidebar text */

[data-testid="stSidebar"] * {

    color: #e8f1ed;
}


/* Navigation items */

[data-testid="stSidebarNav"] a {

    border-radius: 10px;

    margin:
        3px 8px;

    transition:
        background 0.2s ease,
        transform 0.2s ease;
}


[data-testid="stSidebarNav"] a:hover {

    background:
        rgba(220,198,109,0.12);

    transform:
        translateX(3px);
}


/* Active navigation item */

[data-testid="stSidebarNav"] a[aria-current="page"] {

    background:
        rgba(220,198,109,0.17);

    border-left:
        3px solid #dcc66d;
}


/* =========================================================
   SIDEBAR BRAND
   ========================================================= */

.sidebar-brand {

    padding:
        8px 8px 24px 8px;

    margin-bottom:
        15px;

    border-bottom:
        1px solid
        rgba(255,255,255,0.12);
}


.sidebar-logo {

    font-size:
        28px;

    margin-bottom:
        7px;
}


.sidebar-title {

    font-size:
        18px;

    font-weight:
        850;

    letter-spacing:
        0.2px;

    color:
        #ffffff;
}


.sidebar-subtitle {

    margin-top:
        5px;

    font-size:
        11px;

    line-height:
        1.5;

    color:
        #b9cec5;

    letter-spacing:
        0.4px;
}


.sidebar-section {

    color:
        #d9c66d;

    font-size:
        9px;

    font-weight:
        800;

    letter-spacing:
        2px;

    margin:
        22px 8px 8px;
}


/* =========================================================
   STREAMLIT DEFAULT BUTTONS
   ========================================================= */

.stButton > button {

    border-radius:
        10px;

    border:
        1px solid #d9e2dd;

    background:
        white;

    color:
        #123d30;

    font-weight:
        650;

    transition:
        all 0.2s ease;
}


.stButton > button:hover {

    border-color:
        #2f6f5e;

    color:
        #103d30;

    transform:
        translateY(-1px);

    box-shadow:
        0 4px 12px
        rgba(20,60,48,0.08);
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton > button {

    border-radius:
        10px;

    background:
        #0b4a36;

    color:
        white;

    border:
        1px solid #0b4a36;

    font-weight:
        700;

    transition:
        all 0.2s ease;
}


.stDownloadButton > button:hover {

    background:
        #176b4d;

    border-color:
        #176b4d;

    transform:
        translateY(-1px);
}


/* =========================================================
   SELECTBOX / MULTISELECT
   ========================================================= */

[data-baseweb="select"] > div {

    border-radius:
        10px;

    border-color:
        #dce5e0;
}


[data-baseweb="select"] > div:focus-within {

    border-color:
        #2f6f5e;

    box-shadow:
        0 0 0 1px #2f6f5e;
}


/* =========================================================
   SLIDER
   ========================================================= */

[data-testid="stSlider"] {

    padding-top:
        8px;
}


/* =========================================================
   METRIC
   ========================================================= */

[data-testid="stMetric"] {

    background:
        white;

    border:
        1px solid #e0e8e4;

    border-radius:
        14px;

    padding:
        16px 18px;

    box-shadow:
        0 4px 15px
        rgba(20,60,48,0.045);
}


[data-testid="stMetricLabel"] {

    color:
        #8d7945;
}


[data-testid="stMetricValue"] {

    color:
        #103d30;

    font-weight:
        800;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {

    border-radius:
        12px;

    overflow:
        hidden;

    border:
        1px solid #dfe7e2;
}


/* =========================================================
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {

    border:
        1px solid #dfe7e2;

    border-radius:
        12px;

    background:
        white;

    overflow:
        hidden;
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {

    gap:
        6px;

    border-bottom:
        1px solid #dfe7e2;
}


.stTabs [data-baseweb="tab"] {

    border-radius:
        8px 8px 0 0;

    padding:
        9px 15px;

    color:
        #63736b;
}


.stTabs [aria-selected="true"] {

    color:
        #103d30 !important;

    font-weight:
        750;
}


/* =========================================================
   ALERTS
   ========================================================= */

[data-testid="stAlert"] {

    border-radius:
        11px;
}


/* =========================================================
   PLOTLY CONTAINERS
   ========================================================= */

[data-testid="stPlotlyChart"] {

    border-radius:
        14px;

    overflow:
        hidden;

    background:
        white;

    border:
        1px solid #e3e9e5;

    box-shadow:
        0 4px 16px
        rgba(20,60,48,0.035);
}


/* =========================================================
   CHECKBOX
   ========================================================= */

[data-testid="stCheckbox"] {

    color:
        #294c40;
}


/* =========================================================
   RADIO
   ========================================================= */

[data-testid="stRadio"] {

    color:
        #294c40;
}


/* =========================================================
   TEXT INPUT
   ========================================================= */

[data-baseweb="input"] {

    border-radius:
        10px;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {

    width:
        8px;

    height:
        8px;
}


::-webkit-scrollbar-track {

    background:
        #eef2ef;
}


::-webkit-scrollbar-thumb {

    background:
        #9aada4;

    border-radius:
        10px;
}


::-webkit-scrollbar-thumb:hover {

    background:
        #5d796c;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;
    }

    .hero-title {

        font-size:
            34px;
    }

}

</style>
""")


# ============================================================
# SIDEBAR BRAND
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            🌿
        </div>

        <div class="sidebar-title">
            Western Ghats Sentinel
        </div>

        <div class="sidebar-subtitle">
            Tree Cover • Carbon • Conservation
        </div>

    </div>
    """)


# ============================================================
# NAVIGATION
# ============================================================

pages = {

    "EXPLORE": [

        st.Page(
            "overview.py",
            title="Overview",
            icon="🏠",
            url_path="overview",
            default=True
        ),

        st.Page(
            "pages/1_Forest_Loss.py",
            title="Forest Loss",
            icon="🌲",
            url_path="forest-loss"
        ),

        st.Page(
            "pages/2_Spatial_Explorer.py",
            title="Spatial Explorer",
            icon="🗺️",
            url_path="spatial-explorer"
        ),

        st.Page(
            "pages/3_Conservation.py",
            title="Conservation",
            icon="🐘",
            url_path="conservation"
        ),

        st.Page(
            "pages/4_Relationships.py",
            title="Relationships",
            icon="🔗",
            url_path="relationships"
        ),

        st.Page(
            "pages/5_Data_Explorer.py",
            title="Data Explorer",
            icon="📊",
            url_path="data-explorer"
        ),

        st.Page(
            "pages/6_About_Methodology.py",
            title="About & Methodology",
            icon="🌿",
            url_path="about"
        ),

        st.Page(
            "pages/7_Executive_View.py",
            title="Executive View",
            icon="🎯",
            url_path="executive-view"
        ),

        st.Page(
            "pages/8_Forecast.py",
            title="Forecast",
            icon="📈",
            url_path="forecast"
        ),

        st.Page(
            "pages/9_District_Hotspots.py",
            title="District Hotspots",
            icon="🎯",
            url_path="district-hotspots"
        )

    ]

}


# ============================================================
# RUN APP
# ============================================================

pg = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

pg.run()