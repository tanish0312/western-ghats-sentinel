# ============================================================
# WESTERN GHATS SENTINEL
# PROFESSIONAL PROJECT REPORT GENERATOR
# ============================================================

import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)

OUTPUT_FILE = os.path.join(
    REPORT_DIR,
    "Western_Ghats_Sentinel_Project_Report.pdf"
)


# ============================================================
# 2. PROJECT COLOURS
# ============================================================

FOREST_GREEN = colors.HexColor("#1F4D36")
DEEP_GREEN = colors.HexColor("#163B2A")
LIGHT_GREEN = colors.HexColor("#EAF2EC")

GOLD = colors.HexColor("#B28A45")
CREAM = colors.HexColor("#F7F3EA")

EARTH_BROWN = colors.HexColor("#6F5740")

DARK_TEXT = colors.HexColor("#26332C")
GREY_TEXT = colors.HexColor("#69736D")
LIGHT_GREY = colors.HexColor("#F2F4F2")

WHITE = colors.white


# ============================================================
# 3. DATA LOADING
# ============================================================

def load_csv(filename):
    """
    Load a CSV from the project's data folder.
    Returns an empty DataFrame if the file does not exist.
    """

    filepath = os.path.join(
        DATA_DIR,
        filename
    )

    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found.")
        return pd.DataFrame()

    try:
        return pd.read_csv(filepath)

    except Exception as error:
        print(
            f"Warning: Could not read {filename}: {error}"
        )
        return pd.DataFrame()


# ============================================================
# 4. COLUMN DETECTION
# ============================================================

def find_column(df, candidates):
    """
    Find a column by:
    1. Exact name
    2. Partial name
    """

    if df.empty:
        return None

    columns = list(df.columns)

    # Exact matching
    for candidate in candidates:

        for column in columns:

            if column.lower() == candidate.lower():
                return column

    # Partial matching
    for candidate in candidates:

        for column in columns:

            if candidate.lower() in column.lower():
                return column

    return None


# ============================================================
# 5. SAFE NUMERIC FUNCTIONS
# ============================================================

def to_numeric(series):

    if series is None:
        return pd.Series(dtype=float)

    return pd.to_numeric(
        series,
        errors="coerce"
    )


def safe_sum(series):

    if series is None:
        return 0

    values = to_numeric(series).dropna()

    if values.empty:
        return 0

    return float(values.sum())


def safe_mean(series):

    if series is None:
        return 0

    values = to_numeric(series).dropna()

    if values.empty:
        return 0

    return float(values.mean())


def safe_number(value):

    try:

        value = float(value)

        if pd.isna(value):
            return 0

        return value

    except Exception:

        return 0


def format_number(value, decimals=0):

    value = safe_number(value)

    if decimals == 0:
        return f"{value:,.0f}"

    return f"{value:,.{decimals}f}"


# ============================================================
# 6. CORRELATION
# ============================================================

def calculate_correlation(df, column_a, column_b, method):

    if (
        df.empty
        or column_a is None
        or column_b is None
    ):
        return None

    temp = pd.DataFrame({
        "A": to_numeric(df[column_a]),
        "B": to_numeric(df[column_b])
    }).dropna()

    if len(temp) < 3:
        return None

    try:

        return float(
            temp["A"].corr(
                temp["B"],
                method=method
            )
        )

    except Exception:

        return None


# ============================================================
# 7. LOAD ALL PROJECT DATA
# ============================================================

annual_df = load_csv(
    "ANNUAL_TREE_COVER_LOSS.csv"
)

state_df = load_csv(
    "FINAL_STATE_ANALYSIS.csv"
)

state_year_df = load_csv(
    "STATE_YEAR_TREE_LOSS.csv"
)

species_history_df = load_csv(
    "SPECIES_STATUS_HISTORY.csv"
)

species_trends_df = load_csv(
    "SPECIES_STATUS_TRENDS.csv"
)

species_transitions_df = load_csv(
    "SPECIES_STATUS_TRANSITIONS.csv"
)

lag_df = load_csv(
    "LAG_ANALYSIS.csv"
)


