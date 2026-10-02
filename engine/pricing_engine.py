"""
Dynamic Pricing Rule & Constraint Optimization Engine (Motorola Smartphone Edition)
Calculates optimal selling price for Motorola Edge 50 Pro based on predicted demand,
competitor benchmarks (OnePlus/Redmi), inventory scarcity, and landed cost floors.
"""

def calculate_dynamic_price(
    predicted_demand: float,
    current_inventory: int,
    competitor_price: float,
    base_cost: float,
    logistics_cost: float,
    nominal_price: float = 29999.0,     # Motorola Edge 50 Pro MSRP benchmark
    min_margin_pct: float = 0.10,       # 10% minimum profit margin for consumer electronics
    max_price_cap_pct: float = 0.15,    # Max price cannot exceed +15% (₹34,499)
    min_price_floor_pct: float = 0.15   # Max discount cannot exceed -15% (₹25,499)
) -> dict:
    landed_cost = base_cost + logistics_cost
    baseline_demand = 28.0  # Average historical daily demand for mid-premium smartphones

    # 1. Cost Floor Guardrail (Strict Profit Margin)
    # Price can never go below landed cost + minimum margin (e.g. fuel inflation defense!)
    absolute_minimum_price = round(landed_cost * (1.0 + min_margin_pct), 2)

    # 2. Demand Surge Multiplier
    demand_ratio = predicted_demand / baseline_demand
    pricing_multiplier = 1.0 + (demand_ratio - 1.0) * 0.18

    # 3. Inventory Scarcity Adjustment
    # If stock is critically low (< 12 phones) and demand is high, increase price slightly
    stockout_risk = False
    if current_inventory < 12 and predicted_demand > 25:
        pricing_multiplier += 0.05
        stockout_risk = True

    # 4. Preliminary Calculated Price
    suggested_price = nominal_price * pricing_multiplier

    # 5. Competitor Anchoring (OnePlus Nord / Redmi Note on Amazon)
    # If our price is > 6% above competitor, pull back to remain competitive
    if not stockout_risk and suggested_price > (competitor_price * 1.06):
        suggested_price = competitor_price * 1.03

    # 6. Apply Boundary Constraints (Safety Checks)
    upper_limit = nominal_price * (1.0 + max_price_cap_pct)
    lower_limit = max(nominal_price * (1.0 - min_price_floor_pct), absolute_minimum_price)

    final_price = round(min(max(suggested_price, lower_limit), upper_limit), 2)

    # 7. Generate Business Rationale
    if final_price > nominal_price:
        if stockout_risk:
            strategy = "Surge Pricing: Critical stock depletion + High demand spike"
        else:
            strategy = "Surge Pricing: Elevated festive demand detected"
    elif final_price < nominal_price:
        strategy = "Discount Pricing: Clearing inventory against aggressive rival pricing"
    else:
        strategy = "Standard Neutral Pricing: Balanced supply and market demand"

    profit_margin_inr = round(final_price - landed_cost, 2)
    profit_margin_pct = round((profit_margin_inr / final_price) * 100, 2)

    return {
        "recommended_price_inr": final_price,
        "nominal_price_inr": nominal_price,
        "absolute_min_floor_inr": absolute_minimum_price,
        "landed_cost_inr": landed_cost,
        "projected_profit_margin_inr": profit_margin_inr,
        "profit_margin_percentage": profit_margin_pct,
        "pricing_strategy": strategy,
        "stockout_risk_flag": stockout_risk
    }


# Standalone Test Execution
if __name__ == "__main__":
    print("=" * 65)
    print("🧪 TESTING DYNAMIC PRICING ENGINE (MOTOROLA EDGE 50 PRO)")
    print("=" * 65)

    # Scenario A: Big Billion Days Festive Rush + Low Warehouse Stock
    print("\n[Scenario A: Flipkart Big Billion Days Surge + Low Inventory]")
    res_a = calculate_dynamic_price(
        predicted_demand=58.0,
        current_inventory=8,
        competitor_price=29999.0, # OnePlus Nord 4
        base_cost=23500.0,
        logistics_cost=285.0
    )
    for k, v in res_a.items():
        print(f"  • {k:<28}: {v}")

    # Scenario B: Rival Smartphone Discounting on Amazon
    print("\n[Scenario B: Redmi/OnePlus Discount Slump]")
    res_b = calculate_dynamic_price(
        predicted_demand=18.0,
        current_inventory=65,
        competitor_price=26999.0, # Aggressive rival discount
        base_cost=23500.0,
        logistics_cost=240.0
    )
    for k, v in res_b.items():
        print(f"  • {k:<28}: {v}")

    # Scenario C: Fuel Shock / Logistics Surcharge Rise (War Question!)
    print("\n[Scenario C: Fuel Surcharge / High Shipping Inflation]")
    res_c = calculate_dynamic_price(
        predicted_demand=28.0,
        current_inventory=35,
        competitor_price=29499.0,
        base_cost=23500.0,
        logistics_cost=650.0 # Spiked freight/insurance
    )
    for k, v in res_c.items():
        print(f"  • {k:<28}: {v}")