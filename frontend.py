import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Prediction")

st.markdown("Enter the details below to predict your insurance premium:")

age = st.number_input("Age", min_value=1, max_value=99, value=30)
weight = st.number_input("Weight (kg)", min_value=0.1, value=70.5)
height = st.number_input("Height (m)", min_value=0.5, value=1.75)
income_lpa = st.number_input("Income (LPA)", min_value=0.1, value=5.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Guwahati")
occupation = st.selectbox("Occupation", options=['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], index=6)

if st.button("Predict Premium"):
       input_data = {
              "age": age,
              "weight": weight,
              "height": height,
              "income_lpa": income_lpa,
              "smoker": smoker,
              "city": city,
              "occupation": occupation
       }
       
       try:
              response = requests.post(API_URL, json = input_data)
              if response.status_code == 200:
                     result = response.json()
                     st.success(f"Predicted Insurance Premium: **{result['predicted_premium']}**")
              else:
                     st.error(f"API Error: {response.status_code} - {response.text}")
       except requests.exceptions.ConnectionError:
              st.error("Could not connect to the API. Please ensure the backend server is running.")