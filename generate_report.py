# ============================================================
# WESTERN GHATS SENTINEL
# SPECIES-FOCUSED CONSERVATION & BIODIVERSITY REPORT GENERATOR
# ============================================================

import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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
    KeepTogether,
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
    "Western_Ghats_Sentinel_Species_Conservation_Report.pdf"
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

CRITICAL_RED = colors.HexColor("#A83232")
WARNING_ORANGE = colors.HexColor("#D97724")

WHITE = colors.white


# ============================================================
# 3. DATA LOADING
# ============================================================

def load_csv(filename):
    """
    Load a CSV from the project's data folder.
    Returns an empty DataFrame if the file does not exist.
    """
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found.")
        return pd.DataFrame()

    try:
        return pd.read_csv(filepath)
    except Exception as error:
        print(f"Warning: Could not read {filename}: {error}")
        return pd.DataFrame()


# ============================================================
# 4. COLUMN DETECTION & HELPER FUNCTIONS
# ============================================================

def find_column(df, candidates):
    """Find a column by exact or partial name matching."""
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


def to_numeric(series):
    if series is None:
        return pd.Series(dtype=float)
    return pd.to_numeric(series, errors="coerce")


def safe_sum(series):
    if series is None:
        return 0
    values = to_numeric(series).dropna()
    return float(values.sum()) if not values.empty else 0


def safe_mean(series):
    if series is None:
        return 0
    values = to_numeric(series).dropna()
    return float(values.mean()) if not values.empty else 0


def safe_number(value):
    try:
        val = float(value)
        return 0 if pd.isna(val) else val
    except Exception:
        return 0


def format_number(value, decimals=0):
    val = safe_number(value)
    if decimals == 0:
        return f"{val:,.0f}"
    return f"{val:,.{decimals}f}"


def calculate_correlation(df, column_a, column_b, method):
    if df.empty or column_a is None or column_b is None:
        return None

    temp = pd.DataFrame({
        "A": to_numeric(df[column_a]),
        "B": to_numeric(df[column_b])
    }).dropna()

    if len(temp) < 3:
        return None

    try:
        return float(temp["A"].corr(temp["B"], method=method))
    except Exception:
        return None


# ============================================================
# 5. LOAD ALL PROJECT DATA
# ============================================================

annual_df = load_csv("ANNUAL_TREE_COVER_LOSS.csv")
state_df = load_csv("FINAL_STATE_ANALYSIS.csv")
state_year_df = load_csv("STATE_YEAR_TREE_LOSS.csv")
species_history_df = load_csv("SPECIES_STATUS_HISTORY.csv")
species_trends_df = load_csv("SPECIES_STATUS_TRENDS.csv")
species_transitions_df = load_csv("SPECIES_STATUS_TRANSITIONS.csv")
lag_df = load_csv("LAG_ANALYSIS.csv")
district_df = load_csv("DISTRICT_YEAR_TREE_LOSS.csv")


# ============================================================
# 6. SPECIES DATA METRICS (PRIMARY FOCUS)
# ============================================================

species_name_col = find_column(
    species_history_df,
    ["species", "species_name", "scientific_name", "common_name", "name"]
)

species_status_col = find_column(
    species_history_df,
    ["status", "conservation_status", "iucn_status", "category", "red_list_status"]
)

species_year_col = find_column(
    species_history_df,
    ["year", "assessment_year", "date"]
)

total_species_monitored = 0
status_category_count = 0
status_distribution = {}
threatened_species_count = 0
critically_endangered_count = 0
endangered_count = 0
vulnerable_count = 0

if not species_history_df.empty and species_name_col:
    total_species_monitored = species_history_df[species_name_col].dropna().nunique()

if not species_history_df.empty and species_status_col:
    # Get latest status per species
    if species_year_col:
        species_history_df[species_year_col] = pd.to_numeric(species_history_df[species_year_col], errors="coerce")
        latest_species_df = species_history_df.sort_values(species_year_col).groupby(species_name_col).last().reset_index()
    else:
        latest_species_df = species_history_df.groupby(species_name_col).last().reset_index()

    status_counts = latest_species_df[species_status_col].value_counts()
    status_distribution = status_counts.to_dict()
    status_category_count = len(status_counts)

    # Categorize threat levels
    for status, count in status_distribution.items():
        st_upper = str(status).upper()
        if "CRITICAL" in st_upper or st_upper == "CR":
            critically_endangered_count += count
            threatened_species_count += count
        elif "ENDANGERED" in st_upper or st_upper == "EN":
            endangered_count += count
            threatened_species_count += count
        elif "VULNERABLE" in st_upper or st_upper == "VU":
            vulnerable_count += count
            threatened_species_count += count

# Transitions analysis
total_transitions = len(species_transitions_df) if not species_transitions_df.empty else 0
trans_species_col = find_column(species_transitions_df, ["species", "species_name", "scientific_name"])
trans_from_col = find_column(species_transitions_df, ["from_status", "initial_status", "from", "previous_status"])
trans_to_col = find_column(species_transitions_df, ["to_status", "current_status", "to", "new_status"])

# Trends analysis
declining_species_count = 0
stable_species_count = 0
increasing_species_count = 0
trend_col = find_column(species_trends_df, ["trend", "status_trend", "population_trend", "change", "direction"])

if not species_trends_df.empty and trend_col:
    trend_counts = species_trends_df[trend_col].astype(str).str.upper().value_counts()
    for tr, c in trend_counts.items():
        if "DECLIN" in tr or "DETERIORAT" in tr or "DOWN" in tr or "NEGATIVE" in tr:
            declining_species_count += c
        elif "STABLE" in tr or "NEUTRAL" in tr:
            stable_species_count += c
        elif "INCREAS" in tr or "IMPROV" in tr or "UP" in tr or "POSITIVE" in tr:
            increasing_species_count += c

species_image_count = 0
if species_name_col and os.path.isdir("images"):
    image_files = {os.path.splitext(f)[0].lower() for f in os.listdir("images")}
    species_keys = {
        str(s).strip().lower().replace(" ", "_")
        for s in species_history_df[species_name_col].dropna().unique()
    }
    species_image_count = len(image_files & species_keys)


# ============================================================
# 7. HABITAT LOSS & ENVIRONMENTAL METRICS
# ============================================================

annual_year_col = find_column(annual_df, ["year", "Year"])
annual_loss_col = find_column(
    annual_df,
    ["tree_cover_loss_ha", "total_loss_ha", "loss_ha", "tree_cover_loss", "loss"]
)

total_loss = 0
average_annual_loss = 0
start_year = "N/A"
end_year = "N/A"
peak_year = "N/A"
peak_loss = 0

if annual_year_col and annual_loss_col and not annual_df.empty:
    annual_df[annual_year_col] = pd.to_numeric(annual_df[annual_year_col], errors="coerce")
    annual_df[annual_loss_col] = pd.to_numeric(annual_df[annual_loss_col], errors="coerce")
    valid_annual = annual_df.dropna(subset=[annual_year_col, annual_loss_col]).copy()

    if not valid_annual.empty:
        total_loss = safe_sum(valid_annual[annual_loss_col])
        average_annual_loss = safe_mean(valid_annual[annual_loss_col])
        start_year = int(valid_annual[annual_year_col].min())
        end_year = int(valid_annual[annual_year_col].max())

        peak_row = valid_annual.loc[valid_annual[annual_loss_col].idxmax()]
        peak_year = int(peak_row[annual_year_col])
        peak_loss = safe_number(peak_row[annual_loss_col])

state_col = find_column(state_df, ["state", "state_name", "State"])
state_loss_col = find_column(state_df, ["total_loss_ha", "tree_cover_loss_ha", "loss_ha", "total_loss"])
state_intensity_col = find_column(state_df, ["loss_per_1000km2", "loss_per_1000", "loss_intensity"])
state_emissions_col = find_column(state_df, ["total_emissions_Mg", "total_emissions", "emissions_Mg", "co2_emissions"])

