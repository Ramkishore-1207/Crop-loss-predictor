import streamlit as st
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder

model = joblib.load('crop_yield_model_small.pkl')

st.title("🌾 Farmer Crop Loss Predictor")
st.subheader("Tamil Nadu Crop Yield Prediction App")

# Input fields
year = st.number_input("Year", 2000, 2030, 2024)
dist_name = st.selectbox("District", 
    ['Ariyalur', 'Chennai', 'Coimbatore', 'Cuddalore',
     'Dharmapuri', 'Dindigul', 'Erode', 'Kanchipuram',
     'Kanyakumari', 'Karur', 'Madurai', 'Nagapattinam',
     'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai',
     'Ramanathapuram', 'Salem', 'Sivaganga', 'Thanjavur',
     'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
     'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Vellore',
     'Viluppuram', 'Virudhunagar'])

crop = st.selectbox("Select Crop",
    ['chickpea', 'cotton', 'maize', 'rice'])

area = st.number_input("Area (hectares)", 1.0, 1000.0, 10.0)
n_req = st.slider("Nitrogen (kg/ha)", 0, 200, 80)
p_req = st.slider("Phosphorus (kg/ha)", 0, 200, 40)
k_req = st.slider("Potassium (kg/ha)", 0, 200, 40)
total_n = st.slider("Total Nitrogen (kg)", 0, 10000, 800)
total_p = st.slider("Total Phosphorus (kg)", 0, 10000, 400)
total_k = st.slider("Total Potassium (kg)", 0, 10000, 400)
temp = st.slider("Temperature (°C)", 10, 50, 25)
humidity = st.slider("Humidity (%)", 0, 100, 70)
ph = st.slider("Soil pH", 4.0, 9.0, 6.5)
rainfall = st.slider("Rainfall (mm)", 0, 3000, 1200)
wind = st.slider("Wind Speed (m/s)", 0.0, 20.0, 5.0)
solar = st.slider("Solar Radiation", 0.0, 30.0, 15.0)

# Encode
crop_map = {"chickpea": 0, "cotton": 1, 
            "maize": 2, "rice": 3}
crop_encoded = crop_map[crop]

dist_map = {d: i for i, d in enumerate([
    'Ariyalur', 'Chennai', 'Coimbatore', 'Cuddalore',
    'Dharmapuri', 'Dindigul', 'Erode', 'Kanchipuram',
    'Kanyakumari', 'Karur', 'Madurai', 'Nagapattinam',
    'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai',
    'Ramanathapuram', 'Salem', 'Sivaganga', 'Thanjavur',
    'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
    'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Vellore',
    'Viluppuram', 'Virudhunagar'])}
dist_encoded = dist_map[dist_name]

if st.button("🔍 Predict Yield"):
    input_data = np.array([[year, dist_encoded, 
                            crop_encoded, area,
                            n_req, p_req, k_req,
                            total_n, total_p, total_k,
                            temp, humidity, ph,
                            rainfall, wind, solar]])

    prediction = model.predict(input_data)[0]
    st.success(f"🌾 Predicted Yield: {prediction:.2f} kg/hectare")

    if prediction < 500:
        st.error("🔴 High Risk of Crop Loss!")
    elif prediction < 1500:
        st.warning("🟡 Medium Risk!")
    else:
        st.success("🟢 Low Risk — Good Yield Expected!")
