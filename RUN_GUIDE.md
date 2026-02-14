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
