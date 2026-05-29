import streamlit as st
import joblib
import numpy as np
import json

# Load model and data
model = joblib.load('crop_yield_model_small.pkl')
with open('avg_values.json', 'r') as f:
    avg_dict = json.load(f)

# Get unique districts and crops
districts = sorted(set(k.split('_')[0] for k in avg_dict.keys()))
crops = ['chickpea', 'cotton', 'maize', 'rice']

# Title
st.title("🌾 Farmer Crop Loss Predictor")
st.subheader("Tamil Nadu Future Crop Yield Prediction")
st.write("Select Year, District and Crop — rest fills automatically!")

# Main inputs
year = st.number_input("📅 Year", 2024, 2035, 2025)
district = st.selectbox("📍 Select District", districts)
crop = st.selectbox("🌱 Select Crop", crops)

# Auto fill values
key = f"{district}_{crop}"
if key in avg_dict:
    vals = avg_dict[key]
    st.success("✅ Details auto-filled based on historical data!")
else:
    vals = {
        'Area_ha': 100.0,
        'N_req_kg_per_ha': 80.0,
        'P_req_kg_per_ha': 40.0,
        'K_req_kg_per_ha': 40.0,
        'Total_N_kg': 8000.0,
        'Total_P_kg': 4000.0,
        'Total_K_kg': 4000.0,
        'Temperature_C': 25.0,
        'Humidity_%': 70.0,
        'pH': 6.5,
        'Rainfall_mm': 1200.0,
        'Wind_Speed_m_s': 2.0,
        'Solar_Radiation_MJ_m2_day': 18.0
    }
    st.warning("⚠️ Using default values!")

# Show auto filled details
st.subheader("📊 Auto-Filled Details")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡️ Temperature", f"{vals['Temperature_C']}°C")
    st.metric("💧 Humidity", f"{vals['Humidity_%']}%")
    st.metric("🌧️ Rainfall", f"{vals['Rainfall_mm']} mm")
    st.metric("💨 Wind Speed", f"{vals['Wind_Speed_m_s']} m/s")

with col2:
    st.metric("🪨 Soil pH", f"{vals['pH']}")
    st.metric("☀️ Solar Radiation", f"{vals['Solar_Radiation_MJ_m2_day']}")
    st.metric("📐 Area", f"{vals['Area_ha']} ha")

with col3:
    st.metric("🧪 Nitrogen", f"{vals['N_req_kg_per_ha']} kg/ha")
    st.metric("🧪 Phosphorus", f"{vals['P_req_kg_per_ha']} kg/ha")
    st.metric("🧪 Potassium", f"{vals['K_req_kg_per_ha']} kg/ha")

st.divider()

# Encode inputs
crop_map = {"chickpea": 0, "cotton": 1,
            "maize": 2, "rice": 3}
crop_encoded = crop_map[crop]

dist_list = sorted(set(k.split('_')[0] for k in avg_dict.keys()))
dist_encoded = dist_list.index(district)

# Predict button
if st.button("🔍 Predict Future Yield", use_container_width=True):
    input_data = np.array([[
        year, dist_encoded, crop_encoded,
        vals['Area_ha'],
        vals['N_req_kg_per_ha'],
        vals['P_req_kg_per_ha'],
        vals['K_req_kg_per_ha'],
        vals['Total_N_kg'],
        vals['Total_P_kg'],
        vals['Total_K_kg'],
        vals['Temperature_C'],
        vals['Humidity_%'],
        vals['pH'],
        vals['Rainfall_mm'],
        vals['Wind_Speed_m_s'],
        vals['Solar_Radiation_MJ_m2_day']
    ]])

    prediction = model.predict(input_data)[0]

    st.subheader("🎯 Prediction Results")
    st.success(f"🌾 Predicted Yield: {prediction:.2f} kg/hectare")

    if prediction < 500:
        st.error("🔴 High Risk of Crop Loss!")
        st.write("💡 Suggestion: Consider irrigation and fertilizers!")
    elif prediction < 1500:
        st.warning("🟡 Medium Risk!")
        st.write("💡 Suggestion: Monitor weather conditions closely!")
    else:
        st.success("🟢 Low Risk — Good Yield Expected!")
        st.write("💡 Great conditions for farming this year!")
