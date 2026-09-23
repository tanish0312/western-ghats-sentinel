# ============================================================
# WESTERN GHATS SENTINEL
# GLOBAL VISUAL THEME
# ============================================================

import streamlit as st
import plotly.graph_objects as go


# ============================================================
# COLOR PALETTE
# ============================================================

FOREST = "#0B3D2E"
FOREST_LIGHT = "#145943"
FOREST_MID = "#1F6B50"

GOLD = "#D6C27A"
GOLD_DARK = "#B09343"

CREAM = "#FFF9E8"
SOFT_GREEN = "#EEF7F3"
PAGE_BG = "#FAFBFA"

TEXT = "#173F32"
MUTED = "#66746D"

BORDER = "#E3E9E5"


# ============================================================
# GLOBAL CSS
# ============================================================

def apply_global_theme():

    st.html(
        f"""
        <style>

        /* ====================================================
           PAGE
           ==================================================== */

        .stApp {{
            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    {PAGE_BG} 100%
                );
        }}


        .block-container {{
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }}


        /* ====================================================
           HEADINGS
           ==================================================== */

        h1, h2, h3, h4 {{
            color: {TEXT};
            letter-spacing: -0.3px;
        }}


        /* ====================================================
           BUTTONS
           ==================================================== */

        .stButton > button {{
            border-radius: 10px;

            border: 1px solid {BORDER};

            background: white;

            color: {FOREST};

            font-weight: 700;

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                background 0.18s ease;
        }}


        .stButton > button:hover {{
            transform: translateY(-2px);

            box-shadow:
                0 7px 18px
                rgba(11,61,46,0.10);

            background:
                {SOFT_GREEN};

            border-color:
                {FOREST_LIGHT};
        }}


        /* ====================================================
           DOWNLOAD BUTTON
           ==================================================== */

        .stDownloadButton > button {{
            border-radius: 10px;

            background:
                {FOREST};

            color: white;

            border:
                1px solid {FOREST};

            font-weight: 700;

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }}


        .stDownloadButton > button:hover {{
            transform: translateY(-2px);

            box-shadow:
                0 8px 20px
                rgba(11,61,46,0.16);

            background:
                {FOREST_LIGHT};
        }}


        /* ====================================================
           METRIC CARDS
           ==================================================== */

        [data-testid="stMetric"] {{
            background: white;

            border:
                1px solid {BORDER};

            border-radius: 15px;

            padding:
                17px 18px;

            box-shadow:
                0 4px 15px
                rgba(20,60,48,0.045);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }}


        [data-testid="stMetric"]:hover {{
            transform:
                translateY(-2px);

            box-shadow:
                0 9px 24px
                rgba(20,60,48,0.08);
        }}


        [data-testid="stMetricLabel"] {{
            color:
                {MUTED};

            font-size:
                11px;

            font-weight:
                800;

            letter-spacing:
                1.4px;
        }}


        [data-testid="stMetricValue"] {{
            color:
                {FOREST};

            font-weight:
                800;
        }}


        /* ====================================================
           SELECTBOXES
           ==================================================== */

        div[data-baseweb="select"] > div {{
            border-radius:
                10px;

            border-color:
                {BORDER};

            background:
                white;
        }}


        /* ====================================================
           SLIDERS
           ==================================================== */

        [data-testid="stSlider"] {{
            padding-top:
                8px;
        }}


        /* ====================================================
           DATAFRAMES
           ==================================================== */

        [data-testid="stDataFrame"] {{
            border-radius:
                12px;

            overflow:
                hidden;

            border:
                1px solid {BORDER};
        }}


        /* ====================================================
           EXPANDERS
           ==================================================== */

        [data-testid="stExpander"] {{
            border:
                1px solid {BORDER};

            border-radius:
                12px;

            background:
                white;
        }}


        /* ====================================================
           TABS
           ==================================================== */

        button[data-baseweb="tab"] {{
            font-weight:
                700;

            color:
                {MUTED};
        }}


        button[data-baseweb="tab"][aria-selected="true"] {{
            color:
                {FOREST};
        }}


        /* ====================================================
           ALERTS
           ==================================================== */

        [data-testid="stAlert"] {{
            border-radius:
                12px;
        }}


        /* ====================================================
           SIDEBAR
           ==================================================== */

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    {FOREST} 0%,
                    #0A4634 55%,
                    #082F25 100%
                );
        }}


        [data-testid="stSidebarNav"] {{
            padding-top:
                10px;
        }}


        [data-testid="stSidebarNav"] a {{
            border-radius:
                9px;

            margin:
                3px 8px;

            transition:
                transform 0.18s ease,
                background 0.18s ease;
        }}


        [data-testid="stSidebarNav"] a:hover {{
            transform:
                translateX(3px);

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.09
                );
        }}


        [data-testid="stSidebarNav"]
        a[aria-current="page"] {{
            background:
                rgba(
                    255,
                    255,
                    255,
                    0.17
                );

            font-weight:
                700;
        }}


        /* ====================================================
           PLOTLY CONTAINER
           ==================================================== */

        [data-testid="stPlotlyChart"] {{
            border-radius:
                14px;

            overflow:
                hidden;
        }}


        /* ====================================================
           PAGE TRANSITION
           ==================================================== */

        .main {{
            animation:
                fadeIn 0.35s ease;
        }}


        @keyframes fadeIn {{

            from {{
                opacity:
                    0;

                transform:
                    translateY(4px);
            }}

            to {{
                opacity:
                    1;

                transform:
                    translateY(0);
            }}

        }}


        /* ====================================================
           MOBILE
           ==================================================== */

        @media (
            max-width: 768px
        ) {{

            .block-container {{
                padding:
                    1rem;
            }}

            h1 {{
                font-size:
                    30px;
            }}

            h2 {{
                font-size:
                    24px;
            }}

        }}

        </style>
        """
    )


# ============================================================
# PLOTLY THEME
# ============================================================

def apply_plotly_theme(fig, height=430):

    fig.update_layout(

        template="plotly_white",

        height=height,

        font=dict(
            family="Arial, sans-serif",
            color=TEXT
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=15,
            r=15,
            t=25,
            b=15
        ),

        hoverlabel=dict(
            bgcolor=FOREST,
            font_color="white",
            bordercolor=FOREST
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor=BORDER,
            borderwidth=1
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E9EEEB",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E9EEEB",
        zeroline=False
    )

    return fig