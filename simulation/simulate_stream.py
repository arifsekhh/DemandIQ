"""
DemandIQ: Real-Time Market Event Stream Simulator (Motorola Ecosystem)
Simulates continuous Indian e-commerce market telemetry:
  - Rival smartphone price fluctuations (Amazon India: OnePlus Nord / Redmi Note)
  - Live customer checkout orders draining warehouse inventory
  - Sudden Google Trends search spikes and Flipkart festive sales
  - Dispatches live payloads to FastAPI (/api/v1/pricing/recommend) every 3 seconds
"""

import os
import sys
import time
import random
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/v1/pricing/recommend"

# Real-world market shocks for Motorola Edge 50 Pro on Flipkart India
EVENT_SCENARIOS = [
    {
        "event_name": "Standard Organic Browsing Flow",
        "trend_delta": 0,
        "comp_delta": 0,
        "inventory_drain": 1,
        "is_festival": 0
    },
    {
        "event_name": "OnePlus Nord 4 Flash Discount on Amazon (-₹1,200)",
        "trend_delta": +5,
        "comp_delta": -1200,
        "inventory_drain": 0,
        "is_festival": 0
    },
    {
        "event_name": "Redmi Note Competitor Price Hike (+₹800)",
        "trend_delta": +2,
        "comp_delta": +800,
        "inventory_drain": 2,
        "is_festival": 0
    },
    {
        "event_name": "Flipkart Big Billion Days Flash Sale Surge",
        "trend_delta": +35,
        "comp_delta": -500,
        "inventory_drain": 5,
        "is_festival": 1
    },
    {
        "event_name": "Corporate Bulk Smartphone Procurement (Stock Depleting)",
        "trend_delta": +10,
        "comp_delta": 0,
        "inventory_drain": 7,
        "is_festival": 0
    },
    {
        "event_name": "Late-Night Off-Peak Browsing Lull",
        "trend_delta": -15,
        "comp_delta": -400,
        "inventory_drain": 0,
        "is_festival": 0
    }
]

def run_real_time_simulator(interval_seconds=3):
    print("=" * 85)
    print("📡 DEMANDIQ MOTOROLA REAL-TIME EVENT STREAM SIMULATOR")
    print(f"🎯 Target Endpoint: {API_URL}")
    print(f"⏱️ Ingestion Cadence: 1 Event every {interval_seconds} seconds (Press Ctrl+C to terminate)")
    print("=" * 85)

    # Smartphone initial baseline conditions
    current_inventory = 35
    nominal_price = 29999.0
    competitor_baseline = 28999.0   # Rival benchmark (OnePlus/Redmi)
    base_cost = 23500.0             # Component BoM cost
    logistics_cost = 245.0          # Insured Delhivery freight
    google_trend = 55
    event_counter = 1

    try:
        while True:
            # 1. Pick a random real-world market event
            scenario = random.choice(EVENT_SCENARIOS)

            # 2. Apply market shifts
            current_competitor_price = max(24000.0, competitor_baseline + scenario["comp_delta"])
            current_trend = int(max(10, min(100, google_trend + scenario["trend_delta"])))

            # 3. Simulate customer checkout (warehouse stock drain)
            current_inventory = max(0, current_inventory - scenario["inventory_drain"])

            # 4. Automatic warehouse replenishment when critically depleted
            if current_inventory <= 6:
                print("\n" + "!" * 85)
                print("📦 [WAREHOUSE RESTOCK TRIGGER]: Inventory dropped ≤ 6. Received batch shipment of +35 units!")
                print("!" * 85 + "\n")
                current_inventory += 35

            # 5. Build live API payload
            payload = {
                "sku_id": "SKU_MOTO_EDGE_50",
                "our_listing_price": nominal_price,
                "competitor_price": float(current_competitor_price),
                "base_cost": float(base_cost),
                "logistics_cost": float(logistics_cost),
                "inventory_level": int(current_inventory),
                "is_weekend": 1 if datetime.now().weekday() in [5, 6] else 0,
                "is_festival": scenario["is_festival"],
                "google_trend_index": current_trend,
                "day_of_week": datetime.now().weekday(),
                "month": datetime.now().month,
                "demand_lag_1": 28.0,
                "demand_lag_7": 26.0,
                "rolling_mean_demand_7d": 27.5
            }

            timestamp = datetime.now().strftime("%H:%M:%S")

            # 6. Dispatch HTTP POST request to FastAPI backend
            try:
                response = requests.post(API_URL, json=payload, timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    pricing = data["pricing_recommendation"]

                    rec_price = pricing["recommended_price_inr"]
                    pred_demand = data["forecasted_demand_units"]
                    strategy = pricing["pricing_strategy"]
                    margin_pct = pricing["profit_margin_percentage"]
                    stockout = "🚨 CRITICAL" if pricing["stockout_risk_flag"] else "✅ HEALTHY"

                    print(f"[{timestamp}] Event #{event_counter:<2} | {scenario['event_name'][:40]:<40}")
                    print(f"   ↳ Inflow : Warehouse Stock={current_inventory:<2} | Rival Price=₹{current_competitor_price:<7,.0f} | Search Trend={current_trend}")
                    print(f"   ↳ AI Core: Forecast={pred_demand} phones ➔ Dynamic Price: ₹{rec_price:,.2f} ({strategy})")
                    print(f"   ↳ Health : Margin={margin_pct:.1f}% | Stock Status: {stockout}")
                    print("-" * 85)
                else:
                    print(f"[{timestamp}] ⚠️ API Error [{response.status_code}]: {response.text}")
            except requests.exceptions.RequestException:
                print(f"[{timestamp}] 🔴 Connection Refused! Make sure FastAPI is running (`uvicorn api.main:app --reload`).")

            event_counter += 1
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n🛑 Event stream simulation halted cleanly by user.")

if __name__ == "__main__":
    run_real_time_simulator()