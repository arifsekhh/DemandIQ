"""
DemandIQ: FastAPI REST Backend Engine (Motorola Edge 50 Pro Edition)
Exposes high-performance inference endpoints for XGBoost demand forecasting
and deterministic dynamic pricing optimization.
"""

import sys
import os
import joblib
import pandas as pd
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure project root is in sys.path so we can import engine modules safely
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.pricing_engine import calculate_dynamic_price

app = FastAPI(
    title="DemandIQ Operations Engine API",
    description="Production-grade AI Demand Forecasting & Dynamic Pricing Service for Indian E-Commerce",
    version="2.0.0"
)

# Enable CORS for dashboard communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Global Model Loader -----------------
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "demand_model.pkl")
model_artifact = None

@app.on_event("startup")
def load_model():
    global model_artifact
    if not os.path.exists(MODEL_PATH):
        print(f"⚠️ Warning: Model artifact not found at {MODEL_PATH}. Run 'python models/train.py' first!")
        return
    try:
        model_artifact = joblib.load(MODEL_PATH)
        print("✅ DemandIQ Motorola XGBoost Model loaded into memory successfully.")
    except Exception as e:
        print(f"❌ Error loading model artifact: {e}")


# ----------------- Pydantic Input Schema -----------------
class PricingRequest(BaseModel):
    sku_id: str = Field(default="SKU_MOTO_EDGE_50", example="SKU_MOTO_EDGE_50")
    our_listing_price: float = Field(default=29999.0, ge=5000.0, example=29999.0)
    competitor_price: float = Field(default=28999.0, ge=5000.0, example=28999.0)
    base_cost: float = Field(default=23500.0, ge=1000.0, example=23500.0)
    logistics_cost: float = Field(default=245.0, ge=50.0, example=245.0)
    inventory_level: int = Field(default=35, ge=0, example=35)
    is_weekend: int = Field(default=0, ge=0, le=1, example=0)
    is_festival: int = Field(default=0, ge=0, le=1, example=0)
    google_trend_index: int = Field(default=55, ge=0, le=100, example=55)
    day_of_week: int = Field(default=2, ge=0, le=6, example=2)
    month: int = Field(default=10, ge=1, le=12, example=10)
    
    # Historical rolling lag proxies (calibrated for Motorola baseline)
    demand_lag_1: Optional[float] = Field(default=28.0, example=28.0)
    demand_lag_7: Optional[float] = Field(default=26.0, example=26.0)
    rolling_mean_demand_7d: Optional[float] = Field(default=27.5, example=27.5)


# ----------------- Endpoints -----------------
@app.get("/")
def healthcheck():
    return {
        "status": "Online",
        "service": "DemandIQ Core API (Motorola Edition)",
        "model_loaded": model_artifact is not None,
        "docs_url": "/docs"
    }


@app.post("/api/v1/pricing/recommend")
def recommend_price(payload: PricingRequest):
    global model_artifact
    if model_artifact is None:
        if os.path.exists(MODEL_PATH):
            model_artifact = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(status_code=500, detail="ML Model artifact not found. Please train the model first.")

    try:
        model = model_artifact["model"]

        # 1. Feature Engineering (Exact match to train.py schema)
        total_cost = payload.base_cost + payload.logistics_cost
        price_margin_ratio = payload.our_listing_price / payload.base_cost
        competitor_price_gap = payload.competitor_price - payload.our_listing_price

        feature_dict = {
            'Our_Listing_Price_INR': [payload.our_listing_price],
            'Competitor_Price_INR': [payload.competitor_price],
            'Base_Cost_INR': [payload.base_cost],
            'Logistics_Cost_INR': [payload.logistics_cost],
            'Total_Cost_INR': [total_cost],
            'Price_Margin_Ratio': [price_margin_ratio],
            'Competitor_Price_Gap': [competitor_price_gap],
            'Is_Weekend': [payload.is_weekend],
            'Is_Festival': [payload.is_festival],
            'Google_Trend_Index': [payload.google_trend_index],
            'Day_of_Week': [payload.day_of_week],
            'Month': [payload.month],
            'Demand_Lag_1': [payload.demand_lag_1],
            'Demand_Lag_7': [payload.demand_lag_7],
            'Rolling_Mean_Demand_7D': [payload.rolling_mean_demand_7d]
        }
        feature_df = pd.DataFrame(feature_dict)

        # 2. Predict Unconstrained Demand with XGBoost
        raw_pred = float(model.predict(feature_df)[0])
        predicted_demand = round(max(1.0, raw_pred), 1)

        # 3. Deterministic Dynamic Pricing Optimization
        pricing_output = calculate_dynamic_price(
            predicted_demand=predicted_demand,
            current_inventory=payload.inventory_level,
            competitor_price=payload.competitor_price,
            base_cost=payload.base_cost,
            logistics_cost=payload.logistics_cost,
            nominal_price=payload.our_listing_price
        )

        return {
            "sku_id": payload.sku_id,
            "forecasted_demand_units": predicted_demand,
            "current_inventory": payload.inventory_level,
            "pricing_recommendation": pricing_output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")