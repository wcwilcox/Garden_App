import streamlit as st

from src.garden_layout import (
    BEDS,
    GARDEN_MAP,
)

from src.garden_ui.bed_editor import (
    render_bed,
    render_static_object,
)


def render_garden_map(
    crop_options,
    crop_map,
    saved_layout,
    year,
    season,
):
    """
    Renders the complete physical garden map.

    Returns:
        {
            "BR1": {
                (0, 0): "Pk",
                (0, 1): "Br",
            }
        }
    """

    # -----------------------------------------------------
    # GARDEN PLANNER HEADER
    # -----------------------------------------------------

    st.title("Garden Planner🌱")

    st.header(
        f"{season} {year} Garden"
    )

    # -----------------------------------------------------
    # CURRENT GARDEN STATE
    # -----------------------------------------------------

    current_layout = {}

    # -----------------------------------------------------
    # RENDER PHYSICAL MAP
    # -----------------------------------------------------

    for map_row in GARDEN_MAP:

        map_columns = st.columns(
            len(map_row)
        )

        for map_column, bed_id in zip(
            map_columns,
            map_row
        ):

            with map_column:

                # -----------------------------------------
                # EMPTY MAP SPACE
                # -----------------------------------------

                if not bed_id:

                    st.write("")

                    continue

                # -----------------------------------------
                # CHECK BED EXISTS
                # -----------------------------------------

                if bed_id not in BEDS:

                    st.warning(
                        f"Unknown bed: {bed_id}"
                    )

                    continue

                # -----------------------------------------
                # GET BED TYPE
                # -----------------------------------------

                bed_type = BEDS[
                    bed_id
                ]["type"]

                # -----------------------------------------
                # STATIC OBJECTS
                # -----------------------------------------

                if bed_type in {
                    "W",
                    "TREE",
                }:

                    render_static_object(
                        bed_id
                    )

                    continue

                # -----------------------------------------
                # PLANTING BED
                # -----------------------------------------

                render_bed(
                    bed_id=bed_id,
                    current_layout=current_layout,
                    crop_options=crop_options,
                    crop_map=crop_map,
                    saved_layout=saved_layout,
                    year=year,
                    season=season,
                )

    return current_layout