highest_loss_state, highest_loss_value = "N/A", 0
highest_intensity_state, highest_intensity_value = "N/A", 0

if state_col and state_loss_col and not state_df.empty:
    state_df[state_loss_col] = pd.to_numeric(state_df[state_loss_col], errors="coerce")
    valid_state = state_df.dropna(subset=[state_loss_col])
    if not valid_state.empty:
        row = valid_state.loc[valid_state[state_loss_col].idxmax()]
        highest_loss_state, highest_loss_value = str(row[state_col]), safe_number(row[state_loss_col])

if state_col and state_intensity_col and not state_df.empty:
    state_df[state_intensity_col] = pd.to_numeric(state_df[state_intensity_col], errors="coerce")
    valid_intensity = state_df.dropna(subset=[state_intensity_col])
    if not valid_intensity.empty:
        row = valid_intensity.loc[valid_intensity[state_intensity_col].idxmax()]
        highest_intensity_state, highest_intensity_value = str(row[state_col]), safe_number(row[state_intensity_col])


# ============================================================
# 8. REPORT STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=26,
    leading=30,
    textColor=WHITE,
    alignment=TA_CENTER,
    spaceAfter=10
)

subtitle_style = ParagraphStyle(
    "SubtitleCustom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11.5,
    leading=16,
    textColor=colors.HexColor("#DCE9DF"),
    alignment=TA_CENTER
)

section_style = ParagraphStyle(
    "SectionCustom",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=22,
    textColor=FOREST_GREEN,
    spaceBefore=14,
    spaceAfter=8
)

subsection_style = ParagraphStyle(
    "SubsectionCustom",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12.5,
    leading=16,
    textColor=EARTH_BROWN,
    spaceBefore=10,
    spaceAfter=5
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=14.5,
    textColor=DARK_TEXT,
    spaceAfter=7
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
    spaceAfter=4
)

highlight_style = ParagraphStyle(
    "HighlightCustom",
    parent=body_style,
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=14,
    textColor=DEEP_GREEN
)


# ============================================================
# 9. PAGE FOOTER
# ============================================================

def add_page_number(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#D9DED9"))
    canvas.line(2 * cm, 1.5 * cm, width - 2 * cm, 1.5 * cm)

    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(
        2 * cm,
        1.0 * cm,
        "Western Ghats Sentinel • Species Conservation & Threat Assessment Report"
    )
    canvas.drawRightString(width - 2 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


# ============================================================
# 10. CREATE PDF DOCUMENT
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
# 11. COVER PAGE (SPECIES FOCUSED)
# ============================================================

story.append(Spacer(1, 2 * cm))

cover_content = Table(
    [
        [Paragraph("WESTERN GHATS SENTINEL", title_style)],
        [Paragraph("Species Biodiversity & Threat Dynamics Assessment", subtitle_style)],
        [Spacer(1, 0.6 * cm)],
        [Paragraph("A Comprehensive Species Risk, IUCN Red List Trajectory & Habitat Loss Analysis", subtitle_style)]
    ],
    colWidths=[16 * cm]
)

cover_content.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEP_GREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18)
    ])
)

story.append(cover_content)
story.append(Spacer(1, 1 * cm))

story.append(Paragraph("<b>Primary Analytical Focus:</b> Species Conservation Status • Risk Trajectories • Population Trends", body_style))
story.append(Paragraph("<b>Study Region:</b> Western Ghats Hotspot (Karnataka • Kerala • Tamil Nadu • Goa • Maharashtra)", body_style))
story.append(Paragraph(f"<b>Contextual Period:</b> {start_year} – {end_year}", body_style))
story.append(Paragraph(f"<b>Monitored Taxa Count:</b> {total_species_monitored} Endemic & Key Indicator Species", body_style))

