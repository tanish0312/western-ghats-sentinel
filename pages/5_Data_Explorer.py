import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Explorer | Western Ghats Sentinel",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# STYLING
# ============================================================

st.html("""
<style>

.main {
    background: #F7F5EF;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
}

.page-label {
    color: #A0802E;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}

.page-title {
    color: #153D2C;
    font-size: 40px;
    font-weight: 850;
    letter-spacing: -1px;
    margin-top: 5px;
}

.page-description {
    color: #69756E;
    font-size: 14px;
    line-height: 1.7;
    max-width: 1050px;
    margin-top: 8px;
    margin-bottom: 30px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 35px;
}

.metric-card {
    background: white;
    border: 1px solid #E4E3DC;
    border-radius: 16px;
    padding: 22px;
    min-height: 120px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
}

.metric-label {
    color: #78827C;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.metric-value {
    color: #12372A;
    font-size: 27px;
    font-weight: 850;
    margin-top: 8px;
}

.metric-description {
    color: #929A95;
    font-size: 11px;
    margin-top: 5px;
}

.section-label {
    color: #A0802E;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 30px;
}

.section-title {
    color: #153D2C;
    font-size: 28px;
    font-weight: 850;
    margin-top: 5px;
}

.section-description {
    color: #69756E;
    font-size: 13px;
    line-height: 1.7;
    max-width: 1000px;
    margin-bottom: 20px;
}

.info-box {
    background: #F1F6F1;
    border: 1px solid #DCE9DE;
    border-radius: 13px;
    padding: 18px 20px;
    margin: 25px 0;
}

.info-title {
    color: #245D3D;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.info-text {
    color: #68766D;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 6px;
}

.method-box {
    background: #F1F6F1;
    border: 1px solid #DCE9DE;
    border-radius: 13px;
    padding: 20px;
    margin-top: 35px;
}

.method-title {
    color: #245D3D;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.method-text {
    color: #68766D;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 7px;
}

.footer {
    text-align: center;
    color: #929A95;
    font-size: 11px;
    padding-top: 40px;
    margin-top: 45px;
    border-top: 1px solid #DDDDD5;
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="page-label">
    Research Data
</div>

<div class="page-title">
    Data Explorer
</div>

<div class="page-description">

Explore, filter, inspect and download the datasets that
power the Western Ghats Sentinel analytical dashboard.

</div>
""")


# ============================================================
# DATASET DEFINITIONS
# ============================================================

DATASETS = {

    "Forest Raw Data":
        "data/FOREST_RAW_DATA.csv",

    "Annual Tree-Cover Loss":
        "data/ANNUAL_TREE_COVER_LOSS.csv",

    "State-Year Tree Loss":
        "data/STATE_YEAR_TREE_LOSS.csv",

    "Final State Analysis":
        "data/FINAL_STATE_ANALYSIS.csv",

    "Species Status History":
        "data/SPECIES_STATUS_HISTORY.csv",

    "Species Status Trends":
        "data/SPECIES_STATUS_TRENDS.csv",

    "Species Status Transitions":
        "data/SPECIES_STATUS_TRANSITIONS.csv",

    "Lag Analysis":
        "data/LAG_ANALYSIS.csv",

}


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_dataset(path):

    return pd.read_csv(path)


# ============================================================
# FIND AVAILABLE DATASETS
# ============================================================

available_datasets = {}

for name, path in DATASETS.items():

    if os.path.exists(path):

        available_datasets[name] = path


if not available_datasets:

    st.error(
        "No CSV datasets were found in the data folder."
    )

    st.stop()


# ============================================================
# OVERALL DATASET STATISTICS
# ============================================================

total_datasets = len(
    available_datasets
)

total_rows = 0
total_columns = 0


for path in available_datasets.values():

    try:

        temp_df = load_dataset(path)

        total_rows += len(temp_df)

        total_columns += len(temp_df.columns)

    except Exception:
        pass


# ============================================================
# TOP KPI CARDS
# ============================================================