# ============================================================
# 8. IDENTIFY ANNUAL DATA COLUMNS
# ============================================================

annual_year_col = find_column(
    annual_df,
    [
        "year",
        "Year"
    ]
)

annual_loss_col = find_column(
    annual_df,
    [
        "tree_cover_loss_ha",
        "total_loss_ha",
        "loss_ha",
        "tree_cover_loss",
        "loss"
    ]
)


# ============================================================
# 9. IDENTIFY STATE DATA COLUMNS
# ============================================================

state_col = find_column(
    state_df,
    [
        "state",
        "state_name",
        "State"
    ]
)

state_loss_col = find_column(
    state_df,
    [
        "total_loss_ha",
        "tree_cover_loss_ha",
        "loss_ha",
        "total_loss"
    ]
)

state_intensity_col = find_column(
    state_df,
    [
        "loss_per_1000km2",
        "loss_per_1000",
        "loss_intensity"
    ]
)

state_emissions_col = find_column(
    state_df,
    [
        "total_emissions_Mg",
        "total_emissions",
        "emissions_Mg",
        "co2_emissions",
        "emissions"
    ]
)

state_co2ha_col = find_column(
    state_df,
    [
        "Mg_CO2e_per_ha",
        "co2e_per_ha",
        "emissions_per_ha"
    ]
)


# ============================================================
# 10. PREPARE ANNUAL DATA
# ============================================================

if annual_year_col is not None:

    annual_df[annual_year_col] = pd.to_numeric(
        annual_df[annual_year_col],
        errors="coerce"
    )

if annual_loss_col is not None:

    annual_df[annual_loss_col] = pd.to_numeric(
        annual_df[annual_loss_col],
        errors="coerce"
    )


# ============================================================
# 11. EXECUTIVE METRICS
# ============================================================

total_loss = 0
average_annual_loss = 0

start_year = "N/A"
end_year = "N/A"

peak_year = "N/A"
peak_loss = 0


if (
    annual_year_col is not None
    and annual_loss_col is not None
    and not annual_df.empty
):

    valid_annual = annual_df.dropna(
        subset=[
            annual_year_col,
            annual_loss_col
        ]
    ).copy()

    if not valid_annual.empty:

        total_loss = safe_sum(
            valid_annual[annual_loss_col]
        )

        average_annual_loss = safe_mean(
            valid_annual[annual_loss_col]
        )

        start_year = int(
            valid_annual[annual_year_col].min()
        )

        end_year = int(
            valid_annual[annual_year_col].max()
        )

        peak_row = valid_annual.loc[
            valid_annual[annual_loss_col].idxmax()
        ]

        peak_year = int(
            peak_row[annual_year_col]
        )

        peak_loss = safe_number(
            peak_row[annual_loss_col]
        )


# ============================================================
# 12. STATE METRICS
# ============================================================

highest_loss_state = "N/A"
highest_loss_value = 0

highest_intensity_state = "N/A"
highest_intensity_value = 0

highest_emissions_state = "N/A"
highest_emissions_value = 0


# ------------------------------------------------------------
# Highest total loss
# ------------------------------------------------------------

if (
    state_col is not None
    and state_loss_col is not None
    and not state_df.empty
):

    state_df[state_loss_col] = pd.to_numeric(
        state_df[state_loss_col],
        errors="coerce"
    )

    valid_state = state_df.dropna(
        subset=[state_loss_col]
    )

    if not valid_state.empty:

        row = valid_state.loc[
            valid_state[state_loss_col].idxmax()
        ]

        highest_loss_state = str(
            row[state_col]
        )

        highest_loss_value = safe_number(
            row[state_loss_col]
        )


# ------------------------------------------------------------
# Highest intensity
# ------------------------------------------------------------

if (
    state_col is not None
    and state_intensity_col is not None
    and not state_df.empty
):

    state_df[state_intensity_col] = pd.to_numeric(
        state_df[state_intensity_col],
        errors="coerce"
    )

    valid_intensity = state_df.dropna(
        subset=[state_intensity_col]
    )

    if not valid_intensity.empty:

        row = valid_intensity.loc[
            valid_intensity[state_intensity_col].idxmax()
        ]

        highest_intensity_state = str(
            row[state_col]
        )

        highest_intensity_value = safe_number(
            row[state_intensity_col]
        )


