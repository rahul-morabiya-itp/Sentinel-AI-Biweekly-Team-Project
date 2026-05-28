import sqlite3
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import plotly.express as px

from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SentinelAI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# REALTIME AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=15000,
    key="sentinel_dashboard_refresh"
)

# =========================================================
# CONSTANTS
# =========================================================

DATABASE_PATH = "data/logs.db"

API_BASE_URL = "http://127.0.0.1:8000"

# =========================================================
# PAGE TITLE
# =========================================================

st.title("🛡️ SentinelAI Gateway Dashboard")

st.markdown("""
### Enterprise AI Traffic Intelligence, Governance & AI FinOps Platform
""")

# =========================================================
# DATABASE HELPERS
# =========================================================

@st.cache_data(ttl=3)
def load_request_logs():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    dataframe = pd.read_sql(
        "SELECT * FROM request_logs",
        connection
    )

    connection.close()

    return dataframe


# =========================================================
# REALTIME METRICS API
# =========================================================

@st.cache_data(ttl=2)
def load_realtime_metrics():

    try:

        response = requests.get(
            f"{API_BASE_URL}/realtime-metrics",
            timeout=3
        )

        if response.status_code == 200:

            return response.json()

        return {}

    except Exception:

        return {}


# =========================================================
# SAFE DATAFRAME UTILITIES
# =========================================================

def safe_sum(dataframe, column_name):

    if column_name not in dataframe.columns:
        return 0

    return dataframe[column_name].fillna(0).sum()


def safe_mean(dataframe, column_name):

    if column_name not in dataframe.columns:
        return 0

    return round(
        dataframe[column_name].fillna(0).mean(),
        2
    )


# =========================================================
# MAIN APPLICATION
# =========================================================

