from pathlib import Path
import pandas as pd
import streamlit as st

# Dynamically resolve project root: src/crop_data.py -> src/ -> root/
ROOT_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = ROOT_DIR / "data" / "Garden_Planning.xlsx"

@st.cache_data
def load_crop_database():
    """Loads the Master Garden Calendar from Excel."""
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=0)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading Excel file from {EXCEL_PATH}: {e}")
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