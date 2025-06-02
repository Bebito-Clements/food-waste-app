import streamlit as st
import pandas as pd
import sqlite3

# Page setup
st.set_page_config(page_title="Food Wastage App", layout="wide")
st.title("🍱 Local Food Wastage Management System")

# Database connection
conn = sqlite3.connect("food_waste.db")
cursor = conn.cursor()

