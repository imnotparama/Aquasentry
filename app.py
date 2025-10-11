# app.py
# Final Code for the IBM Z Datathon 2025 - AquaSentry Project (with Partial Data Handling)

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import class_weight
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AquaSentry Water Quality Predictor",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Caching for Performance ---
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna()
    return df

@st.cache_resource
def train_model(df):
    X = df.drop('Potability', axis=1)
    y = df['Potability']
    
    # Calculate feature means for imputation
    feature_means = X.mean()

    classes = np.array([0, 1])
    weights = class_weight.compute_class_weight(class_weight='balanced', classes=classes, y=y)
    class_weights_dict = {0: weights[0], 1: weights[1]}
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weights_dict)
    model.fit(X_train, y_train)

    return model, X_test, y_test, feature_means

# --- 3. Load Data and Train Model ---
df = load_data("water_quality.csv")
model, X_test, y_test, feature_means = train_model(df)

# --- 4. Sidebar for User Inputs (UPGRADED for partial data) ---
st.sidebar.header("🎛️ Water Sample Parameters")
st.sidebar.markdown("Uncheck any parameter you don't have data for.")

def get_user_inputs():
    """Gets user inputs from the sidebar, allowing for missing values."""
    inputs = {}
    known_inputs = []

    # Define parameters with their properties for cleaner code
    params = {
        'ph': ("pH Level", 0.0, 14.0, 7.0, 0.1),
        'Hardness': ("Hardness (mg/L)", 47.0, 324.0, 195.0, 1.0),
        'Solids': ("Solids (TDS in ppm)", 320.0, 61227.0, 20927.0, 50.0),
        'Chloramines': ("Chloramines (ppm)", 0.35, 13.13, 7.13, 0.1),
        'Sulfate': ("Sulfate (mg/L)", 129.0, 481.0, 333.0, 1.0),
        'Conductivity': ("Conductivity (μS/cm)", 181.0, 754.0, 426.0, 1.0),
        'Organic_carbon': ("Organic Carbon (ppm)", 2.2, 28.3, 14.2, 0.1),
        'Trihalomethanes': ("Trihalomethanes (μg/L)", 0.74, 124.0, 66.4, 1.0),
        'Turbidity': ("Turbidity (NTU)", 1.45, 6.74, 3.96, 0.01)
    }

    for key, (label, min_val, max_val, default_val, step) in params.items():
        if st.sidebar.checkbox(f"Include {label}", value=True, key=f"check_{key}"):
            inputs[key] = st.sidebar.slider(label, min_val, max_val, default_val, step, key=f"slider_{key}")
            known_inputs.append(key)
        else:
            inputs[key] = np.nan # Use NaN for unknown values

    return pd.DataFrame([inputs]), known_inputs

user_inputs_df, known_inputs = get_user_inputs()

# --- 5. Main Page Layout ---
st.title("💧 AquaSentry - AI Water Quality Predictor")
st.markdown("Welcome to **AquaSentry**, your real-time solution for ensuring water safety.")
main_tab, analysis_tab, vision_tab = st.tabs(["Prediction Tool", "Deeper Analysis", "Project Vision"])

with main_tab:
    st.header("🔬 Real-Time Prediction")
    st.markdown("Use the checkboxes in the sidebar to include only the data you have, then click 'Predict'.")

    st.markdown("#### Your Input Sample (unknowns will be filled with average values):")
    # Impute missing values before displaying and predicting
    imputed_inputs_df = user_inputs_df.fillna(feature_means)
    st.dataframe(imputed_inputs_df, use_container_width=True)
    
    predict_button = st.button("Predict Water Potability", type="primary")

    if predict_button:
        with st.spinner("Analyzing water sample..."):
            prediction = model.predict(imputed_inputs_df)[0]
            prediction_proba = model.predict_proba(imputed_inputs_df)

            if prediction == 1:
                st.success(f"**✅ SAFE TO DRINK** (Confidence: {prediction_proba[0][1]:.2%})")
                st.balloons()
            else:
                st.error(f"**❌ UNSAFE TO DRINK** (Confidence: {prediction_proba[0][0]:.2%})")
                reasons = []
                # Only check reasons for data the user actually provided
                if 'ph' in known_inputs and not (6.5 <= imputed_inputs_df['ph'].iloc[0] <= 8.5):
                    reasons.append(f"the user-provided **pH level ({imputed_inputs_df['ph'].iloc[0]:.2f})** is outside the safe range")
                if 'Solids' in known_inputs and imputed_inputs_df['Solids'].iloc[0] > 1000:
                    reasons.append(f"the user-provided **Total Dissolved Solids ({imputed_inputs_df['Solids'].iloc[0]:,.0f} ppm)** are too high")
                if 'Sulfate' in known_inputs and imputed_inputs_df['Sulfate'].iloc[0] > 250:
                    reasons.append(f"the user-provided **Sulfate level ({imputed_inputs_df['Sulfate'].iloc[0]:.2f} mg/L)** is too high")
                if 'Turbidity' in known_inputs and imputed_inputs_df['Turbidity'].iloc[0] > 5:
                    reasons.append(f"the user-provided **Turbidity ({imputed_inputs_df['Turbidity'].iloc[0]:.2f} NTU)** is too high")
                
                if reasons:
                    st.warning(f"**Primary Reason:** The water is likely unsafe because {reasons[0]}.")
                else:
                    st.warning("**Reason:** Based on the provided data, a combination of factors indicates the water is unsafe.")

