import streamlit as st
import pandas as pd
import sqlite3

# Page setup
st.set_page_config(page_title="Food Wastage App", layout="wide")
st.title("🍱 Local Food Wastage Management System")

# Database connection
conn = sqlite3.connect("food_waste.db")
cursor = conn.cursor()
st.sidebar.header("🔍 Filter Food Listings")

# Get unique values for dropdowns
cities = pd.read_sql_query("SELECT DISTINCT Location FROM food_listings", conn)["Location"].tolist()
food_types = pd.read_sql_query("SELECT DISTINCT Food_Type FROM food_listings", conn)["Food_Type"].tolist()
meal_types = pd.read_sql_query("SELECT DISTINCT Meal_Type FROM food_listings", conn)["Meal_Type"].tolist()

# Sidebar controls
selected_city = st.sidebar.selectbox("Select City", ["All"] + cities)
selected_food_type = st.sidebar.selectbox("Select Food Type", ["All"] + food_types)
selected_meal_type = st.sidebar.selectbox("Select Meal Type", ["All"] + meal_types)
# Build SQL query based on filters
query = "SELECT * FROM food_listings WHERE 1=1"

if selected_city != "All":
    query += f" AND Location = '{selected_city}'"
if selected_food_type != "All":
    query += f" AND Food_Type = '{selected_food_type}'"
if selected_meal_type != "All":
    query += f" AND Meal_Type = '{selected_meal_type}'"

results = pd.read_sql_query(query, conn)

st.subheader("📋 Available Food Listings")
st.dataframe(results)
st.subheader("📞 Contact Info of Providers (For Visible Listings)")
if not results.empty:
    provider_ids = tuple(results["Provider_ID"].unique())
    contact_query = f"SELECT * FROM providers WHERE Provider_ID IN {provider_ids}"
    contact_df = pd.read_sql_query(contact_query, conn)
    st.dataframe(contact_df)
else:
    st.info("No food listings match your filters.")

