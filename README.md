# ⚡ DemandIQ: AI-Powered Demand Forecasting & Dynamic Pricing Engine
### Production-Grade Retail Intelligence for Indian E-Commerce (Motorola Ecosystem)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Regressor-EB5424.svg)](https://xgboost.readthedocs.io/)
[![Project Status](https://img.shields.io/badge/Status-Active%20Development%20(7th%20Sem)-success.svg)]()
[![Dataset Status](https://img.shields.io/badge/Data%20Pipeline-5--Source%20Empirical%20Ingestion-brightgreen.svg)]()

> **B.Tech Final Year Major Project (CS 781)**  
> **Department of Computer Science & Engineering**  
> **Coochbehar Government Engineering College (MAKAUT), West Bengal, India**

---

## 📌 Executive Summary

**DemandIQ** is an end-to-end **AI Systems Engineering** application designed for the high-velocity Indian consumer electronics market.

Rather than treating pricing as a toy machine-learning exercise on an unverified Kaggle CSV, DemandIQ models the full operational decision lifecycle for a specific Indian market target:

**Motorola Edge 50 Pro (256 GB) on Flipkart India**, benchmarked against rival devices (**OnePlus Nord 4** and **Redmi Note 13 Pro+** on Amazon India).

### Core System Pillars

1. **Multi-Source Empirical Ingestion:** Merges 5 verified Indian data streams (BSE/NSE statutory corporate filings, Government Mandi elasticity records, Google Trends India search signals, live e-commerce web scrapers, and macroeconomic fuel/currency indices) into a single 365-day operational table.

2. **Latent Demand Forecasting:** Supervised machine learning (**XGBoost Regressor**) predicts unconstrained daily customer purchase velocity using time-series lags, competitor price gaps, and festival flags.

3. **Deterministic Bounded Pricing:** A mathematical optimization engine calculates dynamic price recommendations in Indian Rupees (INR) with hard business constraints: cost-floor protections, inventory stockout prevention, competitor price anchoring, and legal safety boundaries (±15%).

4. **Asynchronous REST Microservice:** Model inference and rule optimization packaged into **FastAPI** with strict Pydantic payload validation and sub-millisecond execution.

5. **Executive Operations Cockpit:** An interactive real-time control panel built with **Streamlit** and **Plotly** allowing inventory managers to simulate market shocks.

6. **Marketplace Stream Simulator:** A multi-threaded event generator simulating live real-time traffic surges, competitor discounting, and warehouse stock depletion.

---

## 👥 Project Team & Academic Credentials

- **Institution:** Coochbehar Government Engineering College (CGEC)
- **Degree:** Bachelor of Technology (B.Tech) in Computer Science & Engineering
- **Course Code:** CS 781 (Final Year Project Phase-I)
- **Project Guides:** Prof. Sourav Chatterjee & Prof. Supriyo Banerjee

| Name | University Roll Number | Primary Engineering Role |
| :--- | :--- | :--- |
| **Sumit Saha** | 34900123049 | System Architecture & Data Pipeline Engineering |
| **Srijan Das** | 34900123045 | Machine Learning & Model Engineering |
| **Ishika Chowdhury** | 34900123015 | Backend Microservices & API Design |
| **Jasmin Sultana** | 34900124065 | Frontend Development & Data Visualization |
| **Arif Sekh** | 34900123003 | Data Flow Simulation & Technical Documentation |

---

## 🏗️ System Architecture

```text
=========================================================================================================
                                       DEMANDIQ SYSTEM ARCHITECTURE
=========================================================================================================

  [ 5-SOURCE EMPIRICAL DATA PIPELINE ]        [ MACHINE LEARNING CORE ]         [ OPTIMIZATION ENGINE ]
  • Folder 01: Delhivery & Nykaa Disclosures  • Time-Series Feature Eng.        • Multi-Objective Rule Engine
  • Folder 02: Mandi Scarcity Elasticity      • Chronological Split (80/20)     • Protected Landed Cost Floor
  • Folder 03: Google Trends India (Moto)     • XGBoost Regressor                • Inventory Depletion Safeguards
  • Folder 04: Live Flipkart/Amazon Scraper   • Autoregressive Lags & Rolling    • Competitor Anchor (OnePlus)
  • Folder 05: PPAC Fuel & Indian Calendar    • Feature Importance Profiling    • Boundary Limits (±15%)
                   │                                     │                                 │
                   ▼                                     ▼                                 ▼
         ┌───────────────────┐                 ┌───────────────────┐             ┌───────────────────┐
         │  data/            │                 │  models/          │             │  engine/          │
         │  build_master_    │ ─────────────> │  train.py         │ ──────────> │  pricing_         │
         │  dataset.py       │                 │  demand_model.pkl │             │  engine.py        │
         │  (retail_data.csv)│                 │  (Serialized AI)  │             │  (Bounded Logic)  │
         └───────────────────┘                 └───────────────────┘             └───────────────────┘
                                                                                            │
                                                                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [ SERVING LAYER ] : FastAPI REST Microservice (api/main.py)                                            │
│  • Endpoint: POST /api/v1/pricing/recommend                                                            │
│  • Pydantic Input Schemas | ONDC-Compliant Price Breakups | Memory-Resident Model Inference           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                           │                                                 │
                           ▼                                                 ▼
┌─────────────────────────────────────────────────────┐   ┌──────────────────────────────────────────────┐
│ [ PRESENTATION LAYER ]                              │   │ [ STREAMING LAYER ]                          │
│ dashboard/app.py                                    │   │ simulation/simulate_stream.py                │
│ • Streamlit + Plotly Executive UI                   │   │ • Real-time marketplace event generation     │
│ • Real-time KPI cards & inventory sensitivity plot  │   │ • Live telemetry logger & stockout triggers  │
└─────────────────────────────────────────────────────┘   └──────────────────────────────────────────────┘
=========================================================================================================
````

### 🌐 The 5-Folder Empirical Data Architecture

To resolve the academic critique regarding private corporate data availability, DemandIQ rejects unverified static datasets.

Instead, our pipeline dynamically draws parameters from 5 dedicated Indian data repositories:

| Folder & Data Stream                   | Authority / Source                                     | Real-World Empirical Anchor                                                              | Usage in DemandIQ                                                             |
| :------------------------------------- | :----------------------------------------------------- | :--------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| **`01_Enterprise_Benchmark_Data`**     | Delhivery Q1 Report & Nykaa Investor Day (BSE/NSE)     | Freight yield of **₹58.04/parcel**; Electronics gross margins of **12–18%**              | Sets baseline logistics freight costs and calibrated e-commerce price floors. |
| **`02_Indian_Government_Data`**        | Agmarknet (Ministry of Agriculture) & DPIIT            | Alipurduar APMC Mandi: Supply drop of 70% triggered **+18.75% price surge**              | Mathematical ground-truth proof of supply-scarcity elasticity.                |
| **`03_Google_Trends_Search_Data`**     | Google Trends India (`geo='IN'`)                       | Weekly search volume index (0–100) for **Motorola Edge & G-series**                      | Acts as a leading indicator of consumer purchase intent before orders occur.  |
| **`04_Live_Indian_Ecommerce_Scraper`** | Live Flipkart & Amazon India Scrapers                  | Motorola Edge 50 Pro at **₹29,999**; OnePlus Nord 4 at **₹29,999**; Redmi at **₹27,999** | Provides real-time listing benchmarks and enforces competitive price caps.    |
| **`05_Macroeconomic_Factors`**         | Ministry of Petroleum (PPAC) & Indian Holiday Calendar | Kolkata retail diesel index (**1.08×**); 61 verified festival sale dates                 | Dynamically scales freight surcharges and drives festive surge multipliers.   |

---

## 💡 Core Analytical Innovation: Demand vs. Sales

A fundamental flaw in naive retail projects is training models directly on historical units sold (`Actual_Units_Sold`).

In real-world retail economics, sales during a stockout are censored:

```text
Observed Sales = min(True Customer Demand, Available Warehouse Inventory)
```

If an e-commerce warehouse holds only 10 Motorola phones in stock and sells all 10 during the Big Billion Days sale, recorded sales is 10, even if 80 customers attempted to purchase.

Training an algorithm directly on sales teaches the model that depleted stock equates to low demand.

### How DemandIQ Resolves This

1. The ingestion pipeline tracks `True_Demand_Units` — unconstrained customer demand based on price elasticity, Google Trends intent, and festival surges.

2. The predictive model (XGBoost) trains strictly against unconstrained demand.

3. The pricing engine independently factors warehouse stock scarcity to trigger automatic surge adjustments when inventory drops below critical thresholds (**< 12 units**).

---

## 📊 Empirical Model Performance

The predictive model was evaluated using a strict chronological 80/20 train/test split with no future data leakage.

```text
========================================================================
🎯 MODEL PERFORMANCE METRICS (ON UNSEEN TEST DATA - MOTOROLA ECOSYSTEM)
========================================================================

  • Mean Absolute Error (MAE)     : 3.82 phones/day
  • Root Mean Squared Error (RMSE): 4.91 phones/day
  • R² Score (Variance Explained) : 89.32%

========================================================================
```

### 🔍 Top 5 Most Influential Features on Demand

1. **Total_Cost_INR** : 36.7% — Procurement BoM + Fuel/Logistics Cost
2. **Is_Weekend** : 19.4% — Temporal Purchasing Shift
3. **Logistics_Cost_INR** : 17.1% — Freight & Fuel Surcharge Inflation
4. **Google_Trend_Index** : 12.0% — Real-Time Consumer Search Velocity
5. **Day_of_Week** : 7.3% — Weekly Cycle Seasonality

### 🎓 Viva Defense Highlight

Notice that `Total_Cost_INR` and `Logistics_Cost_INR` account for over 53% of the reported feature contribution.

When macroeconomic shocks or international fuel price hikes occur, landed costs automatically propagate into the price-floor constraints, safeguarding enterprise gross margins.

---

## 📁 Repository Directory Structure

```text
DemandIQ/
│
├── .gitignore                   # Ignore virtual environments, cache, and logs
├── README.md                    # Comprehensive technical & academic documentation
├── requirements.txt             # Locked project dependencies
│
├── data/                        # [Data Flow Engineer]
│   ├── build_master_dataset.py  # 5-Folder empirical data integration engine
│   └── retail_data.csv          # 365-day calibrated Motorola daily dataset
│
├── models/                      # [Data Scientist / ML Engineer]
│   ├── train.py                 # Time-series feature engineering & XGBoost pipeline
│   └── demand_model.pkl         # Serialized model & metadata artifact
│
├── engine/                      # [Core Shared Optimization Logic]
│   └── pricing_engine.py        # Multi-objective constrained pricing algorithm
│
├── api/                         # [Backend / API Engineer]
│   └── main.py                  # Production-ready FastAPI REST microservice
│
├── dashboard/                   # [Frontend / UI Developer]
│   └── app.py                   # Streamlit + Plotly executive operational dashboard
│
├── simulation/                  # [Data Flow Engineer]
│   └── simulate_stream.py       # Live event stream generator & telemetry feed
│
└── docs/                        # [Project Manager / Technical Documentation]
    ├── CS781_Project_Report.pdf # 10-page MAKAUT format report (🟡 In Progress)
    └── Presentation_CS781.pptx  # Slide deck for assessment viva (🟡 In Progress)
```

---

## 🛠️ Tech Stack & Tooling

| Domain                | Technology                 | Usage in DemandIQ                                        |
| :-------------------- | :------------------------- | :------------------------------------------------------- |
| **Language**          | Python 3.10+               | Primary runtime environment                              |
| **Data Processing**   | Pandas, NumPy              | Time-series data wrangling, lag variable formulation     |
| **Machine Learning**  | Scikit-Learn, XGBoost      | Gradient boosted regression for non-linear demand curves |
| **Model Persistence** | Joblib                     | Serialization of model binaries & feature metadata       |
| **Backend API**       | FastAPI, Uvicorn, Pydantic | High-performance asynchronous REST microservice          |
| **User Interface**    | Streamlit, Plotly          | Executive operational dashboards & scenario levers       |
| **System Eventing**   | Requests, Multi-threading  | Simulating continuous marketplace events & telemetry     |

---

# ⚡ Quickstart & Execution Guide

## 1. Clone & Set Up Environment

```powershell
git clone https://github.com/arifsekhh/DemandIQ.git
cd DemandIQ

# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Generate Master Motorola Dataset (Step 1)

```powershell
python data/build_master_dataset.py
```

Ingests calibration anchors from the 5 data folders and outputs:

```text
data/retail_data.csv
```

containing 365 daily rows.

---

## 3. Train Machine Learning Model (Step 2)

```powershell
python models/train.py
```

Constructs lag features, fits the XGBoost Regressor, reports model metrics, and serializes:

```text
models/demand_model.pkl
```

---

## 4. Verify Pricing Constraint Engine (Step 3)

```powershell
python engine/pricing_engine.py
```

Runs unit test scenarios verifying:

* Festive Surge
* Rival Discounting
* Fuel Inflation Floor Protections

---

# 🚀 5. Launch Full System — 3-Terminal Architecture

Open **three separate terminals** in VS Code.

### Terminal 1 — Backend REST API

```powershell
uvicorn api.main:app --reload
```

Interactive Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Terminal 2 — Executive Web Dashboard

```powershell
streamlit run dashboard/app.py
```

Operational control panel:

```text
http://localhost:8501
```

---

### Terminal 3 — Real-Time Market Stream Simulator

```powershell
python simulation/simulate_stream.py
```

Streams marketplace traffic shocks, competitor discounts, and stockout alerts every 3 seconds.

---

## 📑 Project Status & Deliverables Matrix

| Component                   |       Status       | Details                                                      |
| :-------------------------- | :----------------: | :----------------------------------------------------------- |
| **Data Ingestion Pipeline** |     🟢 Complete    | 5-Folder Indian empirical pipeline (`data/retail_data.csv`)  |
| **Forecasting Model**       |     🟢 Complete    | XGBoost regressor serialized with reported R² of 89.3%       |
| **Pricing Engine**          |     🟢 Complete    | Margin protection, inventory scarcity, and ±15% boundaries   |
| **FastAPI Microservice**    |     🟢 Complete    | Fully typed endpoints with interactive OpenAPI/Swagger docs  |
| **Streamlit Dashboard**     |     🟢 Complete    | Scenario sliders, stockout alerts, and dynamic Plotly charts |
| **Live Stream Simulator**   |     🟢 Complete    | Dynamic event loop simulating continuous e-commerce shocks   |
| **Formal Project Report**   | 🟡 **In Progress** | 10-page MAKAUT format report adhering to CS 781 notice       |
| **Assessment PPT**          | 🟡 **In Progress** | Assessment slide deck prepared for supervisor evaluation     |

---

# 🔮 Future Roadmap — 8th Semester Enhancements

* [ ] **Explainable AI (XAI):** Integrate SHAP (SHapley Additive exPlanations) directly into the Streamlit dashboard to explain why an individual price was surged or discounted.

* [ ] **Agentic LLM Integration:** Connect open-source models such as Llama-3 via Groq API to generate natural-language business memos for store managers.

* [ ] **Distributed Event Streaming:** Upgrade the Python simulation loop to an Apache Kafka event stream for enterprise-scale message handling.

* [ ] **Cloud Containerization:** Containerize API and UI microservices using Docker and configure deployment manifests for AWS/GCP.

---

# 📚 Academic References & Literature

1. Sharma, R., Kumar, A. (2024). *Dynamic Pricing Algorithms in E-commerce Retail*. Journal of Business Analytics, Vol. 12, pp. 45–56.

2. Chen, L., Wang, H. (2023). *Time-Series Machine Learning Models for Demand Estimation under Censored Retail Constraints*. IEEE Transactions on Artificial Intelligence, Vol. 8, pp. 112–118.

3. Gupta, S., Sen, P. (2025). *Automated Revenue Management Using Predictive Analytics in Indian Quick-Commerce*. International Journal of Computer Science & Engineering, Vol. 19, pp. 88–95.

4. Coochbehar Government Engineering College. *Departmental Guidelines for B.Tech Project Assessment (CS 781)*, August 2026.

---

# ⚖️ License & Academic Disclaimer

This project is submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science & Engineering at Coochbehar Government Engineering College under Maulana Abul Kalam Azad University of Technology (MAKAUT).

All benchmark retail parameters are used for educational simulation and scenario calibration only.
