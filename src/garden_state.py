from src.garden_database import (
    save_layout,
    load_layout
)


# ---------------------------------------------------------
# SAVE GARDEN LAYOUT
# ---------------------------------------------------------

def save_garden_layout(
    garden_state,
    year,
    season
):
    """
    Saves the current garden layout
    to the SQLite database.
    """

    save_layout(
        garden_state=garden_state,
        year=year,
        season=season
    )


# ---------------------------------------------------------
# GET GARDEN LAYOUT
# ---------------------------------------------------------

def get_garden_layout(
    year,
    season
):
    """
    Loads a garden layout from
    the SQLite database.
    """

    return load_layout(
        year=year,
        season=season
    )


# ---------------------------------------------------------
# GET PREVIOUS YEAR LAYOUT
# ---------------------------------------------------------

def get_previous_year_layout(
    year,
    season
):
    """
    Loads the garden layout from
    the previous year for the
    same season.
    """

    previous_year = year - 1

    return get_garden_layout(
        year=previous_year,
        season=season
    )