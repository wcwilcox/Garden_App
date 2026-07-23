import sys
from pathlib import Path

# Fix import path for local and Streamlit Cloud environments
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import streamlit as st
from src.crop_data import get_crop_options, load_crop_database, get_crop_mapping
from src.garden_layout import BED_SECTIONS
from src.crop_rules import check_seasonality, check_nitrogen_rules

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Planner", layout="wide")
st.title("🌱 Personal Garden Planner")

# --- LOAD DATA & MAPPINGS ---
crops_df = load_crop_database()
crop_options = get_crop_options()
crop_map = get_crop_mapping()

# --- SIDEBAR: NAVIGATION & HISTORY ---
st.sidebar.header("Navigation & History")
year = st.sidebar.selectbox("Year", [2026, 2025, 2024])
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Fall"])

st.sidebar.divider()
st.sidebar.info(f"Viewing: **{season} {year}**")

# --- GARDEN GRID RENDERER ---
garden_state = {}

for section_name, beds in BED_SECTIONS.items():
    st.subheader(section_name)
    cols = st.columns(len(beds))
    
    for idx, bed_id in enumerate(beds):
        with cols[idx]:
            # Bed Title
            st.caption(f"**{bed_id}**")
            
            # Crop Selection Dropdown
            selected_crop = st.selectbox(
                label=bed_id,
                options=crop_options,
                key=f"{year}_{season}_{bed_id}",
                label_visibility="collapsed"
            )
            
            # Save to state dictionary
            garden_state[bed_id] = selected_crop
            
            # Dynamic Tooltip: Displays full crop name under each box when selected
            if selected_crop and selected_crop != "Empty":
                full_name = crop_map.get(selected_crop, "Unknown Crop")
                st.caption(f"🌿 *{full_name}*")
            else:
                st.caption("⚪ *Empty*")

# --- VALIDATION & ALERTS SECTION ---
st.divider()
st.header("⚠️ Validation & Alerts")

# 1. Initialize historical state (safe fallback if no past data yet)
past_garden_state = st.session_state.get("past_garden_state", {})

# 2. Run rule checks
seasonality_alerts = check_seasonality(garden_state, season, crops_df)
nitrogen_alerts = check_nitrogen_rules(garden_state, crops_df, past_layout=past_garden_state)

# 3. Combine alerts
all_alerts = seasonality_alerts + nitrogen_alerts

if all_alerts:
    for alert in all_alerts:
        st.warning(alert)
else:
    st.success("✅ No plant conflicts detected in current layout!")