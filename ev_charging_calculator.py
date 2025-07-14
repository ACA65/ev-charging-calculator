import streamlit as st

st.title("🔌 EV Charging Requirements Calculator")

st.markdown("""
This tool helps estimate the required charging power and number of charge points 
based on EV battery specs, SoC, and dwell time.
""")

# Inputs
num_vehicles = st.number_input("Number of Vehicles", min_value=1, value=5)
battery_kwh = st.number_input("Battery Capacity per Vehicle (kWh)", min_value=10.0, value=100.0)
soc_start = st.slider("State of Charge at Arrival (%)", 0, 100, 20) / 100
soc_end = st.slider("Required State of Charge Before Departure (%)", 0, 100, 80) / 100
dwell_time = st.number_input("Available Dwell Time per Vehicle (in hours)", min_value=0.1, value=1.0)
efficiency = st.slider("Charging Efficiency", min_value=0.5, max_value=1.0, value=0.9)

# Calculation
energy_needed = battery_kwh * (soc_end - soc_start)
energy_with_losses = energy_needed / efficiency
power_per_vehicle = energy_with_losses / dwell_time
total_power = power_per_vehicle * num_vehicles

# Outputs
st.subheader("🔍 Results")
st.write(f"⚡ Energy needed per vehicle: **{energy_with_losses:.2f} kWh**")
st.write(f"⚡ Charging power per vehicle: **{power_per_vehicle:.2f} kW**")
st.write(f"⚡ Total site power required: **{total_power:.2f} kW**")
st.write(f"🔌 Recommended number of charging points: **{num_vehicles}**")
