# ============================================================
# PROJECT REPORT DOWNLOAD
# ============================================================
# ============================================================
# PROJECT REPORT DOWNLOAD
# ============================================================

import os
import streamlit as st


st.html(
    """
    <div style="
        margin-top: 3rem;
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            rgba(31, 77, 54, 0.08),
            rgba(178, 138, 69, 0.08)
        );
        border: 1px solid rgba(31, 77, 54, 0.15);
    ">

        <div style="
            font-size: 0.75rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #6F5740;
            font-weight: 700;
        ">
            PROJECT DOCUMENTATION
        </div>

        <h2 style="
            color: #1F4D36;
            margin-top: 0.35rem;
            margin-bottom: 0.5rem;
        ">
            Download the Research Report
        </h2>

        <p style="
            color: #526158;
            font-size: 1rem;
            margin-bottom: 0;
        ">
            Get the complete Western Ghats Sentinel project report,
            including methodology, findings, datasets, limitations,
            analytical framework and future scope.
        </p>

    </div>
    """
)


report_path = os.path.join(
    "reports",
    "Western_Ghats_Sentinel_Project_Report.pdf"
)


if os.path.exists(report_path):

    with open(report_path, "rb") as report_file:

        report_data = report_file.read()


    st.download_button(
        label="📄  Download Complete Project Report",
        data=report_data,
        file_name="Western_Ghats_Sentinel_Project_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


    st.caption(
        "PDF report • Western Ghats Sentinel • "
        "Tree Cover • Carbon • Conservation"
    )


else:

    st.warning(
        "The project report has not been generated yet. "
        "Run `python generate_report.py` from the project folder first."
    )