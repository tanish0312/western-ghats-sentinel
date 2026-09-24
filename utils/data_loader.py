import pandas as pd
import geopandas as gpd


# ---------------------------------------------------------
# FOREST DATA
# ---------------------------------------------------------

def load_forest_data():
    return pd.read_csv(
        "data/FOREST_RAW_DATA.csv"
    )


# ---------------------------------------------------------
# ANNUAL TREE-COVER LOSS
# ---------------------------------------------------------

def load_annual_loss():
    return pd.read_csv(
        "data/ANNUAL_TREE_COVER_LOSS.csv"
    )


# ---------------------------------------------------------
# STATE-YEAR TREE-COVER LOSS
# ---------------------------------------------------------

def load_state_year_loss():
    return pd.read_csv(
        "data/STATE_YEAR_TREE_LOSS.csv"
    )


# ---------------------------------------------------------
# DISTRICT-YEAR TREE-COVER LOSS
# ---------------------------------------------------------

def load_district_year_loss():
    return pd.read_csv(
        "data/DISTRICT_YEAR_TREE_LOSS.csv"
    )


# ---------------------------------------------------------
# DISTRICT MAP
# ---------------------------------------------------------

def load_district_map():
    return gpd.read_file(
        "data/western_ghats_districts.geojson"
    )


# ---------------------------------------------------------
# FINAL STATE ANALYSIS
# ---------------------------------------------------------

def load_state_analysis():
    return pd.read_csv(
        "data/FINAL_STATE_ANALYSIS.csv"
    )


# ---------------------------------------------------------
# SPECIES HISTORY
# ---------------------------------------------------------

def load_species_history():
    return pd.read_csv(
        "data/SPECIES_STATUS_HISTORY.csv"
    )


# ---------------------------------------------------------
# SPECIES TRENDS
# ---------------------------------------------------------

def load_species_trends():
    return pd.read_csv(
        "data/SPECIES_STATUS_TRENDS.csv"
    )


# ---------------------------------------------------------
# SPECIES TRANSITIONS
# ---------------------------------------------------------

def load_species_transitions():
    return pd.read_csv(
        "data/SPECIES_STATUS_TRANSITIONS.csv"
    )


# ---------------------------------------------------------
# LAG ANALYSIS
# ---------------------------------------------------------

def load_lag_analysis():
    return pd.read_csv(
        "data/LAG_ANALYSIS.csv"
    )


# ---------------------------------------------------------
# MAP
# ---------------------------------------------------------

def load_map():
    return gpd.read_file(
        "data/map_complete.geojson"
    )