# Maternal Health Risk Prediction & Dashboard

A dual-function Streamlit application featuring a machine learning model for maternal health risk prediction and a data dashboard for national Ante Natal Care (ANC) statistics.

![App Screenshot](pregnancy_risk_image.jpg)

---

## ## Key Features

* **🤖 Risk Prediction Tool:** An interactive interface to predict maternal health risk levels (Low, Mid, High) based on key health indicators. The tool uses a pre-trained LightGBM model.
* **📊 National ANC Dashboard:** Visualizes Ante Natal Care (ANC) data across states in India, fetching live data directly from the [data.gov.in](http://data.gov.in) API.
* **📈 Interactive Charts:** Includes dynamic bar charts and trend analyses powered by Plotly to explore national health performance and trends over time.

---

## ## Tech Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **Machine Learning:** Scikit-learn, LightGBM, Imbalanced-learn
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly
* **Model Persistence:** Joblib

---

## ## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Maternal_Healthcare_App
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit app:**
    ```bash
    streamlit run main.py
    ```