import streamlit as st


def save_garden_layout(
    garden_state,
    year,
    season
):
    """
    Saves the current garden layout into
    Streamlit session state.

    Each bed is stored using a unique key
    based on year, season, and bed ID.
    """

    for bed_id, crop in garden_state.items():

        state_key = (
            f"{year}_{season}_{bed_id}"
        )

        st.session_state[state_key] = crop


def get_previous_year_layout(
    garden_state,
    year,
    season
):
    """
    Retrieves the previous year's garden layout
    from Streamlit session state.

    Args:
        garden_state: Current garden layout.
        year: Current selected year.
        season: Current selected season.

    Returns:
        dict: Previous year's garden layout.
    """

    previous_year = year - 1

    past_garden_state = {}

    for bed_id in garden_state:

        past_key = (
            f"{previous_year}_{season}_{bed_id}"
        )

        past_garden_state[bed_id] = (
            st.session_state.get(
                past_key,
                "Empty"
            )
        )

    return past_garden_state
