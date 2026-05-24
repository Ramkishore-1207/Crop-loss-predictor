import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load('crop_yield_model_small.pkl')

# Title
st.title("🌾 Farmer Crop Loss Predictor")
st.subheader("Tamil Nadu Crop Yield Prediction App")
st.write("Enter the details below to predict crop yield!")

# Input fields
crop = st.selectbox("Select Crop",
    ['chickpea', 'cotton', 'maize', 'rice'])

area = st.number_input("Area (hectares)",
    min_value=1.0, max_value=1000.0, value=10.0)

temp = st.slider("Temperature (°C)", 10, 50, 25)
humidity = st.slider("Humidity (%)", 0, 100, 70)
rainfall = st.slider("Rainfall (mm)", 0, 3000, 1200)
ph = st.slider("Soil pH", 4.0, 9.0, 6.5)
n_req = st.slider("Nitrogen Required (kg/ha)", 0, 200, 80)
p_req = st.slider("Phosphorus Required (kg/ha)", 0, 200, 40)
k_req = st.slider("Potassium Required (kg/ha)", 0, 200, 40)
wind = st.slider("Wind Speed (m/s)", 0.0, 20.0, 5.0)
solar = st.slider("Solar Radiation", 0.0, 30.0, 15.0)

# Encode crop
crop_map = {"chickpea": 0, "cotton": 1,
            "maize": 2, "rice": 3}
crop_encoded = crop_map[crop]

# Drought index
drought_index = rainfall / temp if temp != 0 else 0

# Predict button
if st.button("🔍 Predict Yield"):
    input_data = np.array([[crop_encoded, area,
                            n_req, p_req, k_req,
                            temp, humidity, ph,
                            rainfall, wind,
                            solar, drought_index]])

    prediction = model.predict(input_data)[0]

    st.success(f"🌾 Predicted Yield: {prediction:.2f} kg/hectare")

    if prediction < 500:
        st.error("🔴 High Risk of Crop Loss!")
    elif prediction < 1500:
        st.warning("🟡 Medium Risk!")
    else:
        st.success("🟢 Low Risk — Good Yield Expected!") 
