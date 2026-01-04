# 🏋️ Fitness Calorie Tracker & Weight Prediction System

A **Streamlit-based fitness tracking web application** that allows users to track daily calorie intake, calories burned, weight progress, and plan weight gain/loss goals with clean visualization and simple machine-learning integration.

---

## 📌 Project Summary

This project combines **fitness tracking + data analytics + basic ML** into one interactive web app.  
Users can:
- Register & login
- Track daily food intake (multiple foods)
- Estimate calories burned via walking
- Maintain daily fitness logs
- Visualize weekly progress
- Plan weight gain/loss scientifically

---

## 👨‍💻 Developers

- **22-NTU-CS-1227** – Umer Moazzam  
- **22-NTU-CS-1229** – Wasif Ali  
- **22-NTU-CS-1191** – Bilal Afzal  

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **CSV-based storage**
- **Machine Learning (weight prediction model)**

---

## 📂 Project Structure

Fitness-Calorie-Tracker/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│ ├── user.csv
│ ├── daily_log.csv
│ └── food_calories.csv
│
└── model/
└── weight_model.py

---

## 🔐 Authentication System

### Features
- Signup
- Login
- Logout
- Session-based authentication

### User Data File
**`data/user.csv`**

| Column   | Description |
|--------|------------|
| username | User ID |
| password | Plain-text password (academic use only) |

> ⚠️ Password hashing not implemented (future improvement).

---

## 🧾 Daily Fitness Logging

All daily data is stored in:

### **`data/daily_log.csv`**

| Column | Description |
|------|------------|
| date | Log date |
| weight | Body weight (kg) |
| intake | Calories consumed |
| burned | Calories burned |
| steps | Steps count |
| distance | Distance walked (km) |
| water_intake | Water intake (liters) |
| sleep_hours | Sleep duration |
| notes | Personal notes |

✔ If today’s entry already exists, values are **updated**, not duplicated.

---

## 🏠 Home Dashboard

Displays **live data (not static)**:
- Calories burned today
- Calories intake today
- Current weight
- Daily target comparison

Uses Streamlit **metrics** for a clean and professional UI.

---

## 🍎 Calorie Intake Analyzer

### Features
- Accepts **multiple foods** (comma-separated)
- Optional quantities (grams)
- Auto calorie calculation
- Target calorie guidance

### Example Input
Foods: Rice, Chicken
Quantities: 150, 200


### Formula Used
Calories = (Calories per 100g / 100) × Quantity


Data source:
data/food_calories.csv

---

## 🏃 Calories Burned Estimator

Estimates calories burned through walking.

### Formula
Calories Burned = Weight (kg) × Distance (km) × 0.9

yaml
Copy code

### Extra Feature
- Calculates **required distance** to burn target calories.

---

## ⚖️ Weight Gain / Loss Planner

Helps users plan weight change scientifically.

### Scientific Rule Used
1 kg body fat ≈ 7700 kcal

yaml
Copy code

### Output
- Required daily calorie surplus (weight gain)
- Required daily calorie deficit (weight loss)
- Recommended foods
- Fitness tips

---

## 📊 Progress & Visualization

### Charts
- Daily intake vs burned (pie chart)
- Last 7 days comparison (bar chart)

### Purpose
- Track consistency
- Analyze trends
- Improve decision making

---

## 🤖 Machine Learning Integration

- File: `model/weight_model.py`
- Used for predicting weight trends
- Demonstrates **ML + Streamlit integration**
- Academic-level implementation

---

## 🎨 UI & UX Highlights

- Wide layout
- Sidebar navigation
- Minimal colors (eye-friendly)
- Emoji-based icons
- Clean metric cards
- No visual clutter

---

## ▶️ How to Run the Project

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
Step 2: Run the app
bash
Copy code
streamlit run app.py
📈 Future Improvements
Password hashing & security

Database (SQLite / Firebase)

Mobile responsiveness

Advanced ML predictions

Personalized reports

Export data (PDF/CSV)

📜 License
This project is created for academic and learning purposes only.

✅ Conclusion
This project demonstrates:

Real-world fitness problem solving

Clean Streamlit UI

CSV-based data handling

Analytics & visualization

ML integration in web apps

💪 Track smart. Train better. Live healthy.
