try:

    dataframe = load_request_logs()

    realtime_metrics = load_realtime_metrics()

    # =====================================================
    # EMPTY STATE
    # =====================================================

    if dataframe.empty:

        st.warning(
            "No AI traffic logs available yet."
        )

        st.info(
            "Send requests through the gateway to begin monitoring."
        )

        st.stop()

    # =====================================================
    # SORT DATA
    # =====================================================

    if "id" in dataframe.columns:

        dataframe = dataframe.sort_values(
            by="id",
            ascending=False
        )

    # =====================================================
    # KPI METRICS
    # =====================================================

    total_requests = len(dataframe)

    total_tokens = safe_sum(
        dataframe,
        "total_tokens"
    )

    total_cost = safe_sum(
        dataframe,
        "estimated_cost"
    )

    average_latency = safe_mean(
        dataframe,
        "latency"
    )

    high_risk_requests = len(
        dataframe[
            dataframe["risk_level"] == "HIGH"
        ]
    )

    duplicate_requests = len(
        dataframe[
            dataframe["similarity_score"].notnull()
        ]
    )

    # =====================================================
    # REALTIME STATUS
    # =====================================================

    last_updated = realtime_metrics.get(
        "last_updated",
        str(datetime.utcnow())
    )

    st.caption(
        f"Last Updated: {last_updated}"
    )

    # =====================================================
    # KPI ROW 1
    # =====================================================

    st.subheader("Platform Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Requests",
        f"{total_requests:,}"
    )

    col2.metric(
        "Total Tokens",
        f"{int(total_tokens):,}"
    )

    col3.metric(
        "Total AI Spend",
        f"${total_cost:.6f}"
    )

    col4.metric(
        "Average Latency",
        f"{average_latency}s"
    )

    # =====================================================
    # KPI ROW 2
    # =====================================================

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "High Risk Requests",
        high_risk_requests
    )

    col6.metric(
        "Duplicate Requests",
        duplicate_requests
    )

    col7.metric(
        "Live Requests",
        realtime_metrics.get(
            "total_requests",
            total_requests
        )
    )

    col8.metric(
        "Live AI Spend",
        f"${realtime_metrics.get('total_cost', total_cost):.6f}"
    )

    st.divider()

    # =====================================================
    # REQUEST LOGS
    # =====================================================

    st.subheader("Realtime AI Traffic Logs")

    st.dataframe(
        dataframe,
        use_container_width=True,
        height=400
    )

    st.divider()

    # =====================================================
    # CHART SECTION
    # =====================================================

    col9, col10 = st.columns(2)

    # =====================================================
    # RISK DISTRIBUTION
    # =====================================================

    with col9:

        st.subheader("Risk Distribution")

        if "risk_level" in dataframe.columns:

            fig_risk = px.pie(
                dataframe,
                names="risk_level",
                title="AI Risk Levels"
            )

            st.plotly_chart(
                fig_risk,
                use_container_width=True
            )

    # =====================================================
    # INTENT DISTRIBUTION
    # =====================================================

    with col10:

        st.subheader("Intent Distribution")

        if "intent" in dataframe.columns:

            fig_intent = px.histogram(
                dataframe,
                x="intent",
                title="Intent Classification"
            )

            st.plotly_chart(
                fig_intent,
                use_container_width=True
            )

    st.divider()

    # =====================================================
    # TOKEN & COST ANALYTICS
    # =====================================================

    col11, col12 = st.columns(2)

    with col11:

        st.subheader("Token Consumption")

        fig_tokens = px.line(
            dataframe,
            y="total_tokens",
            title="Realtime Token Usage"
        )

        st.plotly_chart(
            fig_tokens,
            use_container_width=True
        )

    with col12:

        st.subheader("AI Cost Trends")

        fig_cost = px.line(
            dataframe,
            y="estimated_cost",
            title="Realtime AI Spend"
        )

        st.plotly_chart(
            fig_cost,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # ORGANIZATIONAL ANALYTICS
    # =====================================================

    st.subheader("Organizational AI Usage Intelligence")

    if "source" in dataframe.columns:

        source_metrics = dataframe.groupby(
            "source"
        ).agg({
            "total_tokens": "sum",
            "estimated_cost": "sum",
            "latency": "mean"
        }).reset_index()

        source_metrics["latency"] = (
            source_metrics["latency"]
            .round(2)
        )

        st.dataframe(
            source_metrics,
            use_container_width=True
        )

        fig_source_cost = px.bar(
            source_metrics,
            x="source",
            y="estimated_cost",
            title="Cost Per Organizational Source"
        )

        st.plotly_chart(
            fig_source_cost,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # AI GOVERNANCE
    # =====================================================

    st.subheader("AI Governance & Security Insights")

    pii_requests = dataframe[
        dataframe["pii_detected"].fillna("") != ""
    ]

    governance_col1, governance_col2 = st.columns(2)

    governance_col1.metric(
        "PII Related Requests",
        len(pii_requests)
    )

    governance_col2.metric(
        "High Risk Requests",
        high_risk_requests
    )

    if len(pii_requests) > 0:

        st.warning(
            "Sensitive or regulated information detected."
        )

        st.dataframe(
            pii_requests[[
                "source",
                "pii_detected",
                "risk_level",
                "prompt"
            ]],
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # SEMANTIC DUPLICATES
    # =====================================================

    st.subheader("Semantic Duplicate Detection")

    duplicate_dataframe = dataframe[
        dataframe["similarity_score"].notnull()
    ]

    if len(duplicate_dataframe) > 0:

        st.info(
            "Potential reusable AI workloads detected."
        )

        st.dataframe(
            duplicate_dataframe[[
                "source",
                "prompt",
                "similarity_score"
            ]],
            use_container_width=True
        )

    else:

        st.success(
            "No duplicate workloads detected."
        )

    st.divider()

    # =====================================================
    # OPTIMIZATION INTELLIGENCE
    # =====================================================

    st.subheader("Optimization Intelligence")

    high_token_requests = dataframe[
        dataframe["total_tokens"] > 300
    ]

    if len(high_token_requests) > 0:

        st.warning(
            "High token consumption requests identified."
        )

        st.dataframe(
            high_token_requests[[
                "source",
                "total_tokens",
                "optimization"
            ]],
            use_container_width=True
        )

    else:

        st.success(
            "No major optimization issues detected."
        )

    st.divider()

    # =====================================================
    # AI FINOPS
    # =====================================================

    st.subheader("AI FinOps Insights")

    waste_score = min(
        int(
            (
                duplicate_requests /
                max(total_requests, 1)
            ) * 100
        ),
        100
    )

    potential_savings = round(
        total_cost * (
            waste_score / 100
        ),
        6
    )

    finops_col1, finops_col2 = st.columns(2)

    finops_col1.metric(
        "AI Waste Score",
        f"{waste_score}%"
    )

    finops_col2.metric(
        "Potential Savings",
        f"${potential_savings:.6f}"
    )

    st.markdown("""
### Recommended Optimization Actions

- Enable semantic caching
- Reduce repetitive prompts
- Use smaller models for lightweight workloads
- Compress excessive prompt context
- Standardize enterprise prompt templates
- Route sensitive workloads to secure internal models
""")

except Exception as error:

    st.error(
        f"Dashboard Error: {str(error)}"
    )