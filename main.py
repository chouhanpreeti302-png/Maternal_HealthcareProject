import streamlit as st
import numpy as np
import joblib
# Import the new dashboard class from your other file
from codebase.dashboard_graphs import ANCDashboard

# --- PAGE 1: RISK PREDICTION TOOL ---
def show_prediction_page():
    st.title('Maternal Health Risk Predictor 🤰')
    st.write(
        "This tool predicts maternal health risk based on patient data. "
        "Please enter the patient's details in the sidebar to get a prediction."
    )

    # --- Load The Trained Models ---
    try:
        scaler = joblib.load('model/scaler_maternal_model.sav')
        model = joblib.load('model/finalized_maternal_model.sav')
    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'scaler_maternal_model.sav' and 'finalized_maternal_model.sav' are in the 'model' folder.")
        return

    # --- Sidebar for User Input ---
    st.sidebar.header('Enter Patient Data for Prediction')

    age = st.sidebar.slider('Age', 20, 80, 30)
    systolic_bp = st.sidebar.slider('Systolic Blood Pressure (mmHg)', 90, 180, 120)
    diastolic_bp = st.sidebar.slider('Diastolic Blood Pressure (mmHg)', 60, 120, 80)
    bs = st.sidebar.slider('Blood Sugar (mmol/L)', 6.0, 18.0, 7.8, 0.1)
    body_temp = st.sidebar.slider('Body Temperature (°F)', 96.0, 104.0, 98.6, 0.1)
    heart_rate = st.sidebar.slider('Heart Rate (bpm)', 60, 100, 70)
    
    # --- Prediction Logic ---
    if st.sidebar.button('Predict Health Risk'):
        # Create a numpy array from the inputs
        input_features = np.array([[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]])
        
        # Scale the user input
        scaled_features = scaler.transform(input_features)
        
        # Make a prediction
        prediction = model.predict(scaled_features)
        
        # Display the result
        st.subheader('Prediction Result')
        risk_levels = {0: 'Low Risk', 1: 'Mid Risk', 2: 'High Risk'}
        predicted_risk = risk_levels.get(prediction[0], 'Unknown Risk')
        
        if prediction[0] == 2: # High Risk
            st.error(f'The predicted maternal health risk is: **{predicted_risk}**')
        elif prediction[0] == 1: # Mid Risk
            st.warning(f'The predicted maternal health risk is: **{predicted_risk}**')
        else: # Low Risk
            st.success(f'The predicted maternal health risk is: **{predicted_risk}**')


# --- PAGE 2: NATIONAL HEALTH DASHBOARD ---
def show_dashboard_page():
    st.title("National Health Dashboard: Ante Natal Care (ANC) 📊")
    st.markdown("This dashboard visualizes data on Ante Natal Care across India, based on government health reports.")

    # --- Your API Key and Endpoint for the Dashboard ---
    API_KEY = "579b464db66ec23bdd000001841e8421dcf54a8b43cdb5add832a844"
    API_ENDPOINT = f"https://api.data.gov.in/resource/5ae2dbe0-849d-4e20-91ff-1e2905934d7e?api-key={API_KEY}&format=csv"

    # --- Instantiate and run the dashboard ---
    dashboard = ANCDashboard(API_ENDPOINT)

    if dashboard.anc_data is not None:
        # Display a year selection for the performance chart
        year_to_show = st.selectbox("Select Year for Performance Data", options=['2019-20', '2018-19'], index=0)
        
        dashboard.create_anc_performance_barchart(year=year_to_show)
        st.divider()
        dashboard.create_registration_trend_chart()
    else:
        st.warning("Could not load dashboard data. Please check the API connection.")


# --- MAIN APP NAVIGATION ---
st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Risk Prediction", "National Health Dashboard"))

if page == "Risk Prediction":
    show_prediction_page()
elif page == "National Health Dashboard":
    show_dashboard_page()