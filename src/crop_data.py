from pathlib import Path
import pandas as pd
import streamlit as st

# Path relative to src/crop_data.py -> project root -> data / Garden_Planning.xlsx
ROOT_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = ROOT_DIR / "data" / "Garden_Planning.xlsx"

# src/crop_data.py
@st.cache_data
def load_crop_database():
    """Loads the Master Garden Calendar from Excel."""
    try:
        # Change header=1 to match the actual header row index in Excel (0-indexed)
        df = pd.read_excel(EXCEL_PATH, sheet_name=0, header=1)
        
        # Clean column names
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
        clean_df = df.dropna(
            subset=["Abrv", "Crop Name"]
        )

        return dict(
            zip(
                clean_df["Abrv"].astype(str).str.strip(),
                clean_df["Crop Name"].astype(str).str.strip()
            )
        )
    return {}

def get_crop_options():
    """
    Returns a sorted list of crop abbreviations
    for the garden selection dropdowns.
    """

    df = load_crop_database()

    if (
        not df.empty
        and "Abrv" in df.columns
    ):

        abbreviations = (
            df["Abrv"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return [
            "Empty"
        ] + sorted(abbreviations)

    return ["Empty"]