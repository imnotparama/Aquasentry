AquaSentry 💧 - AI Water Quality Predictor
Team: H@ckahol!cs

Team Number: SAV178

Team Members: C.Monish Nandha Balan , Parameshwaran S ,Gururajan Ganesh Babu, Dharshini B, Anuja V S , Abishek Raj V S

College: SRMIST RAMAPURAM

Our Entry for the IBM Z Datathon 2025: A Predictive Community Health Shield for Water-Borne Disease Prevention.

🚀 The Mission
AquaSentry is an intelligent early-warning system that leverages AI and cloud technology to predict water safety in real-time. Our mission is to create a proactive, accessible tool that can flag contamination risks before they become public health emergencies, enabling authorities and individuals to take preventive action.

✨ Key Features
Real-Time Prediction: Instantly predict if a water sample is safe to drink based on key chemical and physical parameters.

Partial Data Handling: Don't have all the data? Our tool intelligently handles missing values by substituting them with dataset averages, allowing for predictions even with incomplete information.

Interactive UI: A clean, user-friendly interface built with Streamlit, featuring sliders and checkboxes for easy data entry.

In-Depth Analysis: An integrated dashboard to explore the model's performance, understand which factors are most important for prediction, and view correlations in the training data.

Clear & Actionable Results: Provides not just a "safe" or "unsafe" verdict, but also a confidence score and potential reasons for a negative result.

🛠️ Technology Stack
Data Science: Python, Pandas, Scikit-learn, NumPy

Frontend: Streamlit for rapid, interactive dashboarding

Data Visualization: Matplotlib, Seaborn

Deployment Platform: IBM Z (LinuxONE)

Data Source: Kaggle Water Quality Dataset

Why IBM Z and LinuxONE?
AquaSentry is built upon the robust and secure foundation of IBM Z and LinuxONE to handle the mission-critical task of public health monitoring. We chose this platform for its unparalleled capabilities in security, scalability, and reliability.

🛡️ Security: Handling sensitive public health data demands the highest level of security. By leveraging LinuxONE's pervasive encryption, we ensure that all data—from sensor readings to health reports—is encrypted at rest and in transit, providing end-to-end security for our application.

** scalability:** To effectively monitor a nation's water supply, AquaSentry processes millions of data points in real-time. The immense I/O capacity and processing power of the IBM Z platform allow us to scale our operations seamlessly, handling massive data streams without compromising performance.

⏱️ Reliability: Water quality monitoring is a 24/7 responsibility where downtime is not an option. Hosted on IBM Z, AquaSentry benefits from the platform's legendary 99.999% uptime, guaranteeing that our predictive alerts are always operational and available to safeguard communities.

⚙️ Setup and Installation
To run this project locally, follow these steps:

Clone the repository:

git clone [https://github.com/mnnitparama/AquaSentry.git](https://github.com/mnnitparama/AquaSentry.git)
cd AquaSentry



Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`



Install the dependencies:
Make sure you have a requirements.txt file with the necessary libraries.

# requirements.txt
streamlit==1.10.0
pandas
numpy
scikit-learn
matplotlib
seaborn



Then, run the installation command:

pip install -r requirements.txt



Run the Streamlit app:

streamlit run app.py



Your browser should open with the AquaSentry application running!

📈 Future Roadmap
Integrate Real-Time IoT Sensor Data: Connect directly to live sensors in rivers, reservoirs, and municipal water systems.

Incorporate Satellite and Weather Data: Use satellite imagery (for algal blooms) and rainfall data (for runoff risk) to enhance prediction accuracy.

Develop a Mobile Alert System: Send instant alerts to municipal bodies and the public via a dedicated mobile app when a risk is detected.
