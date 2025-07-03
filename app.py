# Import all the necessary libraries
import pandas as pd
import numpy as np
import joblib 
import streamlit as st

# Load the model and structure
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# Streamlit App UI
st.title("Water Pollutants Predictor")
st.write("Predict the water pollutants based on Year and Station ID")

# User inputs
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
station_id = st.text_input("Enter Station ID", value='1')

# Pollutant safe limits (you can update these values as needed)
safe_limits = {
    'O2': 4.0,      # mg/L minimum dissolved oxygen
    'NO3': 10.0,    # mg/L
    'NO2': 1.0,     # mg/L
    'SO4': 200.0,   # mg/L
    'PO4': 0.1,     # mg/L
    'CL': 250.0     # mg/L
}

# Prediction on button click
if st.button('Predict'):
    if not station_id:
        st.warning('Please enter the station ID')
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

        st.subheader(f"Predicted pollutant levels for the station '{station_id}' in {year_input}:")
        unsafe_flags = []  

        for p, val in zip(pollutants, predicted_pollutants):
            st.write(f'{p}: {val:.2f}')
            if p == 'O2':
                if val < safe_limits[p]:
                    unsafe_flags.append(p)
            else:
                if val > safe_limits[p]:
                    unsafe_flags.append(p)

        # Show water safety status
        st.subheader("Water Quality Status:")
        if not unsafe_flags:
            st.success("✅ Water is likely SAFE for basic use.")
        else:
            st.error("❌ Water is likely UNSAFE due to: " + ", ".join(unsafe_flags))

         #Explain why it's unsafe and what should be the ideal levels
            st.subheader("Why Water is Unsafe and What Should be Ideal Levels:")
            for p in unsafe_flags:
                actual_value = predicted_pollutants[pollutants.index(p)]
                if p == 'O2':
                    st.write(f"🔴 **{p}** is too LOW: {actual_value:.2f} mg/L (should be at least {safe_limits[p]} mg/L for safe water).")
                else:
                    st.write(f"🔴 **{p}** is too HIGH: {actual_value:.2f} mg/L (should not exceed {safe_limits[p]} mg/L).")

            st.info("💡 To make the water safe, pollutants need to be within their safe limits as shown above.")