story.append(Spacer(1, 3.5 * cm))
story.append(Paragraph("Prepared by Western Ghats Sentinel Biodiversity Analytics Engine.", small_style))
story.append(PageBreak())


# ============================================================
# 12. EXECUTIVE SUMMARY (SPECIES FOCUSED)
# ============================================================

story.append(Paragraph("1. Executive Summary", section_style))

story.append(
    Paragraph(
        """
        <b>Western Ghats Sentinel</b> is a specialized biodiversity and environmental analytics system 
        focused on evaluating <b>species conservation status, IUCN Red List risk transitions, population trends, 
        and habitat deforestation threats</b> across five Western Ghats states: Karnataka, Kerala, Tamil Nadu, 
        Goa, and Maharashtra.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        f"""
        The project monitors <b>{total_species_monitored} key species</b> across <b>{status_category_count} IUCN Red List 
        status categories</b>. Among monitored species, <b>{threatened_species_count}</b> are classified under high-risk 
        threat categories (Critically Endangered, Endangered, or Vulnerable). These species face compounding pressure 
        from ongoing forest loss, which has accumulated to <b>{format_number(total_loss)} hectares</b> across the region.
        """,
        body_style
    )
)

summary_table_data = [
    ["Biodiversity & Environmental Indicator", "Observed Value"],
    ["Total Monitored Species", f"{total_species_monitored} species"],
    ["Threatened Species (CR + EN + VU)", f"{threatened_species_count} species"],
    ["Critically Endangered (CR) Species", f"{critically_endangered_count} species"],
    ["Endangered (EN) Species", f"{endangered_count} species"],
    ["Vulnerable (VU) Species", f"{vulnerable_count} species"],
    ["Recorded Species Status Transitions", f"{total_transitions} status shifts"],
    ["Declining Species Population Trends", f"{declining_species_count} species"],
    ["Total Regional Tree-Cover Loss", f"{format_number(total_loss)} ha"],
    ["Highest Forest-Loss Intensity State", highest_intensity_state]
]

summary_table = Table(summary_table_data, colWidths=[8.5 * cm, 7.5 * cm])
summary_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), FOREST_GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
        ("GRID", (0, 0), (-1, -1), 0.4, WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
    ])
)

story.append(summary_table)


# ============================================================
# 13. SPECIES BIODIVERSITY & RISK ANALYSIS (CORE SECTION)
# ============================================================

story.append(Paragraph("2. Species Biodiversity & Conservation Status", section_style))

story.append(
    Paragraph(
        """
        The Western Ghats is one of the world's eight 'hottest hotspots' of biological diversity, harboring 
        thousands of endemic flora and fauna species. This analysis evaluates the conservation status 
        distribution using historical and contemporary IUCN Red List assessment records.
        """,
        body_style
    )
)

story.append(Paragraph("IUCN Red List Category Breakdown", subsection_style))

if status_distribution:
    status_rows = [["IUCN Status Category", "Species Count", "Percentage of Monitored Taxa"]]
    for status_cat, count in status_distribution.items():
        pct = (count / total_species_monitored * 100) if total_species_monitored > 0 else 0
        status_rows.append([str(status_cat), str(count), f"{pct:.1f}%"])

    status_table = Table(status_rows, colWidths=[7 * cm, 4.5 * cm, 4.5 * cm])
    status_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DEEP_GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
            ("GRID", (0, 0), (-1, -1), 0.4, WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )
    story.append(status_table)
else:
    story.append(Paragraph("Species status breakdown data is currently unavailable.", body_style))


# ============================================================
# 14. SPECIES TRANSITION & THREAT DYNAMICS
# ============================================================

story.append(Paragraph("3. Species Status Transitions & Escalation", section_style))

story.append(
    Paragraph(
        """
        Tracking changes in species risk categories over time provides vital early warning signals for conservation. 
        A negative transition (e.g., Vulnerable to Endangered) indicates worsening habitat conditions, reduced 
        population viability, or increased anthropogenic pressure.
        """,
        body_style
    )
)

if not species_transitions_df.empty and trans_species_col and trans_from_col and trans_to_col:
    story.append(Paragraph("Key Monitored Conservation Transitions", subsection_style))
    
    trans_rows = [["Species Name", "Previous Status", "New Assessment Status"]]
    sample_trans = species_transitions_df.dropna(subset=[trans_species_col, trans_from_col, trans_to_col]).head(10)
    
    for _, r in sample_trans.iterrows():
        trans_rows.append([
            str(r[trans_species_col]),
            str(r[trans_from_col]),
            str(r[trans_to_col])
        ])

    trans_table = Table(trans_rows, colWidths=[6.5 * cm, 4.75 * cm, 4.75 * cm])
    trans_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), FOREST_GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
            ("GRID", (0, 0), (-1, -1), 0.4, WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )
    story.append(trans_table)
else:
    story.append(Paragraph("Detailed species status transition records were not detected in the dataset.", body_style))


# ============================================================
# 15. POPULATION TRENDS & VULNERABILITY
# ============================================================

story.append(Paragraph("4. Species Population Trends", section_style))

story.append(
    Paragraph(
        f"""
        Evaluating population directionalities reveals underlying ecosystem health. Of the species evaluated 
        in the trends dataset, <b>{declining_species_count} species</b> show declining population trajectories, 
        while <b>{stable_species_count} species</b> remain stable and <b>{increasing_species_count} species</b> show positive recovery.
        """,
        body_style
    )
)

trend_summary_points = [
    f"<b>Declining Populations:</b> {declining_species_count} species are experiencing ongoing numbers contraction.",
    f"<b>Stable Populations:</b> {stable_species_count} species maintain steady population baselines.",
    f"<b>Recovering/Increasing Taxa:</b> {increasing_species_count} species benefit from active conservation interventions."
]

for pt in trend_summary_points:
    story.append(Paragraph(f"• {pt}", bullet_style))


# ============================================================
# 16. HABITAT DEFORESTATION & SPECIES THREAT OVERLAY
# ============================================================

story.append(PageBreak())

story.append(Paragraph("5. Forest Loss & Habitat Pressure Overlay", section_style))

story.append(
    Paragraph(
        f"""
        Tree-cover loss represents a primary driver of habitat fragmentation, territorial displacement, 
        and population isolation for endemic species in the Western Ghats. Between <b>{start_year}</b> and 
        <b>{end_year}</b>, total tree-cover loss reached <b>{format_number(total_loss)} hectares</b>, averaging 
        <b>{format_number(average_annual_loss)} hectares per year</b>.
        """,
        body_style
    )
)

story.append(
    Paragraph(
        f"""
        The highest annual forest loss occurred in <b>{peak_year}</b> ({format_number(peak_loss)} ha lost). 
        Among the study states, <b>{highest_loss_state}</b> experienced the highest total loss ({format_number(highest_loss_value)} ha), 
        while <b>{highest_intensity_state}</b> demonstrated the greatest normalized spatial loss intensity.
        """,
        body_style
    )
)


# ============================================================
# 17. RESEARCH QUESTIONS (SPECIES FOCUS)
# ============================================================

story.append(Paragraph("6. Key Research & Conservation Questions", section_style))

species_research_questions = [
    "Which endemic species are experiencing the fastest escalation in IUCN risk levels?",
    "How does regional tree-cover loss correlate with species population declines?",
    "Which Western Ghats states host the highest density of threatened (CR/EN/VU) species?",
    "Are species risk level transitions lagged relative to major deforestation spikes?",
    "What proportions of declining species are represented in current protected area networks?"
]

for q in species_research_questions:
    story.append(Paragraph(f"• {q}", bullet_style))


# ============================================================
# 18. KEY CONSERVATION FINDINGS
# ============================================================

story.append(Paragraph("7. Key Conservation Findings", section_style))

findings = [
    (
        "Monitored Biodiversity",
        f"The system actively tracks {total_species_monitored} endemic and focal species across {status_category_count} IUCN risk tiers."
    ),
    (
        "Threat Level Scale",
        f"{threatened_species_count} species are currently classified in high-risk IUCN Red List categories (CR, EN, VU)."
    ),
    (
        "Population Contraction",
        f"{declining_species_count} species exhibit documented declining population trajectories across assessment periods."
    ),
    (
        "Habitat Deforestation Pressure",
        f"Accumulated forest loss of {format_number(total_loss)} ha threatens critical corridors, with peak impact in {peak_year}."
    ),
    (
        "Critical Hotspot State",
        f"{highest_loss_state} accounts for the highest accumulated tree loss, presenting elevated risk to localized endemics."
    )
]

for title, description in findings:
    finding_table = Table(
        [[Paragraph(f"<b>{title}</b>", highlight_style), Paragraph(description, body_style)]],
        colWidths=[4.2 * cm, 11.8 * cm]
    )

    finding_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), LIGHT_GREEN),
            ("BACKGROUND", (1, 0), (1, 0), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6DED7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(finding_table)
    story.append(Spacer(1, 0.2 * cm))


# ============================================================
# 19. LIMITATIONS & FUTURE SCOPE
# ============================================================

story.append(Paragraph("8. Conservation Analytical Scope & Future Work", section_style))

story.append(Paragraph("Methodological Boundaries", subsection_style))
limitations = [
    "Species conservation status records reflect periodic IUCN evaluations rather than real-time annual censuses.",
    "Spatial overlay relies on state-aggregated forest loss; localized micro-habitat deforestation requires high-resolution spatial buffers.",
    "Conservation status shifts cannot be attributed solely to tree loss without incorporating poaching, invasive species, and climate variables."
]
for lim in limitations:
    story.append(Paragraph(f"• {lim}", bullet_style))

story.append(Paragraph("Future Research Scope", subsection_style))
future_items = [
    "Incorporate spatial species distribution models (SDMs) and range map overlays.",
    "Integrate bioacoustic and ecoacoustic monitoring metrics for automated species presence detection.",
    "Calculate species-specific habitat fragmentation indices based on high-resolution canopy cover data."
]
for fut in future_items:
    story.append(Paragraph(f"• {fut}", bullet_style))


# ============================================================
# 20. CONCLUSION
# ============================================================

story.append(Paragraph("9. Conclusion", section_style))

story.append(
    Paragraph(
        """
        The <b>Western Ghats Sentinel</b> report provides an integrated analysis centered on species biodiversity 
        and conservation urgency. By combining species Red List trajectories, status transitions, and population trends 
        with regional forest-loss patterns, the platform delivers actionable environmental intelligence designed to 
        support biodiversity conservation and ecological management in the Western Ghats.
        """,
        body_style
    )
)

story.append(Spacer(1, 0.5 * cm))

final_box = Table(
    [[
        Paragraph(
            "<b>WESTERN GHATS SENTINEL</b><br/>"
            "Species Biodiversity • Threat Trajectories • Habitat Conservation",
            highlight_style
        )
    ]],
    colWidths=[16 * cm]
)

final_box.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREEN),
        ("BOX", (0, 0), (-1, -1), 0.7, FOREST_GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10)
    ])
)

story.append(final_box)


# ============================================================
# 21. BUILD THE PDF
# ============================================================

try:
    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )
    print("\n" + "=" * 60)
    print("WESTERN GHATS SENTINEL")
    print("SPECIES-FOCUSED REPORT GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nPDF generated at:\n{OUTPUT_FILE}\n")
    print("=" * 60)

except Exception as error:
    print("\n" + "=" * 60)
    print("REPORT GENERATION FAILED")
    print("=" * 60)
    print(f"\nError:\n{error}\n")
    print("=" * 60)