import sys
from pathlib import Path


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

root_dir = Path(__file__).resolve().parent

if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

import streamlit as st

from src.crop_data import (
    get_crop_options,
    load_crop_database,
    get_crop_mapping
)

from src.garden_layout import (
    BED_SECTIONS
)

from src.crop_rules import (
    check_seasonality,
    check_nitrogen_rules
)

from src.garden_ui import (
    render_sidebar,
    render_garden_grid
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

st.title(
    "🌱 Personal Garden Planner"
)


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

garden_state = render_garden_grid(
    bed_sections=BED_SECTIONS,
    crop_options=crop_options,
    crop_map=crop_map,
    year=year,
    season=season,
    saved_layout=saved_layout
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


# ---------------------------------------------------------
# SEASONALITY CHECK
# ---------------------------------------------------------

seasonality_alerts = check_seasonality(
    garden_state,
    season,
    crops_df
)


# ---------------------------------------------------------
# NITROGEN ROTATION CHECK
# ---------------------------------------------------------

nitrogen_alerts = check_nitrogen_rules(
    garden_state,
    crops_df,
    past_layout=past_garden_state
)


# ---------------------------------------------------------
# COMBINE ALERTS
# ---------------------------------------------------------

all_alerts = (
    seasonality_alerts
    + nitrogen_alerts
)


# ---------------------------------------------------------
# DISPLAY ALERTS
# ---------------------------------------------------------

if all_alerts:

    for alert in all_alerts:

        st.warning(
            alert
        )

else:

    st.success(
        "✅ No plant conflicts detected "
        "in current layout!"
    )
