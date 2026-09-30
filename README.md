# 🌿 Western Ghats Sentinel

> **An Interactive Environmental Analytics & Species Conservation Platform for the Western Ghats Biodiversity Hotspot**


## 📌 Executive Overview

**Western Ghats Sentinel** is an open-source environmental analytics project designed to assess **species conservation risks, IUCN Red List status trajectories, population trends, and forest loss drivers** across five key states in India's Western Ghats region: **Karnataka, Kerala, Tamil Nadu, Goa, and Maharashtra**.

By transforming multi-source environmental datasets into an interactive web interface and automated reporting workflow, the platform enables researchers, conservationists, and decision-makers to evaluate biodiversity threats in tandem with regional deforestation and carbon dynamics.

---

## 📌 Key Features

- 🐅 **Species Threat Dynamics**: Interactive tracking of monitored endemic species across IUCN Red List risk tiers (*Critically Endangered, Endangered, Vulnerable, Near Threatened, Least Concern*).
- 🔄 **Conservation Transitions**: Historic evaluation of species threat escalations and risk status changes over time.
- 📉 **Population Trend Monitoring**: Analytics pinpointing proportions of declining, stable, and recovering species populations.
- 🗺️ **Spatial Deforestation & Intensity**: State-level tree-cover loss quantification, area-normalized spatial intensity mapping, and carbon emission indicators.
- 📄 **Automated PDF Report Generator**: Built-in PDF generation engine (`generate_report.py`) producing professional, species-centric conservation intelligence reports.

---

## 📂 Repository Structure

```text
western-ghats-sentinel/
├── data/                                 # Project Datasets
│   ├── ANNUAL_TREE_COVER_LOSS.csv        # Temporal forest loss series
│   ├── DISTRICT_YEAR_TREE_LOSS.csv      # District-level deforestation breakdowns
│   ├── FINAL_STATE_ANALYSIS.csv          # State-level loss, emissions & spatial intensity
│   ├── FOREST_RAW_DATA.csv               # Primary observational datasets
│   ├── LAG_ANALYSIS.csv                  # Lagged statistical correlations
│   ├── SPECIES_STATUS_HISTORY.csv        # Historical species IUCN assessments
│   ├── SPECIES_STATUS_TRANSITIONS.csv    # Recorded category shifts per species
│   ├── SPECIES_STATUS_TRENDS.csv         # Population directionality metrics
│   └── STATE_YEAR_TREE_LOSS.csv          # State x Year loss matrix
├── images/                               # Species and geographic assets
├── reports/                              # Generated PDF reports output folder
├── app.py                                # Streamlit Interactive Dashboard main script
├── generate_report.py                    # PDF Report Generation script
├── requirements.txt                      # Project dependency list
└── README.md                             # Project Documentation
```

---

## 📊 Analytical Data Architecture

| Dataset | Primary Analytical Focus | Key Indicators |
| :--- | :--- | :--- |
| `SPECIES_STATUS_HISTORY.csv` | Taxa Risk Baselines | Species Name, Assessment Year, IUCN Category |
| `SPECIES_STATUS_TRANSITIONS.csv` | Threat Escalation Tracking | Previous Status, Updated Status, Shift Direction |
| `SPECIES_STATUS_TRENDS.csv` | Population Trajectories | Population Trend (*Declining, Stable, Increasing*) |
| `ANNUAL_TREE_COVER_LOSS.csv` | Temporal Habitat Loss | Annual Loss (ha), Peak Deforestation Years |
| `FINAL_STATE_ANALYSIS.csv` | Spatial & Carbon Pressure | Loss Intensity (ha/1,000 km²), Emissions ($Mg\,CO_2e$) |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your system.

### 2. Clone Repository
```bash
git clone https://github.com/tanish0312/western-ghats-sentinel.git
cd western-ghats-sentinel
```

### 3. Create & Activate Virtual Environment
```bash
# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Running the Interactive Streamlit Dashboard
Launch the web interface to explore interactive charts, spatial maps, and species profiles:
```bash
streamlit run app.py
```

### Generating the Species Conservation PDF Report
To build the species-focused PDF report, execute the generation script:
```bash
python generate_report.py
```
The compiled PDF report will be saved automatically to:
`reports/Western_Ghats_Sentinel_Species_Conservation_Report.pdf`

---

## 🛠️ Technology Stack

- **Frontend & Dashboard**: Streamlit
- **Data Engineering & Analysis**: Pandas, NumPy
- **Spatial Processing**: GeoPandas, Shapely
- **Data Visualizations**: Plotly Express, Plotly Graph Objects
- **Document Generation**: ReportLab
- **Geographic Data**: GeoJSON

---

## 🔬 Research Boundaries & Disclaimer

- **Observational Nature**: Statistical relationships and correlation analyses do not imply direct causation between tree loss and species status transitions.
- **Spatial Granularity**: Forest loss indicators are aggregated at state levels; detailed micro-habitat analysis requires high-resolution remote sensing layers.
- **Assessment Schedules**: Species Red List assessments reflect periodic IUCN evaluations rather than continuous real-time censuses.

---

## 🤝 Contributing

Contributions are welcome! If you would like to add new dataset layers, improve spatial analysis models, or refine species visualization components:
1. Fork the Repository
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.