# ------------------------------------------------------------
# Highest emissions
# ------------------------------------------------------------

if (
    state_col is not None
    and state_emissions_col is not None
    and not state_df.empty
):

    state_df[state_emissions_col] = pd.to_numeric(
        state_df[state_emissions_col],
        errors="coerce"
    )

    valid_emissions = state_df.dropna(
        subset=[state_emissions_col]
    )

    if not valid_emissions.empty:

        row = valid_emissions.loc[
            valid_emissions[state_emissions_col].idxmax()
        ]

        highest_emissions_state = str(
            row[state_col]
        )

        highest_emissions_value = safe_number(
            row[state_emissions_col]
        )


# ============================================================
# 13. SPECIES METRICS
# ============================================================

species_name_col = find_column(
    species_history_df,
    [
        "species",
        "species_name",
        "scientific_name"
    ]
)

species_status_col = find_column(
    species_history_df,
    [
        "status",
        "conservation_status",
        "iucn_status"
    ]
)


species_count = 0
status_category_count = 0


if species_name_col is not None:

    species_count = (
        species_history_df[species_name_col]
        .dropna()
        .nunique()
    )


if species_status_col is not None:

    status_category_count = (
        species_history_df[species_status_col]
        .dropna()
        .nunique()
    )


# ============================================================
# 14. CORRELATION
# ============================================================

annual_emissions_col = find_column(
    annual_df,
    [
        "total_emissions_Mg",
        "emissions_Mg",
        "emissions",
        "co2",
        "carbon"
    ]
)

spearman_correlation = calculate_correlation(
    annual_df,
    annual_loss_col,
    annual_emissions_col,
    "spearman"
)


pearson_correlation = calculate_correlation(
    annual_df,
    annual_loss_col,
    annual_emissions_col,
    "pearson"
)


# ============================================================
# 15. REPORT STYLES
# ============================================================

styles = getSampleStyleSheet()


title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=28,
    leading=32,
    textColor=WHITE,
    alignment=TA_CENTER,
    spaceAfter=12
)


subtitle_style = ParagraphStyle(
    "SubtitleCustom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=12,
    leading=18,
    textColor=colors.HexColor("#DCE9DF"),
    alignment=TA_CENTER
)


section_style = ParagraphStyle(
    "SectionCustom",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=19,
    leading=24,
    textColor=FOREST_GREEN,
    spaceBefore=12,
    spaceAfter=10
)


subsection_style = ParagraphStyle(
    "SubsectionCustom",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=EARTH_BROWN,
    spaceBefore=10,
    spaceAfter=6
)


body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.7,
    leading=15,
    textColor=DARK_TEXT,
    spaceAfter=8
)


small_style = ParagraphStyle(
    "SmallCustom",
    parent=body_style,
    fontSize=8,
    leading=11,
    textColor=GREY_TEXT
)


bullet_style = ParagraphStyle(
    "BulletCustom",
    parent=body_style,
    leftIndent=14,
    firstLineIndent=-8,
    bulletIndent=5,
    spaceAfter=5
)


highlight_style = ParagraphStyle(
    "HighlightCustom",
    parent=body_style,
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=15,
    textColor=DEEP_GREEN
)


# ============================================================
# 16. PAGE FOOTER
# ============================================================

def add_page_number(canvas, doc):

    canvas.saveState()

    width, height = A4

    canvas.setStrokeColor(
        colors.HexColor("#D9DED9")
    )

    canvas.line(
        2 * cm,
        1.5 * cm,
        width - 2 * cm,
        1.5 * cm
    )

    canvas.setFont(
        "Helvetica",
        7.5
    )

    canvas.setFillColor(
        GREY_TEXT
    )

    canvas.drawString(
        2 * cm,
        1.0 * cm,
        "Western Ghats Sentinel • Tree Cover • Carbon • Conservation"
    )

    canvas.drawRightString(
        width - 2 * cm,
        1.0 * cm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# 17. CREATE PDF DOCUMENT
# ============================================================

document = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm
)


