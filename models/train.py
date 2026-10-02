"""
DemandIQ: XGBoost Time-Series Training Pipeline (Motorola Edition)
Uses pure NumPy for regression metrics to avoid Windows Application Control DLL blocks.
"""

import os
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

def load_and_engineer_features(data_path="data/retail_data.csv"):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run data/build_master_dataset.py first!")

    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    # 1. Economic / Pricing Features
    df['Price_Margin_Ratio'] = df['Our_Listing_Price_INR'] / df['Base_Cost_INR']
    df['Competitor_Price_Gap'] = df['Competitor_Price_INR'] - df['Our_Listing_Price_INR']
    df['Total_Cost_INR'] = df['Base_Cost_INR'] + df['Logistics_Cost_INR']

    # 2. Calendar / Temporal Features
    df['Day_of_Week'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month

    # 3. Time-Series Lag & Rolling Window Features (No lookahead bias)
    df['Demand_Lag_1'] = df['True_Demand_Units'].shift(1)
    df['Demand_Lag_7'] = df['True_Demand_Units'].shift(7)
    df['Rolling_Mean_Demand_7D'] = df['True_Demand_Units'].shift(1).rolling(window=7).mean()

    # Drop the first 7 rows containing NaNs from lagging
    df = df.dropna().reset_index(drop=True)
    return df

def calculate_metrics_numpy(y_true, y_pred):
    """Computes MAE, RMSE, and R2 using pure NumPy (zero DLL dependencies)."""
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)

    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = float(1.0 - (ss_res / ss_tot)) if ss_tot != 0 else 0.0
    
    return mae, rmse, r2

def train_demand_model():
    print("⏳ Loading Motorola dataset and engineering features...")
    df = load_and_engineer_features()

    feature_cols = [
        'Our_Listing_Price_INR',
        'Competitor_Price_INR',
        'Base_Cost_INR',
        'Logistics_Cost_INR',
        'Total_Cost_INR',
        'Price_Margin_Ratio',
        'Competitor_Price_Gap',
        'Is_Weekend',
        'Is_Festival',
        'Google_Trend_Index',
        'Day_of_Week',
        'Month',
        'Demand_Lag_1',
        'Demand_Lag_7',
        'Rolling_Mean_Demand_7D'
    ]
    target_col = 'True_Demand_Units'

    X = df[feature_cols]
    y = df[target_col]

    # Chronological Time-Series Split (80% Train, 20% Test)
    train_size = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

    print(f"📊 Training records: {len(X_train)} | Test records: {len(X_test)}")
    print("🚀 Training XGBoost Demand Regressor for Motorola Edge 50...")

    model = XGBRegressor(
        n_estimators=120,
        learning_rate=0.06,
        max_depth=4,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate predictions using pure NumPy
    y_pred = model.predict(X_test)
    mae, rmse, r2 = calculate_metrics_numpy(y_test, y_pred)

    print("\n" + "=" * 50)
    print("🎯 MODEL PERFORMANCE METRICS (ON UNSEEN TEST DATA)")
    print("=" * 50)
    print(f"  • Mean Absolute Error (MAE) : {mae:.2f} phones")
    print(f"  • Root Mean Squared Error (RMSE): {rmse:.2f} phones")
    print(f"  • R² Score (Variance Explained): {r2 * 100:.2f}%")
    print("=" * 50)

    # Feature Importance Analysis
    importance_df = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    print("\n🔍 Top 5 Most Influential Features on Demand:")
    for _, row in importance_df.head(5).iterrows():
        print(f"   {row['Feature']:<25} : {row['Importance'] * 100:.1f}%")

    # Serialize Model & Metadata
    os.makedirs("models", exist_ok=True)
    artifact = {
        "model": model,
        "features": feature_cols,
        "metrics": {"mae": mae, "rmse": rmse, "r2": r2}
    }
    artifact_path = "models/demand_model.pkl"
    joblib.dump(artifact, artifact_path)
    print(f"\n💾 Model successfully serialized to: {artifact_path}")

if __name__ == "__main__":
    train_demand_model()