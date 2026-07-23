import streamlit as st
import pandas as pd

st.title("🌱 Personal Garden Planner")

# --- 1. LOAD YOUR EXCEL DATA ---
@st.cache_data
def load_data():
    # Load crop database (sheet 1)
    crops_df = pd.read_excel("Garden_Planning.xlsx", sheet_name="CropDatabase")
    return crops_df

try:
    crops_df = load_data()
    crop_options = ["Empty"] + crops_df["Abbreviation"].tolist()
except Exception:
    # Fallback dummy data if file isn't connected yet
    crop_options = ["Empty", "TOM", "CRN", "BEA", "SQU"]
    crops_df = pd.DataFrame({
        "Abbreviation": ["TOM", "CRN", "BEA", "SQU"],
        "Name": ["Tomato", "Corn", "Beans", "Squash"],
        "Nitrogen": ["High", "High", "Fixer", "Medium"]
    })

# --- 2. SELECT YEAR & SEASON ---
col_year, col_season = st.columns(2)
with col_year:
    year = st.selectbox("Year", [2026, 2025, 2024])
with col_season:
    season = st.selectbox("Season", ["Spring", "Summer", "Fall"])

st.divider()

# --- 3. GARDEN GRID SELECTION ---
st.subheader(f"Garden Layout: {season} {year}")

# Set up a 2x2 grid using Streamlit columns
grid_data = {}
cols_row1 = st.columns(2)
cols_row2 = st.columns(2)

with cols_row1[0]:
    grid_data["A1"] = st.selectbox("Plot A1", crop_options, key="A1")
with cols_row1[1]:
    grid_data["B1"] = st.selectbox("Plot B1", crop_options, key="B1")

with cols_row2[0]:
    grid_data["A2"] = st.selectbox("Plot A2", crop_options, key="A2")
with cols_row2[1]:
    grid_data["B2"] = st.selectbox("Plot B2", crop_options, key="B2")

# --- 4. SIMPLE RULE CHECKS ---
st.divider()
st.subheader("⚠️ Rule Checks & Alerts")

# Example Check 1: High Nitrogen Conflict in Same Cell
# (In a full app, you would compare current year vs last year's data)
high_n_crops = crops_df[crops_df["Nitrogen"] == "High"]["Abbreviation"].tolist()

for cell, crop in grid_data.items():
    if crop in high_n_crops:
        st.warning(f"**{cell}**: {crop} is a **High Nitrogen** consumer. Ensure crop rotation for next season!")

# Example Check 2: Companion Plant Rule
if grid_data["A1"] == "TOM" and grid_data["B1"] == "CRN":
    st.error("**Companion Warning!** Tomatoes and Corn in adjacent plots (A1 & B1) can attract the same pests.")