story = []


# ============================================================
# 18. COVER PAGE
# ============================================================

story.append(
    Spacer(
        1,
        2.5 * cm
    )
)


cover_content = Table(
    [
        [
            Paragraph(
                "WESTERN GHATS<br/>SENTINEL",
                title_style
            )
        ],
        [
            Paragraph(
                "Tree Cover • Carbon • Conservation",
                subtitle_style
            )
        ],
        [
            Spacer(
                1,
                0.8 * cm
            )
        ],
        [
            Paragraph(
                "Environmental Intelligence & Data Analytics Report",
                subtitle_style
            )
        ]
    ],
    colWidths=[
        16 * cm
    ]
)


cover_content.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            DEEP_GREEN
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            15
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            15
        )
    ])
)


story.append(
    cover_content
)

story.append(
    Spacer(
        1,
        1 * cm
    )
)


story.append(
    Paragraph(
        "<b>Study Region:</b> Karnataka • Kerala • Tamil Nadu • Goa • Maharashtra",
        body_style
    )
)

story.append(
    Paragraph(
        f"<b>Analysis Period:</b> {start_year} – {end_year}",
        body_style
    )
)

story.append(
    Paragraph(
        "<b>Analytical Focus:</b> Forest loss • Carbon • Spatial intensity • Conservation",
        body_style
    )
)

story.append(
    Spacer(
        1,
        4 * cm
    )
)

story.append(
    Paragraph(
        "Prepared as a data analytics and environmental intelligence project.",
        small_style
    )
)

story.append(
    PageBreak()
)


# ============================================================
# 19. EXECUTIVE SUMMARY
# ============================================================

story.append(
    Paragraph(
        "1. Executive Summary",
        section_style
    )
)

story.append(
    Paragraph(
        """
        <b>Western Ghats Sentinel</b> is an interactive environmental
        analytics project designed to examine tree-cover loss,
        carbon-related indicators, spatial patterns and conservation
        information across five states associated with the Western Ghats:
        Karnataka, Kerala, Tamil Nadu, Goa and Maharashtra.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        f"""
        The available annual dataset covers <b>{start_year}–{end_year}</b>
        and records approximately <b>{format_number(total_loss)} hectares</b>
        of tree-cover loss. The average annual loss is approximately
        <b>{format_number(average_annual_loss)} hectares</b>.
        """,
        body_style
    )
)

summary_table_data = [
    ["Indicator", "Result"],
    [
        "Total tree-cover loss",
        f"{format_number(total_loss)} ha"
    ],
    [
        "Average annual loss",
        f"{format_number(average_annual_loss)} ha"
    ],
    [
        "Peak loss year",
        str(peak_year)
    ],
    [
        "Peak annual loss",
        f"{format_number(peak_loss)} ha"
    ],
    [
        "Highest total-loss state",
        highest_loss_state
    ],
    [
        "Highest loss-intensity state",
        highest_intensity_state
    ],
    [
        "Highest emissions state",
        highest_emissions_state
    ],
    [
        "Species represented",
        str(species_count)
    ]
]


summary_table = Table(
    summary_table_data,
    colWidths=[
        8 * cm,
        8 * cm
    ]
)


summary_table.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            FOREST_GREEN
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            WHITE
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),
        (
            "FONTNAME",
            (0, 1),
            (0, -1),
            "Helvetica-Bold"
        ),
        (
            "BACKGROUND",
            (0, 1),
            (-1, -1),
            LIGHT_GREY
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.4,
            WHITE
        ),
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            9
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            7
        )
    ])
)


story.append(
    summary_table
)


# ============================================================
# 20. PROJECT OBJECTIVE
# ============================================================

story.append(
    Paragraph(
        "2. Project Objective",
        section_style
    )
)

story.append(
    Paragraph(
        """
        The project transforms environmental datasets into an
        interactive analytical system that allows users to investigate
        forest-loss patterns, compare states, understand normalized
        spatial intensity, examine carbon-related indicators and
        explore conservation-status information.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        "Primary objectives",
        subsection_style
    )
)


