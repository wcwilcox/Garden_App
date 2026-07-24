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
            crop TEXT NOT NULL,
            UNIQUE(year, season, bed_id)
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

    connection = get_connection()

    cursor = connection.cursor()

    for bed_id, crop in garden_state.items():

        cursor.execute(
            """
            INSERT INTO garden_layouts (
                year,
                season,
                bed_id,
                crop
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(year, season, bed_id)
            DO UPDATE SET
                crop = excluded.crop
            """,
            (
                year,
                season,
                bed_id,
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

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT bed_id, crop
        FROM garden_layouts
        WHERE year = ?
        AND season = ?
        """,
        (
            year,
            season
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return {
        bed_id: crop
        for bed_id, crop in rows
    }


def get_all_layouts():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT year, season, bed_id, crop
        FROM garden_layouts
        ORDER BY year, season, bed_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows