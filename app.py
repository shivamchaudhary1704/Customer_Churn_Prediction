import streamlit as st
import pandas as pd
import pickle

# Load model & mapping
model = pickle.load(open("model_new.pkl", "rb"))
main_map = pickle.load(open("mapping_new.pkl", "rb"))

# Columns used in training
expected_columns = [
    # mapped cols
   'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 
  'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 
  'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
    
]

st.set_page_config(page_title="Telco Churn Prediction", layout="wide")
st.title("📊 Telco Customer Churn Prediction")

# --- UI ---
col1, col2, col3 = st.columns(3)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col2:
    senior_citizen = st.selectbox("Senior Citizen", [0, 1])
with col3:
    partner = st.selectbox("Partner", ["Yes", "No"])

col1, col2, col3 = st.columns(3)
with col1:
    dependents = st.selectbox("Dependents", ["Yes", "No"])
with col2:
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
with col3:
    multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

col1, col2, col3 = st.columns(3)
with col1:
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
with col2:
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
with col3:
    online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

col1, col2, col3 = st.columns(3)
with col1:
    device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
with col2:
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
with col3:
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])

col1, col2, col3 = st.columns(3)
with col1:
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
with col2:
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
with col3:
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])

col1, col2, col3 = st.columns(3)
with col1:
    payment_method = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )
with col2:
    tenure = st.number_input("Tenure (Months)", min_value=0, max_value=72, value=12)
with col3:
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=70.0)

total_charges = st.number_input("Total Charges", min_value=0.0, value=1000.0)


# --- Prediction ---
if st.button("Predict"):
    # Create dataframe with raw categorical columns where needed
    input_data = {
        'gender': main_map[gender],
        'SeniorCitizen': senior_citizen,
        'Partner': main_map[partner],
        'Dependents': main_map[dependents],
        'PhoneService': main_map[phone_service],
        'MultipleLines': main_map[multiple_lines],
        
        'OnlineSecurity': main_map[online_security],
        'OnlineBackup': main_map[online_backup],
        'DeviceProtection': main_map[device_protection],
        'TechSupport': main_map[tech_support],
        'StreamingTV': main_map[streaming_tv],
        'StreamingMovies': main_map[streaming_movies],
        'PaperlessBilling': main_map[paperless_billing],
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,
        ####
        'Contract': main_map[contract],                  # keep raw for get_dummies
        'InternetService': main_map[internet_service],   # keep raw for get_dummies
        'PaymentMethod': main_map[payment_method],       
        
        
        
    }

    df = pd.DataFrame([input_data])

  
    # Add missing dummy columns from training
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns to match training data
    df = df[expected_columns]

    # Predict
    pred = model.predict(df)[0]
    if pred == 1:
        st.error("⚠ This customer is likely to churn.")
    else:
        st.success("✅ This customer is likely to stay.")