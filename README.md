# food-waste-app
# 🍱 Local Food Wastage Management System

A data-driven web app built using **Python, SQLite, Pandas, and Streamlit** to connect food providers (like restaurants) with receivers (like NGOs), minimizing food waste in local communities.

## 🚀 Live App

🔗 [Click here to view the live app](https://your-deployed-link.streamlit.app)

## 📦 Tech Stack

- **Python**
- **SQLite** (relational database)
- **Pandas** (data analysis)
- **Streamlit** (web UI)
- **GitHub** + **Streamlit Cloud** (deployment)

## 🧠 Features

- 🔍 Filter food listings by city, type, and meal
- 📞 View provider contact info for available food
- 📊 Insights via SQL (Top providers, most claimed meals, total quantity, etc.)
- ✅ Live app with user-friendly interface

## 🗃️ Data Sources

- `providers_data.csv`
- `receivers_data.csv`
- `food_listings_data.csv`
- `claims_data.csv`

## 🛠 How to Run Locally

# Clone the repo:
   ```bash
   git clone https://github.com/Bebito-Clements/food-waste-app.git
   cd food-waste-app
   
# Install required packages
pip install streamlit pandas

# Run the app
streamlit run app.py
