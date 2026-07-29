import streamlit as st

from src.garden_layout import (
    BEDS,
    BED_TYPES,
)


def render_static_object(
    bed_id
):
    """
    Renders a non-planting object such as
    a tower, water station, or tree.
    """

    bed_type = BEDS[
        bed_id
    ]["type"]

    name = BED_TYPES[
        bed_type
    ]["name"]

    st.markdown(
        f"**{name}**"
    )

    st.caption(
        bed_id
    )


def render_bed(
    bed_id,
    current_layout,
    crop_options,
    crop_map,
    saved_layout,
    year,
    season,
):
    """
    Renders the individual planting cells
    for a garden bed.

    Returns the crop assignment for each cell.
    """

    bed_type = BEDS[
        bed_id
    ]["type"]

    bed_info = BED_TYPES[
        bed_type
    ]

    rows = bed_info[
        "rows"
    ]

    columns = bed_info[
        "columns"
    ]

    bed_name = bed_info[
        "name"
    ]

    st.markdown(
        f"**{bed_name}**"
    )

    st.caption(
        bed_id
    )

    # Get saved cells for this bed
    saved_cells = saved_layout.get(
        bed_id,
        {}
    )

    # Initialize bed state
    bed_state = {}

    # Create one Streamlit column per physical column
    grid_columns = st.columns(
        columns
    )

    # Render rows vertically
    for row in range(rows):

        for column in range(columns):

            cell_position = (
                row,
                column
            )

            saved_crop = saved_cells.get(
                cell_position,
                "Empty"
            )

            # Find the correct Streamlit column
            cell_column = grid_columns[
                column
            ]

            with cell_column:

                selected_crop = st.selectbox(
                    f"{row + 1},{column + 1}",
                    crop_options,
                    index=(
                        crop_options.index(
                            saved_crop
                        )
                        if saved_crop
                        in crop_options
                        else 0
                    ),
                    key=(
                        f"{year}_"
                        f"{season}_"
                        f"{bed_id}_"
                        f"{row}_"
                        f"{column}"
                    ),
                    label_visibility="collapsed",
                )

                bed_state[
                    cell_position
                ] = selected_crop

    current_layout[
        bed_id
    ] = bed_state