st.html(
    f"""
<div class="metric-grid">

    <div class="metric-card">

        <div class="metric-label">
            Datasets
        </div>

        <div class="metric-value">
            {total_datasets}
        </div>

        <div class="metric-description">
            Analytical files available
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Total Records
        </div>

        <div class="metric-value">
            {total_rows:,}
        </div>

        <div class="metric-description">
            Across all datasets
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Total Columns
        </div>

        <div class="metric-value">
            {total_columns:,}
        </div>

        <div class="metric-description">
            Variables available
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Format
        </div>

        <div class="metric-value">
            CSV
        </div>

        <div class="metric-description">
            Structured research data
        </div>

    </div>

</div>
"""
)


# ============================================================
# DATASET SELECTOR
# ============================================================

st.html("""
<div class="section-label">
    Dataset Library
</div>

<div class="section-title">
    Choose a Dataset
</div>

<div class="section-description">

Select a dataset to inspect its structure, filter records,
search values and download the data.

</div>
""")


selected_dataset = st.selectbox(
    "Dataset",
    list(
        available_datasets.keys()
    )
)


selected_path = available_datasets[
    selected_dataset
]


# ============================================================
# LOAD SELECTED DATASET
# ============================================================

try:

    df = load_dataset(
        selected_path
    )

except Exception as e:

    st.error(
        "Unable to read the selected dataset."
    )

    st.code(
        str(e)
    )

    st.stop()


# ============================================================
# SELECTED DATASET STATISTICS
# ============================================================

row_count = len(df)

column_count = len(df.columns)

missing_values = int(
    df.isna().sum().sum()
)

duplicate_rows = int(
    df.duplicated().sum()
)


# ============================================================
# DATASET KPI CARDS
# ============================================================

st.html(
    f"""
<div class="metric-grid">

    <div class="metric-card">

        <div class="metric-label">
            Rows
        </div>

        <div class="metric-value">
            {row_count:,}
        </div>

        <div class="metric-description">
            Records in selected dataset
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Columns
        </div>

        <div class="metric-value">
            {column_count}
        </div>

        <div class="metric-description">
            Variables
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Missing Values
        </div>

        <div class="metric-value">
            {missing_values:,}
        </div>

        <div class="metric-description">
            Empty cells
        </div>

    </div>


    <div class="metric-card">

        <div class="metric-label">
            Duplicate Rows
        </div>

        <div class="metric-value">
            {duplicate_rows:,}
        </div>

        <div class="metric-description">
            Exact duplicate records
        </div>

    </div>

</div>
"""
)


# ============================================================
# SEARCH & FILTER
# ============================================================

st.html("""
<div class="section-label">
    Search & Filter
</div>

<div class="section-title">
    Explore the Records
</div>

<div class="section-description">

Search across the entire dataset or apply filters to
individual categorical columns.

</div>
""")


search_text = st.text_input(
    "Search across all columns",
    placeholder=(
        "Try Kerala, 2015, Endangered, "
        "Maharashtra..."
    )
)


filtered_df = df.copy()


# ============================================================
# GLOBAL SEARCH
# ============================================================

if search_text.strip():

    search_value = (
        search_text
        .strip()
        .lower()
    )

    search_mask = (
        filtered_df
        .astype(str)
        .apply(
            lambda column:
            column
            .str
            .lower()
            .str
            .contains(
                search_value,
                na=False
            )
        )
        .any(axis=1)
    )

    filtered_df = filtered_df[
        search_mask
    ]


# ============================================================
# COLUMN FILTERS
# ============================================================

filterable_columns = []


for column in filtered_df.columns:

    unique_count = (
        filtered_df[column]
        .nunique(
            dropna=True
        )
    )

    if unique_count <= 30:

        filterable_columns.append(
            column
        )