objectives = [
    "Measure annual tree-cover loss across the available study period.",
    "Compare tree-cover loss between the five study states.",
    "Normalize loss using state-level area to provide spatial intensity.",
    "Examine carbon and CO₂-related indicators associated with forest loss.",
    "Explore temporal conservation-status information.",
    "Investigate statistical relationships and lagged associations.",
    "Present the results through an interactive Streamlit dashboard."
]


for item in objectives:

    story.append(
        Paragraph(
            f"• {item}",
            bullet_style
        )
    )


# ============================================================
# 21. RESEARCH QUESTIONS
# ============================================================

story.append(
    Paragraph(
        "3. Research Questions",
        section_style
    )
)


research_questions = [
    "How has tree-cover loss changed over the analysis period?",
    "How does forest loss differ among the five study states?",
    "Which states show greater loss intensity after area normalization?",
    "How are tree-cover loss and carbon-related indicators associated?",
    "What temporal patterns are visible in conservation-status data?",
    "Are there observable lagged relationships between environmental indicators?",
    "What can the available datasets reveal, and what are their analytical boundaries?"
]


for question in research_questions:

    story.append(
        Paragraph(
            f"• {question}",
            bullet_style
        )
    )


# ============================================================
# 22. STUDY REGION
# ============================================================

story.append(
    Paragraph(
        "4. Study Region",
        section_style
    )
)

story.append(
    Paragraph(
        """
        The geographical focus of this project is the Western Ghats
        study region represented through five Indian states:
        <b>Karnataka, Kerala, Tamil Nadu, Goa and Maharashtra</b>.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        The spatial component uses polygon boundaries representing
        the study states. District-level boundary information is also
        available in the underlying spatial data; however, the
        tree-cover-loss observations used for the principal state-level
        analysis are aggregated at the state level.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        Therefore, state-level results should not be interpreted as
        district-level tree-cover-loss estimates.
        """,
        body_style
    )
)


# ============================================================
# 23. DATASET ARCHITECTURE
# ============================================================

story.append(
    Paragraph(
        "5. Data & Dataset Architecture",
        section_style
    )
)


dataset_rows = [
    [
        "Dataset",
        "Analytical purpose"
    ],
    [
        "FOREST_RAW_DATA.csv",
        "Underlying forest/environmental observations"
    ],
    [
        "ANNUAL_TREE_COVER_LOSS.csv",
        "Annual tree-cover-loss analysis"
    ],
    [
        "STATE_YEAR_TREE_LOSS.csv",
        "State-by-year forest-loss analysis"
    ],
    [
        "FINAL_STATE_ANALYSIS.csv",
        "State-level environmental indicators"
    ],
    [
        "SPECIES_STATUS_HISTORY.csv",
        "Historical species conservation-status records"
    ],
    [
        "SPECIES_STATUS_TRENDS.csv",
        "Species-status trend analysis"
    ],
    [
        "SPECIES_STATUS_TRANSITIONS.csv",
        "Conservation-status transition analysis"
    ],
    [
        "LAG_ANALYSIS.csv",
        "Lagged relationship analysis"
    ],
    [
        "map_complete.geojson",
        "Spatial boundary and mapping layer"
    ]
]


dataset_table = Table(
    dataset_rows,
    colWidths=[
        7 * cm,
        9 * cm
    ]
)


dataset_table.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            FOREST_GREEN
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            WHITE
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),
        (
            "BACKGROUND",
            (0, 1),
            (-1, -1),
            LIGHT_GREY
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.4,
            WHITE
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP"
        ),
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            8.5
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6
        )
    ])
)


story.append(
    dataset_table
)


# ============================================================
# 24. DATA PREPARATION
# ============================================================

story.append(
    Paragraph(
        "6. Data Preparation & Validation",
        section_style
    )
)