with analysis_tab:
    # (This section remains unchanged)
    st.header("📊 Understanding the Model")
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Feature Importance", "Model Performance", "Data Overview"])
    
    with sub_tab1:
        st.markdown("#### Which factors are most important for prediction?")
        importance = pd.Series(model.feature_importances_, index=df.drop('Potability', axis=1).columns)
        importance_df = importance.reset_index().rename(columns={'index': 'Feature', 0: 'Importance'}).sort_values(by='Importance', ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.set_style("whitegrid")
        bar_plot = sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis', ax=ax, orient='h')
        for i in bar_plot.patches:
            ax.text(i.get_width() + .005, i.get_y() + .5, str(round(i.get_width(), 4)), fontsize=10, color='gray')
        ax.set_title("Feature Importance in Water Potability", fontsize=16)
        st.pyplot(fig)

    with sub_tab2:
        st.markdown("#### How well does our AI model perform?")
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        st.metric(label="Model Accuracy on Test Data", value=f"{accuracy:.2%}")
        st.text("Classification Report:")
        report = classification_report(y_test, y_pred, output_dict=True)
        st.dataframe(pd.DataFrame(report).transpose())

    with sub_tab3:
        st.markdown("#### Quick Look at the Training Data")
        st.dataframe(df.describe())
        st.markdown("##### Correlation Matrix")
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
        st.pyplot(fig)

with vision_tab:
    # (This section remains unchanged)
    st.header("🎯 Project Vision & Story")
    st.markdown("""
    ### The Problem
    Water contamination is a silent crisis, often going undetected until it leads to widespread illness. Traditional water testing methods are slow, expensive, and reactive. With changing environmental conditions, a proactive, real-time solution is urgently needed to protect public health.

    ### Our Solution: AquaSentry
    **AquaSentry** is an intelligent early-warning system that leverages AI, open-source data, and cloud technology to predict water safety in real-time. By analyzing key chemical and physical parameters, our platform can flag contamination risks before they become health emergencies, enabling authorities to take preventive action.

    ### Technology Stack
    - **Data Science:** Python, Pandas, Scikit-learn
    - **Frontend:** Streamlit for rapid, interactive dashboarding
    - **Data Sources:** Kaggle Water Quality Datasets, CPCB (Central Pollution Control Board) open data.
    - **Deployment Target:** **IBM Cloud** using containers, running on **IBM LinuxONE** for maximum security, scalability, and reliability.

    ### Why IBM Z and LinuxONE?
    - **Security:** Water quality and public health data are sensitive. LinuxONE's 'pervasive encryption' ensures this data is secure at all times.
    - **Scalability:** To monitor an entire nation's water supply, we need to process millions of data points per second. The I/O capacity and processing power of the IBM Z platform are built for this massive scale.
    - **Reliability:** Water monitoring is a mission-critical 24/7 task. The legendary 99.999% uptime of IBM mainframes guarantees our alert system never fails.
    
    ### Future Roadmap
    1.  **Integrate Real-Time IoT Sensor Data:** Connect directly to live sensors in rivers and reservoirs.
    2.  **Incorporate Satellite and Weather Data:** Use satellite imagery (for algal blooms) and rainfall data (for runoff risk) to enhance prediction accuracy.
    3.  **Develop a Mobile Alert System:** Send instant alerts to municipal bodies and the public via a dedicated mobile app.
    """)