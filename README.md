# water-quality-prediction_AICTE-PROJECT-1
A machine learning project to predict water quality based on chemical properties like pH, hardness, solids, and more. Useful for environmental monitoring and public health

# Water Quality Prediction App
A machine learning-powered web application built with Streamlit that predicts key water pollutants based on the selected year and station ID. It helps determine whether the water quality is safe or polluted based on predicted chemical concentrations.

# Features
Predicts pollutant levels like:

O₂ (Dissolved Oxygen)

NO₃ (Nitrate)

NO₂ (Nitrite)

SO₄ (Sulfate)

PO₄ (Phosphate)

CL (Chloride)

Interactive Streamlit interface
User inputs: Year and Station ID
Displays results in a clean and readable format
Includes water safety classification (Safe / Unsafe)
Model powered by a trained ML algorithm using real data

 # How It Works
User selects or enters:

Year

Station ID

The app passes this input to a trained ML model.
The model predicts levels of key water pollutants.
A rule-based system checks whether these levels are within safe limits.
The result is shown on the screen with safety indicators.

 # Safe Water Criteria (Example Rules)
Pollutant	Safe Range (Example)
O₂	> 5 mg/L
NO₃	< 10 mg/L
NO₂	< 1 mg/L
SO₄	< 250 mg/L
PO₄	< 0.5 mg/L
CL	< 250 mg/L
You can modify these ranges in the app logic to reflect your region's standards.

 # Model Training (Brief)
Algorithm used: e.g., Random Forest Regressor , MultiOutput Regression
Trained on historical data of water quality from various monitoring stations
Features: Year, Station ID (One-hot encoded), others (if available)

# Tool used
pandas
numpy
joblib
scikit-learn
streamlit
Matplotlib
Seaborn
Jupyter Notebook
 # Model Performance
The model was evaluated using:
R² Score
Mean Squared Error (MSE)
# Model link:
Model link for columns:https://drive.google.com/file/d/1FwzNKS3WvLOt0a-Xe7EgnOB8B4yN2CTr/view?usp=drive_link

Model link for pollutin:https://drive.google.com/file/d/11VMiho6ikieZ_BgQZxaruwHxqFlMykcs/view?usp=drive_link

 # Inspiration
This project aims to raise awareness about water pollution and help make data-driven decisions for clean water initiatives.

# Contact
For questions or collaborations, reach out to:
Name:Aman kumar
Email:aman 1782003@gmail.com
GitHub: https://github.com/Aman-kumar-178.

