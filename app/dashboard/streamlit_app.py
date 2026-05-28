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
# AUTO REFRESH
# =========================================================

REFRESH_INTERVAL_MS = 10000

st_autorefresh(
    interval=REFRESH_INTERVAL_MS,
    key="sentinel_dashboard_refresh"
)

# =========================================================
# CONSTANTS
# =========================================================

DATABASE_PATH = "data/logs.db"

API_BASE_URL = "http://127.0.0.1:8000"

# =========================================================
# PAGE HEADER
# =========================================================

st.title("🛡️ SentinelAI Gateway Dashboard")

st.markdown("""
### Enterprise AI Traffic Intelligence, Governance & AI FinOps Platform
""")

# =========================================================
# DATABASE HELPERS
# =========================================================

@st.cache_data(ttl=5)
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
# REALTIME METRICS
# =========================================================

@st.cache_data(ttl=3)
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
# SAFE HELPERS
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
    # KPI CALCULATIONS
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

    pii_requests = len(
        dataframe[
            dataframe["pii_detected"].fillna("") != ""
        ]
    )

    # =====================================================
    # LAST UPDATED
    # =====================================================

    last_updated = realtime_metrics.get(
        "last_updated",
        str(datetime.utcnow())
    )

    st.caption(
        f"Last Updated: {last_updated}"
    )

    # =====================================================
    # KPI SECTION
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
        "PII Requests",
        pii_requests
    )

    col8.metric(
        "Live AI Spend",
        f"${realtime_metrics.get('total_cost', total_cost):.6f}"
    )

    st.divider()

    # =====================================================
    # REALTIME TRAFFIC LOGS
    # =====================================================

    st.subheader("Realtime AI Traffic Logs")

    st.dataframe(
        dataframe,
        use_container_width=True,
        height=450
    )

    st.divider()

    # =====================================================
    # RISK & INTENT ANALYTICS
    # =====================================================

    col9, col10 = st.columns(2)

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

        st.subheader("Realtime Token Consumption")

        fig_tokens = px.line(
            dataframe,
            y="total_tokens",
            title="Token Usage Trends"
        )

        st.plotly_chart(
            fig_tokens,
            use_container_width=True
        )

    with col12:

        st.subheader("Realtime AI Spend")

        fig_cost = px.line(
            dataframe,
            y="estimated_cost",
            title="AI Cost Trends"
        )

        st.plotly_chart(
            fig_cost,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # MODEL USAGE INTELLIGENCE
    # =====================================================

    st.subheader("Model Usage Intelligence")

    if (
        "model_name" in dataframe.columns
        and
        "provider" in dataframe.columns
    ):

        model_metrics = dataframe.groupby(
            ["provider", "model_name"]
        ).agg({
            "total_tokens": "sum",
            "estimated_cost": "sum",
            "latency": "mean"
        }).reset_index()

        model_metrics["latency"] = (
            model_metrics["latency"]
            .round(2)
        )

        st.dataframe(
            model_metrics,
            use_container_width=True
        )

        fig_models = px.bar(
            model_metrics,
            x="model_name",
            y="estimated_cost",
            color="provider",
            title="Cost Per Model"
        )

        st.plotly_chart(
            fig_models,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # ORGANIZATIONAL ANALYTICS
    # =====================================================

    st.subheader(
        "Organizational AI Usage Intelligence"
    )

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
    # GOVERNANCE & SECURITY
    # =====================================================

    st.subheader(
        "AI Governance & Security Insights"
    )

    pii_dataframe = dataframe[
        dataframe["pii_detected"].fillna("") != ""
    ]

    if len(pii_dataframe) > 0:

        st.warning(
            "Sensitive information detected in prompts."
        )

        st.dataframe(
            pii_dataframe[[
                "source",
                "pii_detected",
                "risk_level",
                "prompt"
            ]],
            use_container_width=True
        )

    else:

        st.success(
            "No sensitive information detected."
        )

    st.divider()

    # =====================================================
    # SEMANTIC DUPLICATE DETECTION
    # =====================================================

    st.subheader(
        "Semantic Duplicate Detection"
    )

    duplicate_dataframe = dataframe[
        dataframe["similarity_score"].notnull()
    ]

    if len(duplicate_dataframe) > 0:

        st.info(
            "Potential reusable workloads detected."
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
            "No semantic duplicates detected."
        )

    st.divider()

    # =====================================================
    # OPTIMIZATION INTELLIGENCE
    # =====================================================

    st.subheader(
        "Optimization Intelligence"
    )

    high_token_requests = dataframe[
        dataframe["total_tokens"] > 300
    ]

    if len(high_token_requests) > 0:

        st.warning(
            "High token usage workloads identified."
        )

        st.dataframe(
            high_token_requests[[
                "source",
                "model_name",
                "total_tokens",
                "estimated_cost",
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
    # AI FINOPS INSIGHTS
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
### Optimization Recommendations

- Enable semantic caching
- Reuse duplicate AI workloads
- Route lightweight tasks to cheaper models
- Compress verbose prompts
- Standardize enterprise prompts
- Route sensitive requests to secure models
- Optimize high-cost organizational workloads
""")

    st.divider()

    # =====================================================
    # MODEL COST LEADERBOARD
    # =====================================================

    st.subheader("Model Cost Leaderboard")

    if "model_name" in dataframe.columns:

        leaderboard = dataframe.groupby(
            "model_name"
        ).agg({
            "estimated_cost": "sum",
            "total_tokens": "sum"
        }).reset_index()

        leaderboard = leaderboard.sort_values(
            by="estimated_cost",
            ascending=False
        )

        st.dataframe(
            leaderboard,
            use_container_width=True
        )

except Exception as error:

    st.error(
        f"Dashboard Error: {str(error)}"
    )