if filterable_columns:

    st.write(
        "Optional column filters"
    )

    selected_filter_columns = st.multiselect(
        "Choose columns",
        filterable_columns
    )


    for column in selected_filter_columns:

        values = sorted(
            filtered_df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        selected_values = st.multiselect(
            f"Filter: {column}",
            values,
            default=values
        )


        if selected_values:

            filtered_df = filtered_df[
                filtered_df[column]
                .astype(str)
                .isin(
                    selected_values
                )
            ]


# ============================================================
# CURRENT SELECTION
# ============================================================

st.html(
    f"""
<div class="info-box">

    <div class="info-title">
        Current Selection
    </div>

    <div class="info-text">

        Showing
        <b>{len(filtered_df):,}</b>
        of
        <b>{len(df):,}</b>
        records from
        <b>{selected_dataset}</b>.

    </div>

</div>
"""
)


# ============================================================
# DATA TABLE
# ============================================================

st.html("""
<div class="section-label">
    Records
</div>

<div class="section-title">
    Data Table
</div>

<div class="section-description">

The table below contains the records matching your current
search and filters.

</div>
""")


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    height=520
)


# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.html("""
<div class="section-label">
    Export
</div>

<div class="section-title">
    Download Data
</div>

<div class="section-description">

Download either the filtered records or the complete
selected dataset.

</div>
""")


filtered_csv = (
    filtered_df
    .to_csv(index=False)
    .encode("utf-8")
)


full_csv = (
    df
    .to_csv(index=False)
    .encode("utf-8")
)


download_col1, download_col2 = st.columns(2)


with download_col1:

    st.download_button(

        label="⬇️ Download Filtered Data",

        data=filtered_csv,

        file_name=(
            selected_dataset
            .lower()
            .replace(" ", "_")
            + "_filtered.csv"
        ),

        mime="text/csv",

        use_container_width=True
    )


with download_col2:

    st.download_button(

        label="⬇️ Download Complete Dataset",

        data=full_csv,

        file_name=(
            selected_dataset
            .lower()
            .replace(" ", "_")
            + ".csv"
        ),

        mime="text/csv",

        use_container_width=True
    )


# ============================================================
# COLUMN INFORMATION
# ============================================================

st.html("""
<div class="section-label">
    Dataset Structure
</div>

<div class="section-title">
    Column Information
</div>

<div class="section-description">

Inspect the type, completeness and uniqueness of every
variable in the selected dataset.

</div>
""")


column_info = pd.DataFrame(
    {
        "Column": df.columns,

        "Data Type": [
            str(
                df[column].dtype
            )
            for column in df.columns
        ],

        "Non-Null Values": [
            int(
                df[column]
                .notna()
                .sum()
            )
            for column in df.columns
        ],

        "Missing Values": [
            int(
                df[column]
                .isna()
                .sum()
            )
            for column in df.columns
        ],

        "Unique Values": [
            int(
                df[column]
                .nunique(
                    dropna=True
                )
            )
            for column in df.columns
        ]
    }
)


st.dataframe(
    column_info,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# NUMERICAL SUMMARY
# ============================================================

# IMPORTANT:
# We intentionally use include="number"
# instead of np.number.
# This means NumPy is NOT required here.

numeric_columns = (
    df
    .select_dtypes(
        include="number"
    )
    .columns
    .tolist()
)


if numeric_columns:

    st.html("""
    <div class="section-label">
        Statistical Summary
    </div>

    <div class="section-title">
        Numerical Variables
    </div>

    <div class="section-description">

    Descriptive statistics for the numerical variables
    contained in the selected dataset.

    </div>
    """)


    summary = (
        df[numeric_columns]
        .describe()
        .T
        .reset_index()
        .rename(
            columns={
                "index": "Variable"
            }
        )
    )


    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DATA QUALITY NOTE
# ============================================================

st.html("""
<div class="method-box">

    <div class="method-title">
        Data Quality & Transparency
    </div>

    <div class="method-text">

        The Data Explorer provides direct visibility into the
        datasets used by Western Ghats Sentinel. Users can
        inspect row counts, variables, missing values,
        duplicate records and numerical summaries before
        using the data for analysis.

    </div>

</div>
""")


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    <b>Western Ghats Sentinel</b>

    &nbsp;•&nbsp;

    Tree Cover • Carbon • Conservation

    <br>

    Research Data Explorer

</div>
""")