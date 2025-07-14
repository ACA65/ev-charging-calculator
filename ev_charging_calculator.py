import streamlit as st
import pandas as pd

st.title("🔌 EVessel Charging Infrastructure Sizing Tool")

st.markdown("""
This tool estimates the number of chargers and required power based on eVessel operations 
using Candela P-12 parameters or custom input.
""")

# Option: Load default values
use_defaults = st.checkbox("Use Candela P-12 Defaults", value=True)

if use_defaults:
    battery_kwh = 252
    consumption_per_nm = 0.8
    trip_distance_nm = 12.5
    round_trips_per_day = 4
    dwell_time_hours = 6.0
    charging_efficiency = 0.9
else:
    battery_kwh = st.number_input("Battery Capacity per Vessel (kWh)", min_value=10.0, value=252.0)
    consumption_per_nm = st.number_input("Energy Consumption per Nautical Mile (kWh/NM)", min_value=0.1, value=0.8)
    trip_distance_nm = st.number_input("One-Way Trip Distance (NM)", min_value=1.0, value=12.5)
    round_trips_per_day = st.number_input("Round Trips per Day per Vessel", min_value=1, value=4)
    dwell_time_hours = st.number_input("Charging Time per Vessel per Day (hours)", min_value=0.1, value=6.0)
    charging_efficiency = st.slider("Charging Efficiency", min_value=0.5, max_value=1.0, value=0.9)

# Fleet size
num_vessels_total = st.number_input("Total Number of Vessels", min_value=1, value=10)
num_vessels_active = st.number_input("Number of Vessels Operating at a Time", min_value=1, max_value=num_vessels_total, value=5)

# Charging behavior
charging_strategy = st.radio(
    "Charging Behavior",
    ["All vessels charge concurrently", "Staggered charging with offset arrival"],
    index=0
)

# CapEx cost estimates
cost_per_kw = st.number_input("Estimated Installed Cost per kW (USD)", min_value=100.0, value=800.0)
cost_per_point = st.number_input("Estimated Cost per Charging Point (USD)", min_value=1000.0, value=20000.0)

# Core calculation
trip_energy = trip_distance_nm * 2 * consumption_per_nm
daily_energy_per_vessel = trip_energy * round_trips_per_day
energy_with_losses = daily_energy_per_vessel / charging_efficiency
power_per_vessel = energy_with_losses / dwell_time_hours

if charging_strategy == "All vessels charge concurrently":
    concurrent_vessels = num_vessels_active
else:
    concurrent_vessels = max(1, round(num_vessels_active / 2))  # assume staggered charging across 2 time windows

total_power_required = power_per_vessel * concurrent_vessels
estimated_total_cost = total_power_required * cost_per_kw + concurrent_vessels * cost_per_point

# Outputs
st.subheader("🔍 Results Summary")
st.write(f"🛥️ Energy used per round trip: **{trip_energy:.2f} kWh**")
st.write(f"🔋 Daily energy need per vessel: **{daily_energy_per_vessel:.2f} kWh**")
st.write(f"⚡ Charging power per vessel: **{power_per_vessel:.2f} kW**")
st.write(f"🔌 Concurrent vessels charging: **{concurrent_vessels}**")
st.write(f"⚡ Total site power required: **{total_power_required:.2f} kW**")
st.write(f"💰 Estimated infrastructure cost: **USD {estimated_total_cost:,.0f}**")

# Export section
st.subheader("📤 Export Results")

df_export = pd.DataFrame({
    "Metric": [
        "Trip Distance (NM)",
        "Energy per Round Trip (kWh)",
        "Daily Energy per Vessel (kWh)",
        "Charging Efficiency",
        "Charging Time per Vessel (h)",
        "Charging Power per Vessel (kW)",
        "Vessels Charging Concurrently",
        "Total Site Power Required (kW)",
        "CapEx per kW (USD)",
        "CapEx per Point (USD)",
        "Total Estimated Cost (USD)"
    ],
    "Value": [
        trip_distance_nm,
        trip_energy,
        daily_energy_per_vessel,
        charging_efficiency,
        dwell_time_hours,
        power_per_vessel,
        concurrent_vessels,
        total_power_required,
        cost_per_kw,
        cost_per_point,
        estimated_total_cost
    ]
})

csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download CSV Report",
    data=csv,
    file_name='evessel_charging_sizing.csv',
    mime='text/csv'
)
