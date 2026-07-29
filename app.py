#streamlit run app.py

import streamlit as st

from src.garden_database import (
    initialize_database,
)

from src.crop_data import (
    get_crop_options,
    load_crop_database,
    get_crop_mapping
)

from src.crop_rules.validator import validate_layout

from src.garden_ui.sidebar import (
    render_sidebar
)

from src.garden_ui.garden_renderer import (
    render_garden_map
)

from src.garden_state import (
    save_garden_layout,
    get_garden_layout,
    get_previous_year_layout
)



# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Garden Planner",
    layout="wide"
)


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

initialize_database()


# ---------------------------------------------------------
# LOAD CROP DATA
# ---------------------------------------------------------

crops_df = load_crop_database()

crop_options = get_crop_options()

crop_map = get_crop_mapping()


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

year, season = render_sidebar()


# ---------------------------------------------------------
# LOAD SAVED GARDEN LAYOUT
# ---------------------------------------------------------

saved_layout = get_garden_layout(
    year=year,
    season=season
)


# ---------------------------------------------------------
# GARDEN GRID
# ---------------------------------------------------------

garden_state = render_garden_map(
    crop_options=crop_options,
    crop_map=crop_map,
    saved_layout=saved_layout,
    year=year,
    season=season,
)


# ---------------------------------------------------------
# SAVE CURRENT GARDEN STATE
# ---------------------------------------------------------

save_garden_layout(
    garden_state=garden_state,
    year=year,
    season=season
)


# ---------------------------------------------------------
# HISTORICAL STATE
# ---------------------------------------------------------

past_garden_state = get_previous_year_layout(
    year=year,
    season=season
)


# ---------------------------------------------------------
# VALIDATION & ALERTS
# ---------------------------------------------------------

st.divider()

st.header(
    "⚠️ Validation & Alerts"
)


alerts = validate_layout(
    current_layout=garden_state,
    past_layout=past_garden_state,
    selected_season=season,
    crops_df=crops_df
)

if alerts:

    for alert in alerts:

        st.warning(
            alert
        )

else:

    st.success(
        "✅ No plant conflicts detected "
        "in current layout!"
    )
