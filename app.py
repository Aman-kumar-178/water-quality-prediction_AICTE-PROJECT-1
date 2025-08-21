# Import all the necessary libraries
import pandas as pd
import numpy as np
import joblib 
import streamlit as st
import gdown
import os

# ------------------------------
# Google Drive से मॉडल और columns download करो
# ------------------------------
model_url = "https://drive.google.com/file/d/1FwzNKS3WvLOt0a-Xe7EgnOB8B4yN2CTr/view?usp=drive_link"   # <-- अपना pollution_model.pkl ID डालो
cols_url = "https://drive.google.com/file/d/11VMiho6ikieZ_BgQZxaruwHxqFlMykcs/view?usp=drive_link"         # <-- अपना model_columns.pkl ID डालो

model_path = "pollution_model.pkl"
cols_path = "model_columns.pkl"

if not os.path.exists(model_path):
    st.write("📥 Downloading pollution_model.pkl from Google Drive...")
    gdown.download(model_url, model_path, quiet=False)

if not os.path.exists(cols_path):
    st.write("📥 Downloading model_columns.pkl from Google Drive...")
    gdown.download(cols_url, cols_path, quiet=False)

# अब मॉडल लोड करो
model = joblib.load(model_path)
model_cols = joblib.load(cols_path)

# ------------------------------
# Streamlit App UI
# ------------------------------
st.title("💧 Water Pollutants Predictor")
st.write("Predict the water pollutants based on **Year** and **Station ID**")

# User inputs
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
station_id = st.text_input("Enter Station ID", value='1')

# Pollutant safe limits (as per standards)
safe_limits = {
    'O2': 4.0,      # mg/L minimum dissolved oxygen
    'NO3': 10.0,    # mg/L
    'NO2': 1.0,     # mg/L
    'SO4': 200.0,   # mg/L
    'PO4': 0.1,     # mg/L
    'CL': 250.0     # mg/L
}

# ------------------------------
# Prediction on button click
# ------------------------------
if st.button('🔮 Predict'):
    if not station_id:
        st.warning('⚠️ Please enter the Station ID')
    else:
        # Prepare input
        input_df = pd.DataFrame({'year': [year_input], 'id':[station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        # Align with model columns
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        # Predict pollutants
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

        st.subheader(f"📊 Predicted pollutant levels for Station **{station_id}** in **{year_input}**:")
        unsafe_flags = []  

        for p, val in zip(pollutants, predicted_pollutants):
            st.write(f'🔹 {p}: {val:.2f} mg/L')
            if p == 'O2':
                if val < safe_limits[p]:
                    unsafe_flags.append(p)
            else:
                if val > safe_limits[p]:
                    unsafe_flags.append(p)

        # Show water safety status
        st.subheader("🚰 Water Quality Status:")
        if not unsafe_flags:
            st.success("✅ Water is likely SAFE for basic use.")
        else:
            st.error("❌ Water is likely UNSAFE due to: " + ", ".join(unsafe_flags))

            # Explain why it's unsafe and what should be the ideal levels
            st.subheader("⚠️ Why Water is Unsafe and Ideal Levels:")
            for p in unsafe_flags:
                actual_value = predicted_pollutants[pollutants.index(p)]
                if p == 'O2':
                    st.write(f"🔴 **{p}** is too LOW: {actual_value:.2f} mg/L (should be at least {safe_limits[p]} mg/L).")
                else:
                    st.write(f"🔴 **{p}** is too HIGH: {actual_value:.2f} mg/L (should not exceed {safe_limits[p]} mg/L).")

            st.info("💡 To make the water safe, pollutants need to be within their safe limits.")








