import pandas as pd
import numpy as np
import joblib 
import streamlit as st
import gdown
import os

st.set_page_config(page_title="Water Pollutants Predictor", layout="centered")

# --- Google Drive direct download links ---
MODEL_URL = "https://drive.google.com/uc?id=1FwzNKS3WvLOt0a-Xe7EgnOB8B4yN2CTr"   # model file ID se banaya
COLS_URL = "https://drive.google.com/uc?id=11VMiho6ikieZ_BgQZxaruwHxqFlMykcs"   # columns file ID se banaya

MODEL_PATH = "pollution_model.pkl"
COLS_PATH = "model_columns.pkl"

# --- Function to safely download from Google Drive ---
def download_file(url, output, min_size=50000):
    if not os.path.exists(output):
        st.write(f"📥 Downloading {output} ...")
        gdown.download(url, output, quiet=False, fuzzy=True)

    # Debugging: Check file size
    if os.path.exists(output):
        file_size = os.path.getsize(output)
        st.write(f"✅ {output} downloaded (size: {file_size} bytes)")
        if file_size < min_size:
            st.error(f"❌ {output} seems corrupted (too small)!")
            st.stop()
    else:
        st.error(f"❌ {output} not found after download!")
        st.stop()

# --- Download model + columns ---
download_file(MODEL_URL, MODEL_PATH)
download_file(COLS_URL, COLS_PATH)

# --- Load model safely ---
try:
    model = joblib.load(MODEL_PATH)
    model_cols = joblib.load(COLS_PATH)
except Exception as e:
    st.error("⚠️ Model file seems corrupted or not compatible with this environment!")
    st.write(e)  # debug info
    st.stop()

# --- Streamlit App UI ---
st.title("💧 Water Pollutants Predictor")
st.write("Predict the water pollutants based on **Year** and **Station ID**")

# --- User inputs ---
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
station_id = st.text_input("Enter Station ID", value='1')

# --- Pollutant safe limits ---
safe_limits = {
    'O2': 4.0,      # mg/L minimum dissolved oxygen
    'NO3': 10.0,    # mg/L
    'NO2': 1.0,     # mg/L
    'SO4': 200.0,   # mg/L
    'PO4': 0.1,     # mg/L
    'CL': 250.0     # mg/L
}

# --- Prediction button ---
if st.button('Predict'):
    if not station_id:
        st.warning('⚠️ Please enter the station ID')
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

        st.subheader(f"Predicted pollutant levels for station **{station_id}** in **{year_input}**:")
        unsafe_flags = []  

        for p, val in zip(pollutants, predicted_pollutants):
            st.write(f'- {p}: {val:.2f} mg/L')
            if p == 'O2':
                if val < safe_limits[p]:
                    unsafe_flags.append(p)
            else:
                if val > safe_limits[p]:
                    unsafe_flags.append(p)

        # Show water safety status
        st.subheader("💡 Water Quality Status:")
        if not unsafe_flags:
            st.success("✅ Water is likely SAFE for basic use.")
        else:
            st.error("❌ Water is likely UNSAFE due to: " + ", ".join(unsafe_flags))

            # Explain unsafe pollutants
            st.subheader("⚠️ Why Unsafe and Ideal Levels:")
            for p in unsafe_flags:
                actual_value = predicted_pollutants[pollutants.index(p)]
                if p == 'O2':
                    st.write(f"🔴 **{p}** is too LOW: {actual_value:.2f} mg/L (should be ≥ {safe_limits[p]} mg/L).")
                else:
                    st.write(f"🔴 **{p}** is too HIGH: {actual_value:.2f} mg/L (should be ≤ {safe_limits[p]} mg/L).")

            st.info("💡 To make the water safe, pollutants must be within safe limits.")



