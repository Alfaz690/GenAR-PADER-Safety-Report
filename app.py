import json
from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from src.analysis import compute_analysis
from src.generator import generate_sections, markdown_report
from src.loader import normalize_text_columns
from src.validation import validate_and_prepare
from src.validator import validate_report

st.set_page_config(
    page_title="GenAR | PADER Safety Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp { background: #f4f7fb; }
    [data-testid="stHeader"] { background: rgba(244,247,251,0.9); }
    [data-testid="stSidebar"] { background: #0b1736; }
    [data-testid="stSidebar"] * { color: #eef4ff !important; }

    .hero {
        background: linear-gradient(135deg, #102a72 0%, #1769aa 55%, #19a7a0 100%);
        padding: 28px 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(16,42,114,.16);
    }
    .hero h1 { margin: 0; font-size: 34px; }
    .hero p { margin: 8px 0 0; opacity: .9; font-size: 16px; }

    .section-title { font-size: 22px; font-weight: 750; color: #12203b; margin: 10px 0 12px; }
    .small-muted { color: #667085; font-size: 13px; }

    .kpi {
        background: white;
        border: 1px solid #e4eaf2;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 112px;
        box-shadow: 0 5px 18px rgba(16,42,114,.06);
    }
    .kpi .label { color: #667085; font-size: 13px; font-weight: 650; }
    .kpi .value { color: #102a72; font-size: 29px; font-weight: 800; margin-top: 5px; }
    .kpi .sub { color: #667085; font-size: 12px; margin-top: 3px; }

    .status-ok {
        background: #ecfdf3; border: 1px solid #abefc6; color: #067647;
        padding: 14px 16px; border-radius: 12px; font-weight: 700;
    }
    .status-warn {
        background: #fffaeb; border: 1px solid #fedf89; color: #b54708;
        padding: 14px 16px; border-radius: 12px; font-weight: 700;
    }
    .info-card {
        background: white; border: 1px solid #e4eaf2; border-radius: 16px;
        padding: 18px; box-shadow: 0 5px 18px rgba(16,42,114,.05);
    }
    div[data-testid="stFileUploader"] {
        background: white; border: 1px dashed #7aa2d8; border-radius: 14px; padding: 8px;
    }
    .footer { text-align:center; color:#98a2b3; font-size:12px; padding:28px 0 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def kpi(label, value, sub=""):
    return f"""
    <div class='kpi'>
      <div class='label'>{label}</div>
      <div class='value'>{value}</div>
      <div class='sub'>{sub}</div>
    </div>
    """


def dict_frame(d, name="Value"):
    if not d:
        return pd.DataFrame(columns=["Category", name])

    # Handle both dictionary and list formats from analysis output
    if isinstance(d, list):
        df = pd.DataFrame(d)
        if "Category" not in df.columns:
            df["Category"] = range(len(df))
        return df

    return pd.DataFrame({
        "Category": list(d.keys()),
        name: list(d.values())
    })


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class='hero'>
      <h1>🛡️ GenAR</h1>
      <p>AI-assisted regulatory safety reporting • PADER-style analysis • evidence-grounded reporting</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## GenAR Control Center")
    st.caption("Safety reporting prototype")
    st.markdown("### Workflow")
    st.markdown("1. 📁 Upload safety data")
    st.markdown("2. 🔎 Validate & analyze")
    st.markdown("3. 🧠 Generate report")
    st.markdown("4. ✅ Validate output")
    st.markdown("5. 👤 Human review")
    st.divider()
    st.markdown("**AI mode**")
    st.info("Offline evidence-grounded fallback is available when API credits are unavailable.")

st.markdown("<div class='section-title'>📁 Upload Safety Dataset</div>", unsafe_allow_html=True)
uploaded = st.file_uploader(
    "Upload the supplied Bisoprolol safety CSV",
    type=["csv"],
    help="The app performs deterministic analysis first and only then generates the report from approved evidence.",
)

if not uploaded:
    st.markdown(
        """
        <div class='info-card'>
        <b>Ready to analyze</b><br>
        <span class='small-muted'>Upload a CSV to view case volume, seriousness, demographics, reactions, outcomes and trends.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='footer'>GenAR • Controlled, traceable safety reporting prototype</div>", unsafe_allow_html=True)
    st.stop()

with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    tmp.write(uploaded.getbuffer())
    csv_path = tmp.name

try:
    df = pd.read_csv(csv_path, low_memory=False)
    df = normalize_text_columns(df)
    df = validate_and_prepare(df)
except Exception as exc:
    st.error(str(exc))
    st.stop()

analysis = compute_analysis(df)
case = analysis["case_summary"]
alerts = analysis.get("alerts", {})
period = analysis.get("reporting_period", {})

# -----------------------------
# KPI row
# -----------------------------
st.markdown("<div class='section-title'>📊 Safety Overview</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(kpi("Total cases", f"{case['total_cases']:,}", "Unique safety report IDs"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi("Serious cases", f"{case['serious_cases']:,}", f"{case['serious_percentage']:.1f}% of cases"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi("Non-serious", f"{case['non_serious_cases']:,}", f"{case['non_serious_percentage']:.1f}% of cases"), unsafe_allow_html=True)
with c4:
    st.markdown(kpi("15-day / alerts", f"{alerts.get('alert_cases', 0):,}", "Expedited criteria cases"), unsafe_allow_html=True)

st.caption(f"Reporting period: {period.get('start', 'N/A')} → {period.get('end', 'N/A')}  •  Product: {analysis.get('dataset', {}).get('product', 'Bisoprolol')}")

# -----------------------------
# Analytics tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Demographics", "⚠️ Reactions", "🌍 Geography", "🕒 Trends & Outcomes"])

with tab1:
    a, b = st.columns(2)
    with a:
        st.markdown("**Age-group distribution**")
        age_df = dict_frame(analysis.get("age_groups", {}), "Cases").set_index("Category")
        st.bar_chart(age_df, use_container_width=True)
    with b:
        st.markdown("**Sex distribution**")
        sex_df = dict_frame(analysis.get("sex_distribution", {}), "Cases").set_index("Category")
        st.bar_chart(sex_df, use_container_width=True)

with tab2:
    a, b = st.columns(2)
    with a:
        st.markdown("**Most common reactions**")
        reaction_df = pd.DataFrame(analysis.get("top_reactions", []))
        if not reaction_df.empty:
            reaction_df = reaction_df.rename(columns={"value": "Reaction", "count": "Cases"}).set_index("Reaction").head(10)
            st.bar_chart(reaction_df, use_container_width=True)
        else:
            st.info("No reaction data available.")
    with b:
        st.markdown("**Most common serious reactions**")
        serious_df = pd.DataFrame(analysis.get("top_serious_reactions", []))
        if not serious_df.empty:
            serious_df = serious_df.rename(columns={"value": "Reaction", "count": "Cases"}).set_index("Reaction").head(10)
            st.bar_chart(serious_df, use_container_width=True)
        else:
            st.info("No serious reaction data available.")

with tab3:
    country_df = dict_frame(analysis.get("country_distribution_top15", {}), "Cases").set_index("Category")
    st.bar_chart(country_df, use_container_width=True)

with tab4:
    a, b = st.columns(2)
    with a:
        st.markdown("**Monthly case trend**")
        trend = analysis.get("trends", {}).get("monthly_cases", {})
        trend_df = dict_frame(trend, "Cases").set_index("Category")
        st.line_chart(trend_df, use_container_width=True)
    with b:
        st.markdown("**Outcomes**")
        outcome_df = pd.DataFrame(analysis.get("outcomes", []))
        if not outcome_df.empty:
            outcome_df = outcome_df.rename(columns={"value": "Outcome", "count": "Cases"}).head(10).set_index("Outcome")
            st.bar_chart(outcome_df, use_container_width=True)
        else:
            st.info("No outcome data available.")

with st.expander("🔍 View deterministic analysis data"):
    st.json(analysis)

# -----------------------------
# Report generation
# -----------------------------
st.markdown("<div class='section-title'>📄 PADER Report Generation</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='info-card'><b>Grounding rule:</b> deterministic Python computes the numbers first; the report generator receives the approved analysis rather than the raw CSV.</div>",
    unsafe_allow_html=True,
)

if st.button("🚀 Generate PADER Draft", type="primary", use_container_width=True):
    with st.spinner("Generating evidence-grounded report sections..."):
        try:
            try:
                sections = generate_sections(analysis, use_ai=True)
                generation_mode = "AI generation"
            except Exception:
                sections = generate_sections(analysis, use_ai=False)
                generation_mode = "Offline evidence-grounded fallback"

            validation = validate_report(sections, analysis)
            report = markdown_report(analysis, sections)
            st.session_state["sections"] = sections
            st.session_state["validation"] = validation
            st.session_state["report"] = report
            st.session_state["generation_mode"] = generation_mode
            st.session_state["review_status"] = "Pending review"
        except Exception as exc:
            st.error(str(exc))

if "validation" in st.session_state:
    st.divider()
    validation = st.session_state["validation"]
    generation_mode = st.session_state.get("generation_mode", "Unknown")

    status_col, mode_col = st.columns(2)
    with status_col:
        if validation.get("overall_valid"):
            st.markdown("<div class='status-ok'>✅ Validation passed — no unsupported numbers detected by the validator.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-warn'>⚠️ Validation flagged the draft — review before finalization.</div>", unsafe_allow_html=True)
    with mode_col:
        st.markdown(f"<div class='info-card'><b>Generation mode</b><br>{generation_mode}</div>", unsafe_allow_html=True)

    rtab1, rtab2, rtab3 = st.tabs(["📄 Report", "🔎 Validation & Evidence", "👤 Human Review"])

    with rtab1:
        st.download_button(
            "⬇️ Download PADER Markdown",
            data=st.session_state["report"],
            file_name="pader_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
        for name, text in st.session_state["sections"].items():
            with st.expander(name.replace("_", " ").title(), expanded=True):
                st.markdown(text)

    with rtab2:
        st.markdown("**Validation result**")
        st.json(validation)
        evidence = analysis.get("evidence", None)
        if evidence is not None:
            st.markdown("**Evidence**")
            st.json(evidence)
        else:
            st.info("Evidence is stored in the generated evidence.json artifact.")

    with rtab3:
        current = st.session_state.get("review_status", "Pending review")
        st.markdown(f"**Review status:** `{current}`")
        left, right = st.columns(2)
        with left:
            if st.button("✅ Approve Report", use_container_width=True):
                st.session_state["review_status"] = "Approved by reviewer"
                st.rerun()
        with right:
            if st.button("🚩 Flag for Review", use_container_width=True):
                st.session_state["review_status"] = "Flagged for review"
                st.rerun()
        st.caption("Human review is the final control before treating the generated report as final.")

st.markdown("<div class='footer'>GenAR • Evidence-grounded regulatory safety reporting • Prototype dashboard</div>", unsafe_allow_html=True)