story.append(
    Paragraph(
        """
        Data preparation involved loading the source datasets,
        standardizing analytical fields, aggregating state-level
        observations and preparing spatial information for visualization.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        "Spatial validation",
        subsection_style
    )
)

story.append(
    Paragraph(
        """
        A key spatial-validation step was required because the original
        geographic data contained multiple district polygons while the
        tree-cover-loss values were available at state level.
        Directly joining state-level totals to district geometries would
        repeat the same state value across multiple polygons.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        To address this, district geometries were dissolved into a
        single polygon per state before the state-level environmental
        totals were joined. This prevents duplicated state totals in
        the mapped analysis.
        """,
        body_style
    )
)
story.append(
    Paragraph(
        """
        Area calculations use an equal-area coordinate reference system
        so that the normalized loss-intensity indicator is based on
        projected area rather than unprojected geographic coordinates.
        """,
        body_style
    )
)


# ============================================================
# 25. SPATIAL METHODOLOGY
# ============================================================

story.append(
    Paragraph(
        "7. Spatial Methodology",
        section_style
    )
)

spatial_methods = [
    "State geometries are dissolved before state-level totals are joined.",
    "Area is calculated using an equal-area coordinate reference system.",
    "Loss intensity is expressed as tree-cover loss per 1,000 km².",
    "Carbon-related indicators are displayed alongside forest-loss measures.",
    "The spatial explorer provides state-level visual comparison."
]


for method in spatial_methods:

    story.append(
        Paragraph(
            f"• {method}",
            bullet_style
        )
    )


# ============================================================
# 26. FOREST LOSS ANALYSIS
# ============================================================

story.append(
    Paragraph(
        "8. Forest-Loss Analysis",
        section_style
    )
)

story.append(
    Paragraph(
        f"""
        Across the available annual data, the project records
        approximately <b>{format_number(total_loss)} hectares</b> of
        tree-cover loss during the analysis period. The average annual
        loss is approximately <b>{format_number(average_annual_loss)}
        hectares</b>.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        f"""
        The highest annual loss occurs in <b>{peak_year}</b>, with
        approximately <b>{format_number(peak_loss)} hectares</b>
        recorded for that year.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        f"""
        At the state level, <b>{highest_loss_state}</b> records the
        highest total tree-cover loss in the available state-level
        analysis, at approximately
        <b>{format_number(highest_loss_value)} hectares</b>.
        """,
        body_style
    )
)


# ============================================================
# 27. CARBON & EMISSIONS
# ============================================================

story.append(
    Paragraph(
        "9. Carbon & Emissions Analysis",
        section_style
    )
)

story.append(
    Paragraph(
        f"""
        The state-level dataset includes estimated emissions indicators
        associated with the environmental analysis. Within that dataset,
        <b>{highest_emissions_state}</b> records the highest total
        emissions value, approximately
        <b>{format_number(highest_emissions_value)} Mg</b>.
        """,
        body_style
    )
)


if spearman_correlation is not None:

    story.append(
        Paragraph(
            f"""
            The available annual data produces a Spearman correlation
            of approximately <b>{spearman_correlation:.3f}</b> between
            tree-cover loss and the identified emissions indicator.
            """,
            body_style
        )
    )

else:

    story.append(
        Paragraph(
            """
            A directly compatible annual emissions column was not
            identified for the automated annual correlation calculation.
            The state-level emissions indicators remain available for
            descriptive comparison.
            """,
            body_style
        )
    )


if pearson_correlation is not None:

    story.append(
        Paragraph(
            f"""
            The corresponding Pearson correlation is approximately
            <b>{pearson_correlation:.3f}</b>.
            """,
            body_style
        )
    )


story.append(
    Paragraph(
        """
        Correlation describes statistical association. It does not by
        itself establish that one environmental variable causes another.
        """,
        body_style
    )
)


# ============================================================
# 28. CONSERVATION ANALYSIS
# ============================================================

story.append(
    Paragraph(
        "10. Conservation Analysis",
        section_style
    )
)

story.append(
    Paragraph(
        f"""
        The conservation component contains historical species-status
        information representing approximately <b>{species_count}
        unique species</b> across <b>{status_category_count}
        status categories</b> in the available history dataset.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        The dashboard examines status distributions, historical
        records, conservation trajectories and status transitions
        where supported by the available datasets.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        These records provide temporal conservation context but do not
        establish that forest loss caused a particular species-status
        change. Species geographic-range information is not included
        in the analytical dataset, so direct habitat-loss attribution
        cannot be established from these records alone.
        """,
        body_style
    )
)


# ============================================================
# 29. RELATIONSHIP & LAG ANALYSIS
# ============================================================

story.append(
    Paragraph(
        "11. Relationship & Lag Analysis",
        section_style
    )
)

relationship_points = [
    "Annual tree-cover loss and emissions are compared statistically where compatible fields are available.",
    "Pearson correlation measures linear association.",
    "Spearman correlation measures monotonic association.",
    "State-level relationships provide a cross-sectional comparison.",
    "Lag analysis examines relationships at different temporal offsets.",
    "Statistical association is not treated as proof of causation."
]


for point in relationship_points:

    story.append(
        Paragraph(
            f"• {point}",
            bullet_style
        )
    )


# ============================================================
# 30. KEY FINDINGS
# ============================================================

story.append(
    PageBreak()
)

story.append(
    Paragraph(
        "12. Key Findings",
        section_style
    )
)


findings = [
    (
        "Forest-loss scale",
        f"The available dataset records approximately "
        f"{format_number(total_loss)} hectares of tree-cover loss."
    ),
    (
        "Peak year",
        f"The highest annual loss occurs in {peak_year}, "
        f"with approximately {format_number(peak_loss)} hectares."
    ),
    (
        "State comparison",
        f"{highest_loss_state} records the highest total "
        f"tree-cover loss among the five study states."
    ),
    (
        "Spatial intensity",
        f"{highest_intensity_state} records the highest "
        f"normalized loss intensity in the state-level dataset."
    ),
    (
        "Carbon pressure",
        f"{highest_emissions_state} records the highest total "
        f"emissions indicator in the state-level dataset."
    ),
    (
        "Conservation context",
        f"The conservation history dataset represents approximately "
        f"{species_count} unique species across "
        f"{status_category_count} status categories."
    )
]


for title, description in findings:

    finding_table = Table(
        [
            [
                Paragraph(
                    f"<b>{title}</b>",
                    highlight_style
                ),
                Paragraph(
                    description,
                    body_style
                )
            ]
        ],
        colWidths=[
            4.2 * cm,
            11.8 * cm
        ]
    )

    finding_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, 0),
                LIGHT_GREEN
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, 0),
                WHITE
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#D6DED7")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    story.append(
        finding_table
    )

    story.append(
        Spacer(
            1,
            0.25 * cm
        )
    )


# ============================================================
# 31. APPLICATION ARCHITECTURE
# ============================================================

story.append(
    Paragraph(
        "13. Application Architecture",
        section_style
    )
)


architecture_rows = [
    [
        "Layer",
        "Technology / implementation"
    ],
    [
        "Application interface",
        "Streamlit"
    ],
    [
        "Data processing",
        "Python + Pandas"
    ],
    [
        "Spatial analysis",
        "GeoPandas"
    ],
    [
        "Interactive visualization",
        "Plotly"
    ],
    [
        "Spatial data",
        "GeoJSON"
    ],
    [
        "Statistical analysis",
        "Pandas / numerical analysis"
    ],
    [
        "Report generation",
        "ReportLab"
    ],
    [
        "Data storage",
        "CSV + GeoJSON"
    ]
]


architecture_table = Table(
    architecture_rows,
    colWidths=[
        6 * cm,
        10 * cm
    ]
)


architecture_table.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            FOREST_GREEN
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            WHITE
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),
        (
            "BACKGROUND",
            (0, 1),
            (-1, -1),
            LIGHT_GREY
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.4,
            WHITE
        ),
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            9
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            7
        )
    ])
)


story.append(
    architecture_table
)


# ============================================================
# 32. TECHNOLOGY STACK
# ============================================================

story.append(
    Paragraph(
        "14. Technology Stack",
        section_style
    )
)


technologies = [
    "Python",
    "Streamlit",
    "Pandas",
    "GeoPandas",
    "Plotly",
    "ReportLab",
    "CSV",
    "GeoJSON",
    "HTML/CSS styling"
]


for technology in technologies:

    story.append(
        Paragraph(
            f"• {technology}",
            bullet_style
        )
    )


# ============================================================
# 33. LIMITATIONS
# ============================================================

story.append(
    PageBreak()
)

story.append(
    Paragraph(
        "15. Research Limitations",
        section_style
    )
)


limitations = [
    "Tree-cover-loss observations are represented at state level.",
    "State-level results should not be interpreted as district-level estimates.",
    "Correlation does not establish causation.",
    "Lagged statistical relationships do not independently establish causal mechanisms.",
    "The conservation dataset does not contain species geographic-range information.",
    "Species-status associations therefore cannot be treated as direct habitat-loss attribution.",
    "Environmental indicators may represent different measurement concepts and should be interpreted according to their source definitions.",
    "The dashboard is an analytical representation of the available datasets and is not a complete ecological assessment of the Western Ghats."
]


for limitation in limitations:

    story.append(
        Paragraph(
            f"• {limitation}",
            bullet_style
        )
    )


# ============================================================
# 34. FUTURE SCOPE
# ============================================================

story.append(
    Paragraph(
        "16. Future Scope",
        section_style
    )
)


future_scope = [
    "Integrate additional satellite-derived environmental indicators.",
    "Add district-level forest-loss data where compatible datasets are available.",
    "Integrate species geographic-range or habitat-distribution data.",
    "Add protected-area and biodiversity-hotspot boundaries.",
    "Introduce more advanced spatial statistics.",
    "Develop automated data-refresh pipelines.",
    "Add scenario modelling and forecasting where scientifically appropriate.",
    "Deploy the dashboard publicly through Streamlit Community Cloud.",
    "Enable user-selectable report generation directly from the dashboard."
]


for item in future_scope:

    story.append(
        Paragraph(
            f"• {item}",
            bullet_style
        )
    )


# ============================================================
# 35. CONCLUSION
# ============================================================

story.append(
    Paragraph(
        "17. Conclusion",
        section_style
    )
)

story.append(
    Paragraph(
        """
        Western Ghats Sentinel demonstrates how environmental datasets
        can be transformed into an interactive data-storytelling and
        analytical system. The project combines forest-loss analysis,
        spatial comparison, carbon-related indicators, conservation
        information and statistical relationships within a single
        application.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        Rather than relying on a single environmental indicator, the
        project combines multiple measures to provide broader analytical
        context. The methodology also distinguishes observed patterns
        and statistical associations from causal conclusions.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        """
        The resulting system provides a foundation for further
        environmental analytics, spatial research and data-driven
        conservation investigation.
        """,
        body_style
    )

)
# ============================================================
# 36. FINAL PROJECT BOX
# ============================================================

story.append(
    Spacer(
        1,
        1 * cm
    )
)


final_box = Table(
    [
        [
            Paragraph(
                "<b>WESTERN GHATS SENTINEL</b><br/>"
                "Tree Cover • Carbon • Conservation",
                highlight_style
            )
        ]
    ],
    colWidths=[
        16 * cm
    ]
)


final_box.setStyle(
    TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            LIGHT_GREEN
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.7,
            FOREST_GREEN
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            14
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            14
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            12
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            12
        )
    ])
)


story.append(
    final_box
)


# ============================================================
# 37. BUILD THE PDF
# ============================================================

try:

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    print()
    print("=" * 60)
    print("WESTERN GHATS SENTINEL")
    print("PROJECT REPORT")
    print("=" * 60)
    print()
    print("SUCCESS!")
    print()
    print("Your PDF has been generated at:")
    print()
    print(OUTPUT_FILE)
    print()
    print("=" * 60)

except Exception as error:

    print()
    print("=" * 60)
    print("REPORT GENERATION FAILED")
    print("=" * 60)
    print()
    print("Error:")
    print(error)
    print()
    print("=" * 60)