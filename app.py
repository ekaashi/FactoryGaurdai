import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load("xgb_model.pkl")

st.set_page_config(page_title="FactoryGuard AI", layout="centered")

st.title("🛠️ FactoryGuard AI")
st.subheader("Predictive Maintenance System")

st.write("Enter machine sensor values to predict failure risk.")

# Input fields
vibration = st.number_input("Vibration", min_value=0.0, value=1.5)
pressure = st.number_input("Pressure", min_value=0.0, value=50.0)
temperature = st.number_input("Temperature", min_value=0.0, value=300.0)

pwf = st.selectbox("Power Failure (PWF)", [0, 1])
osf = st.selectbox("Overstrain Failure (OSF)", [0, 1])
twf = st.selectbox("Tool Wear Failure (TWF)", [0, 1])
hdf = st.selectbox("Heat Dissipation Failure (HDF)", [0, 1])

# Create input DataFrame
input_data = pd.DataFrame({
    'UDI': [8001],                      # default / dummy
    'temperature': [temperature],
    'Process temperature K': [temperature],  # reuse if same
    'vibration': [vibration],
    'pressure': [pressure],
    'Tool wear min': [0],               # default
    'TWF': [twf],
    'HDF': [hdf],
    'PWF': [pwf],
    'OSF': [osf],
    'RNF': [0],                         # default
    'temp_roll_mean_3': [temperature], # simple approximation
    'vib_roll_std_3': [0.0]             # default
})


# Predict
if st.button("Predict Failure"):
    probability = model.predict_proba(input_data)[0][1]
    prediction = "FAILURE" if probability > 0.5 else "NO FAILURE"

    st.success(f"Prediction: {prediction}")
    st.info(f"Failure Probability: {probability:.2f}")

