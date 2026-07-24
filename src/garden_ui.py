import streamlit as st


def render_sidebar():
    """
    Renders the sidebar navigation controls.

    Returns:
        tuple: Selected year and season.
    """

    st.sidebar.header(
        "Navigation & History"
    )

    year = st.sidebar.selectbox(
        "Year",
        [2026, 2025, 2024]
    )

    season = st.sidebar.selectbox(
        "Season",
        [
            "Spring",
            "Summer",
            "Fall"
        ]
    )

    st.sidebar.divider()

    st.sidebar.info(
        f"Viewing: **{season} {year}**"
    )

    return year, season


def render_garden_grid(
    bed_sections,
    crop_options,
    crop_map,
    year,
    season,
    saved_layout=None
):
    """
    Renders the garden bed selection grid.

    Args:
        bed_sections:
            Dictionary containing garden sections
            and bed IDs.

        crop_options:
            List of crop abbreviations available
            for selection.

        crop_map:
            Dictionary mapping crop abbreviations
            to full crop names.

        year:
            Selected garden year.

        season:
            Selected garden season.

        saved_layout:
            Previously saved garden layout for
            the selected year and season.

    Returns:
        dict:
            Mapping of bed IDs to selected
            crop abbreviations.
    """

    # Use empty dictionary if no saved layout exists
    if saved_layout is None:

        saved_layout = {}


    garden_state = {}


    # ---------------------------------------------------------
    # RENDER GARDEN SECTIONS
    # ---------------------------------------------------------

    for section_name, beds in bed_sections.items():

        st.subheader(
            section_name
        )

        cols = st.columns(
            len(beds)
        )


        # -----------------------------------------------------
        # RENDER INDIVIDUAL BEDS
        # -----------------------------------------------------

        for idx, bed_id in enumerate(beds):

            with cols[idx]:

                # Bed title
                st.caption(
                    f"**{bed_id}**"
                )


                # -------------------------------------------------
                # DETERMINE SAVED CROP
                # -------------------------------------------------

                saved_crop = saved_layout.get(
                    bed_id,
                    "Empty"
                )


                # -------------------------------------------------
                # DETERMINE DROPDOWN INDEX
                # -------------------------------------------------

                if saved_crop in crop_options:

                    default_index = (
                        crop_options.index(
                            saved_crop
                        )
                    )

                else:

                    default_index = 0


                # -------------------------------------------------
                # CROP SELECTION
                # -------------------------------------------------

                selected_crop = st.selectbox(
                    label=bed_id,
                    options=crop_options,
                    index=default_index,
                    key=f"{year}_{season}_{bed_id}",
                    label_visibility="collapsed"
                )


                # -------------------------------------------------
                # SAVE CURRENT SELECTION
                # -------------------------------------------------

                garden_state[bed_id] = (
                    selected_crop
                )


                # -------------------------------------------------
                # DISPLAY FULL CROP NAME (CAPTION)
                # -------------------------------------------------

                if (
                    selected_crop
                    and selected_crop != "Empty"
                ):

                    full_name = crop_map.get(
                        selected_crop,
                        "Unknown Crop"
                    )

                    st.caption(
                        f"🌿 *{full_name}*"
                    )

                else:

                    st.caption(
                        "⚪ *Empty*"
                    )


    return garden_state