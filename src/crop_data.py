import pandas as pd
import streamlit as st

EXCEL_PATH = "data/Garden_Planning.xlsx"

@st.cache_data
def load_crop_database():
    """Loads the Master Garden Calendar from Excel."""
    try:
        # Update sheet_name if needed to match your tab
        df = pd.read_excel(EXCEL_PATH, sheet_name=0) 
        # Clean column names (strip trailing spaces)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()

def get_crop_mapping():
    """
    Returns a dictionary mapping Abbreviations -> Full Crop Names
    e.g., {'Pk': 'Pumpkin', 'Br': 'Broccoli', ...}
    """
    df = load_crop_database()
    if not df.empty and "Abrv" in df.columns:
        return dict(zip(df["Abrv"], df["Crop Name"]))
    return {}

def get_crop_options():
    """Returns list of abbreviations for selectbox dropdowns."""
    df = load_crop_database()
    if not df.empty and "Abrv" in df.columns:
        return ["Empty"] + sorted(df["Abrv"].dropna().astype(str).tolist())
    return ["Empty"]