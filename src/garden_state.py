import streamlit as st


def initialize_garden_history():
    """
    Initializes the garden history dictionary
    in Streamlit session state.
    """

    if "garden_history" not in st.session_state:

        st.session_state.garden_history = {}


def save_garden_layout(
    garden_state,
    year,
    season
):
    """
    Saves the current garden layout for
    the selected year and season.

    Args:
        garden_state: Dictionary mapping bed IDs
                      to crop abbreviations.
        year: Selected garden year.
        season: Selected garden season.
    """

    # Make sure history exists
    initialize_garden_history()

    # Create unique history key
    history_key = (
        f"{year}_{season}"
    )

    # Save a copy of the layout
    st.session_state.garden_history[
        history_key
    ] = garden_state.copy()


def get_garden_layout(
    year,
    season
):
    """
    Retrieves a saved garden layout
    for a specific year and season.

    Returns:
        dict: Saved garden layout.

        Returns an empty dictionary if
        no layout has been saved.
    """

    # Make sure history exists
    initialize_garden_history()

    # Create lookup key
    history_key = (
        f"{year}_{season}"
    )

    # Retrieve saved layout
    return st.session_state.garden_history.get(
        history_key,
        {}
    ).copy()


def get_previous_year_layout(
    year,
    season
):
    """
    Retrieves the garden layout from
    the previous year for the same season.

    Example:

        Current:
        2026 Spring

        Previous:
        2025 Spring

    Returns:
        dict: Previous year's garden layout.
    """

    previous_year = year - 1

    return get_garden_layout(
        year=previous_year,
        season=season
    )
