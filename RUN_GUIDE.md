# How to Run AquaSentry 🌊

This system consists of two parts: a **Django Backend** (for API & Logic) and a **React Frontend** (for the UI). Validating the "Patent-Ready" status requires running both.

You will need **3 separate terminal windows**.

## Terminal 1: Backend Server 🧠
This runs the API and the Image Processing Engine.

```powershell
# 1. Go to the project folder
cd "c:\Users\hunte\Aquasentry- Team h@ckaholics\backend"

# 2. Install dependencies (if not already done)
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# 3. Start the server
.\venv\Scripts\python.exe manage.py runserver
```
*Keep this window open.*

---

## Terminal 2: Sensor Simulation 📡
This simulates the IoT devices sending real-time data to your dashboard.

```powershell
# 1. Go to the project folder
cd "c:\Users\hunte\Aquasentry- Team h@ckaholics\backend"

# 2. Start the simulation
.\venv\Scripts\python.exe manage.py start_simulation
```
*Keep this window open. You should see "Data packet sent..." messages.*

---

## Terminal 3: Frontend Dashboard 💻
This runs the visual user interface.

```powershell
# 1. Go to the frontend folder (IMPORTANT: Use this specific folder)
cd "c:\Users\hunte\Aquasentry- Team h@ckaholics\aquasentry-frontend"

# 2. Start the website
npm run dev
```

**Once running, open your browser at:** [http://localhost:5173](http://localhost:5173)

---

### Troubleshooting
- **Error: "npm error enoent"**: This means you are in the wrong folder. Make sure you typed `cd aquasentry-frontend` before running `npm run dev`.
- **Backend not connecting**: Ensure Terminal 1 is running and shows `Quit the server with CTRL-BREAK`.

## 🛰️ Satellite Simulation Mode (Patent-Ready Demo)
To ensure your presentation always works perfectly without expensive API keys:
- The system checks for `SENTINEL_CLIENT_ID` in the backend.
- **If no key is found**, it automatically generates a **Synthetic Satellite Image**.
- This image contains simulated **Algae (Green)** and **Turbidity (Brown)** which the OpenCV engine then detects.
- This proves the *logic* works without needing a live paid subscription.

## 📧 Email Alert System
- The system uses **Gmail SMTP** to send alerts for Health Reports.
- **Configuration**: To make this work, update `backend/aquasentry_backend/settings.py` with your Gmail address.
- **Demo Mode**: If configured correctly, submitting a report (Severity 1+) will instantly send an email to your inbox.
