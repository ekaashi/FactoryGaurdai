# 🏭 FactoryGuard AI

### 🚀 Predictive Maintenance System using Machine Learning

FactoryGuard AI is a smart predictive maintenance system that analyzes machine sensor data and predicts the probability of machine failure. It helps industries reduce downtime, prevent unexpected breakdowns, and improve operational efficiency.

---

## 📌 Overview

In traditional systems, maintenance is performed **after failure occurs**, which leads to high costs and production loss.

FactoryGuard AI shifts this to a **proactive approach** by:

* Predicting machine failures in advance
* Monitoring key sensor parameters
* Providing actionable insights

---

## ⚙️ Features

* 📊 Real-time failure prediction
* 🎯 Failure probability score (0–100%)
* 🟢🟡🔴 Risk level classification (Low / Medium / High)
* 📈 Interactive dashboard (charts + gauge)
* 🎛️ Easy-to-use UI with sliders & toggles
* ⚡ Fast predictions using trained ML model

---

## 🧠 Machine Learning Model

* **Algorithm:** XGBoost Classifier
* **Task:** Binary Classification (Failure / No Failure)
* **Output:** Probability of machine failure

---

## 📥 Input Parameters

### 🔧 Sensor Data

* Temperature
* Pressure
* Vibration

### 🚨 Failure Indicators

* Power Failure (PWF)
* Overstrain Failure (OSF)
* Tool Wear Failure (TWF)
* Heat Dissipation Failure (HDF)

---

## 🛠️ Tech Stack

| Layer         | Technology      |
| ------------- | --------------- |
| Frontend      | Streamlit       |
| Backend       | Python          |
| ML Model      | XGBoost         |
| Data          | Pandas, NumPy   |
| Visualization | Plotly          |
| Deployment    | Streamlit Cloud |

---

## 🚀 Installation & Run

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/factoryguard-ai.git
cd factoryguard-ai
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Application

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This app can be deployed easily using:

* Streamlit Cloud
* Render

---

## 🎯 Use Cases

* Industrial machine monitoring
* Predictive maintenance systems
* Manufacturing analytics
* IoT-based smart factories

---

## ⚠️ Limitations

* No real-time sensor integration (manual input only)
* Model performance depends on dataset quality
* Requires retraining for different machine types

---

## 🔮 Future Improvements

* 🌐 IoT sensor integration
* 📊 Real-time monitoring dashboard
* 📱 Alert system (SMS / Email)
* 🤖 Deep learning model enhancement

---

## 👨‍💻 Author

**Abhishek**
B.Tech Student | AI & Data Science Enthusiast

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
