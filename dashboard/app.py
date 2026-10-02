"""
DemandIQ: Executive Dynamic Pricing & Demand Forecasting Dashboard
Motorola Edge 50 Pro (Flipkart India Operational Control Panel)
"""

import os
import sys
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATASET_PATH = os.path.join(PROJECT_ROOT, "data", "retail_data.csv")
API_URL = "http://127.0.0.1:8000/api/v1/pricing/recommend"

st.set_page_config(
    page_title="DemandIQ | Motorola AI Pricing Engine",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom Styling -----------------
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Top Header & System Telemetry -----------------
col_title, col_status = st.columns([3.5, 1.5])
with col_title:
    st.markdown("<div class='main-title'>📱 DemandIQ: Retail Operations Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Motorola Edge 50 Pro (256 GB) — Real-Time Flipkart Market Intelligence</div>", unsafe_allow_html=True)

with col_status:
    try:
        r = requests.get("http://127.0.0.1:8000/", timeout=1)
        if r.status_code == 200:
            st.success("🟢 AI Backend Online (Port 8000)", icon="⚡")
        else:
            st.warning("🟠 Backend Anomaly")
    except requests.exceptions.RequestException:
        st.error("🔴 Backend Offline\n(Run uvicorn api.main:app)", icon="⚠️")

# ----------------- Sidebar Controls -----------------
st.sidebar.header("🎛️ Operational & Market Levers")

st.sidebar.subheader("📱 Target Smartphone Device")
sku = st.sidebar.selectbox("Active Catalog SKU", ["SKU_MOTO_EDGE_50 (Motorola Edge 50 Pro)"])
base_cost = st.sidebar.number_input("Base Component Procurement BoM (₹)", min_value=15000.0, max_value=32000.0, value=23500.0, step=500.0)
logistics_cost = st.sidebar.number_input("Insured Air Freight & Logistics (₹)", min_value=100.0, max_value=1000.0, value=245.0, step=25.0, help="Adjust to simulate Middle East fuel spikes or express transit insurance.")
current_price = st.sidebar.slider("Current Listing Price on Flipkart (₹)", min_value=22000.0, max_value=38000.0, value=29999.0, step=500.0)

st.sidebar.subheader("🏢 Rival Intelligence (Amazon India)")
competitor_price = st.sidebar.slider("Competitor Price (OnePlus Nord 4 / Redmi) (₹)", min_value=22000.0, max_value=38000.0, value=28999.0, step=500.0)
inventory = st.sidebar.slider("Warehouse Inventory (Phones)", min_value=0, max_value=120, value=35, step=1)
google_trend = st.sidebar.slider("Google Trends Search Index for Motorola (0-100)", min_value=10, max_value=100, value=65, step=5)

st.sidebar.subheader("📅 Temporal Constraints")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    is_weekend = st.toggle("Weekend Surge?", value=False)
with col_s2:
    is_festival = st.toggle("Festival / BBD Sale?", value=False)

# ----------------- Dispatch to API -----------------
payload = {
    "sku_id": "SKU_MOTO_EDGE_50",
    "our_listing_price": float(current_price),
    "competitor_price": float(competitor_price),
    "base_cost": float(base_cost),
    "logistics_cost": float(logistics_cost),
    "inventory_level": int(inventory),
    "is_weekend": 1 if is_weekend else 0,
    "is_festival": 1 if is_festival else 0,
    "google_trend_index": int(google_trend),
    "day_of_week": 5 if is_weekend else 2,
    "month": 10 if is_festival else 4,
    "demand_lag_1": 28.0,
    "demand_lag_7": 26.0,
    "rolling_mean_demand_7d": 27.5
}

response_data = None
try:
    api_resp = requests.post(API_URL, json=payload, timeout=2)
    if api_resp.status_code == 200:
        response_data = api_resp.json()
    else:
        st.error(f"API Error [{api_resp.status_code}]: {api_resp.text}")
except requests.exceptions.RequestException:
    st.warning("⚠️ FastAPI Backend is not responding. Please start it using: `uvicorn api.main:app --reload`")

# ----------------- Executive KPI Cards -----------------
if response_data:
    pricing = response_data["pricing_recommendation"]
    rec_price = pricing["recommended_price_inr"]
    pred_demand = response_data["forecasted_demand_units"]
    price_delta = round(rec_price - current_price, 2)
    profit_margin = pricing["projected_profit_margin_inr"]
    margin_pct = pricing["profit_margin_percentage"]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="Recommended Dynamic Price",
            value=f"₹{rec_price:,.2f}",
            delta=f"{price_delta:+,.2f} INR",
            delta_color="normal"
        )
    with kpi2:
        st.metric(
            label="Predicted Demand (Next 24h)",
            value=f"{pred_demand} Phones",
            delta="High Velocity" if pred_demand > 35 else "Normal Velocity"
        )
    with kpi3:
        st.metric(
            label="Projected Unit Net Margin",
            value=f"₹{profit_margin:,.2f}",
            delta=f"{margin_pct:.1f}% Margin"
        )
    with kpi4:
        if pricing["stockout_risk_flag"]:
            st.error("🚨 Critical Stock Depletion\n(Warehouse Stockout Risk)")
        else:
            st.success("📦 Warehouse Health: Healthy")

    # Strategy Explanation Box
    st.info(
        f"💡 **Pricing Strategy:** {pricing['pricing_strategy']}  |  "
        f"**Landed Cost:** ₹{pricing['landed_cost_inr']:,.2f}  |  "
        f"**Protected Margin Floor:** ₹{pricing['absolute_min_floor_inr']:,.2f}"
    )

st.divider()

# ----------------- Interactive Visual Analytics -----------------
col_chart1, col_chart2 = st.columns([3.2, 2])

with col_chart1:
    st.subheader("📈 Historical Motorola Demand vs. Censored Actual Sales")
    if os.path.exists(DATASET_PATH):
        df_hist = pd.read_csv(DATASET_PATH)
        df_hist["Date"] = pd.to_datetime(df_hist["Date"], dayfirst=True, format="mixed")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_hist["Date"],
            y=df_hist["True_Demand_Units"],
            name="True Unconstrained Demand",
            line=dict(color="#2563EB", width=2.5)
        ))
        fig.add_trace(go.Bar(
            x=df_hist["Date"],
            y=df_hist["Actual_Units_Sold"],
            name="Actual Sales (Censored by Stock)",
            marker_color="#94A3B8",
            opacity=0.45
        ))
        fig.update_layout(
            height=370,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", y=1.12),
            xaxis_title="Date",
            yaxis_title="Units (Phones)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run `data/build_master_dataset.py` to generate the Motorola dataset.")

with col_chart2:
    st.subheader("📊 Price Sensitivity vs. Inventory")
    # Simulate price adjustment curve as inventory drains
    inv_levels = list(range(5, 75, 10))
    sim_prices = []
    for inv in inv_levels:
        sim_multiplier = 1.0 + (0.08 if inv < 12 else 0.0) - (0.04 if inv > 45 else 0.0)
        sim_prices.append(round(current_price * sim_multiplier, 2))

    fig_sim = px.line(
        x=inv_levels,
        y=sim_prices,
        markers=True,
        labels={"x": "Warehouse Inventory (Phones)", "y": "Calculated Price (₹)"},
        title="Motorola Dynamic Price vs. Inventory Level"
    )
    fig_sim.update_traces(line_color="#E11D48", line_width=3)
    fig_sim.update_layout(height=370, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_sim, use_container_width=True)