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