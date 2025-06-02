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
    provider_ids = results["Provider_ID"].dropna().unique().tolist()

    if len(provider_ids) == 0:
        st.warning("No provider IDs found for current listings.")
    elif len(provider_ids) == 1:
        contact_query = f"SELECT * FROM providers WHERE Provider_ID = {provider_ids[0]}"
        contact_df = pd.read_sql_query(contact_query, conn)
        st.dataframe(contact_df)
    else:
        id_list = ",".join(str(id) for id in provider_ids)
        contact_query = f"SELECT * FROM providers WHERE Provider_ID IN ({id_list})"
        contact_df = pd.read_sql_query(contact_query, conn)
        st.dataframe(contact_df)
else:
    st.info("No food listings match your filters.")
    st.subheader("📊 Food Wastage Insights")

tab1, tab2, tab3 = st.tabs(["Top Providers", "Food Trends", "Receiver Stats"])

with tab1:
    st.markdown("### 🏙️ Providers by City")
    st.dataframe(pd.read_sql_query("""
        SELECT City, COUNT(*) AS Provider_Count
        FROM providers
        GROUP BY City
    """, conn))

    st.markdown("### 🥇 Providers with Most Donations")
    st.dataframe(pd.read_sql_query("""
        SELECT p.Name, SUM(f.Quantity) AS Total_Donated
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY Total_Donated DESC
        LIMIT 5
    """, conn))

with tab2:
    st.markdown("### 🍽️ Most Common Food Types")
    st.dataframe(pd.read_sql_query("""
        SELECT Food_Type, COUNT(*) AS Count
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Count DESC
    """, conn))

    st.markdown("### 🍱 Meal Types Claimed Most")
    st.dataframe(pd.read_sql_query("""
        SELECT f.Meal_Type, COUNT(*) AS Claim_Count
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY Claim_Count DESC
    """, conn))

    st.markdown("### 📦 Total Food Quantity Available")
    st.dataframe(pd.read_sql_query("""
        SELECT SUM(Quantity) AS Total_Quantity
        FROM food_listings
    """, conn))

with tab3:
    st.markdown("### 📈 Top 5 Receivers by Claims")
    st.dataframe(pd.read_sql_query("""
        SELECT r.Name, COUNT(*) AS Total_Claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY c.Receiver_ID
        ORDER BY Total_Claims DESC
        LIMIT 5
    """, conn))

    st.markdown("### ✅ Claim Status Breakdown")
    st.dataframe(pd.read_sql_query("""
        SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage
        FROM claims
        GROUP BY Status
    """, conn))





