import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

DATA_DIR.mkdir(
    exist_ok=True
)

DATABASE_PATH = DATA_DIR / "garden.db"


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS garden_layouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            year INTEGER NOT NULL,

            season TEXT NOT NULL,

            bed_id TEXT NOT NULL,

            row INTEGER NOT NULL,

            column INTEGER NOT NULL,

            crop TEXT NOT NULL,

            UNIQUE(
                year,
                season,
                bed_id,
                row,
                column
            )
        )
        """
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------------
# SAVE GARDEN LAYOUT
# ---------------------------------------------------------

def save_layout(
    garden_state,
    year,
    season
):
    """
    Saves the current garden layout.

    Each planting cell is stored as an
    individual database record.

    Expected garden_state format:

        {
            "BR1": {
                (0, 0): "Tomato",
                (0, 1): "Tomato",
                (1, 0): "Beans",
            }
        }
    """

    connection = get_connection()

    cursor = connection.cursor()

    for bed_id, cells in garden_state.items():

        for (
            cell_position,
            crop
        ) in cells.items():

            row, column = cell_position

            cursor.execute(
                """
                INSERT INTO garden_layouts (
                    year,
                    season,
                    bed_id,
                    row,
                    column,
                    crop
                )
                VALUES (?, ?, ?, ?, ?, ?)

                ON CONFLICT(
                    year,
                    season,
                    bed_id,
                    row,
                    column
                )

                DO UPDATE SET
                    crop = excluded.crop
                """,
                (
                    year,
                    season,
                    bed_id,
                    row,
                    column,
                    crop
                )
            )

    connection.commit()

    connection.close()


# ---------------------------------------------------------
# LOAD GARDEN LAYOUT
# ---------------------------------------------------------

def load_layout(
    year,
    season
):
    """
    Loads a garden layout from SQLite.

    Returns:

        {
            "BR1": {
                (0, 0): "Tomato",
                (0, 1): "Tomato",
            }
        }
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            bed_id,
            row,
            column,
            crop

        FROM garden_layouts

        WHERE year = ?
        AND season = ?

        ORDER BY
            bed_id,
            row,
            column
        """,
        (
            year,
            season
        )
    )

    rows = cursor.fetchall()

    connection.close()


    garden_state = {}


    for (
        bed_id,
        row,
        column,
        crop
    ) in rows:

        if bed_id not in garden_state:

            garden_state[
                bed_id
            ] = {}

        garden_state[
            bed_id
        ][
            (row, column)
        ] = crop


    return garden_state


# ---------------------------------------------------------
# GET ALL LAYOUTS
# ---------------------------------------------------------

def get_all_layouts():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            year,
            season,
            bed_id,
            row,
            column,
            crop

        FROM garden_layouts

        ORDER BY
            year,
            season,
            bed_id,
            row,
            column
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows