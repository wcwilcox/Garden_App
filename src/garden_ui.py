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
    season
):
    """
    Renders the garden bed selection grid.

    Args:
        bed_sections: Dictionary containing garden sections and bed IDs.
        crop_options: List of crop abbreviations available for selection.
        crop_map: Dictionary mapping crop abbreviations to full crop names.
        year: Selected garden year.
        season: Selected garden season.

    Returns:
        dict: Mapping of bed IDs to selected crop abbreviations.
    """

    garden_state = {}

    for section_name, beds in bed_sections.items():

        st.subheader(section_name)

        cols = st.columns(len(beds))

        for idx, bed_id in enumerate(beds):

            with cols[idx]:

                # Bed title
                st.caption(
                    f"**{bed_id}**"
                )

                # Crop selection
                selected_crop = st.selectbox(
                    label=bed_id,
                    options=crop_options,
                    key=f"{year}_{season}_{bed_id}",
                    label_visibility="collapsed"
                )

                # Save selected crop
                garden_state[bed_id] = selected_crop

                # Display full crop name
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
