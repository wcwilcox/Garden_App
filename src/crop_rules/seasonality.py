def check_seasonality(
current_layout,
selected_season,
crops_df,
):

alerts = []

# -------------------------------------------------
# CLEAN COLUMN NAMES
# -------------------------------------------------

crops_df.columns = (
    crops_df.columns
    .str.strip()
)

# -------------------------------------------------
# REQUIRED COLUMNS
# -------------------------------------------------

if (
    "Abrv" not in crops_df.columns
    or "Grow Season" not in crops_df.columns
):
    return alerts

# -------------------------------------------------
# LOOP THROUGH BEDS
# -------------------------------------------------

for bed_id, bed_layout in current_layout.items():

    # Make sure bed contains cell data
    if not isinstance(
        bed_layout,
        dict
    ):
        continue

    # -------------------------------------------------
    # LOOP THROUGH CELLS IN THE BED
    # -------------------------------------------------

    for position, abrv in bed_layout.items():

        # -------------------------------------------------
        # SKIP EMPTY CELLS
        # -------------------------------------------------

        if (
            not abrv
            or abrv == "Empty"
        ):
            continue

        # -------------------------------------------------
        # NORMALIZE CROP ABBREVIATION
        # -------------------------------------------------

        abrv = str(
            abrv
        ).strip()

        # -------------------------------------------------
        # FIND CROP
        # -------------------------------------------------

        crop_row = crops_df[
            crops_df["Abrv"]
            .astype(str)
            .str.strip()
            == abrv
        ]

        # -------------------------------------------------
        # SKIP UNKNOWN CROPS
        # -------------------------------------------------

        if crop_row.empty:
            continue

        # -------------------------------------------------
        # GET VALID SEASONS
        # -------------------------------------------------

        valid_seasons = str(
            crop_row[
                "Grow Season"
            ].values[0]
        ).strip()

        # -------------------------------------------------
        # CHECK SEASONALITY
        # -------------------------------------------------

        if (
            selected_season
            not in valid_seasons
            and "Perennial"
            not in valid_seasons
            and "Full Season"
            not in valid_seasons
        ):

            row, column = position

            alerts.append(
                f"📅 **Seasonality Alert in "
                f"{bed_id} "
                f"(Row {row + 1}, "
                f"Column {column + 1}):** "
                f"{abrv} typically grows in "
                f"'{valid_seasons}', but current "
                f"layout is set to "
                f"'{selected_season}'."
            )

return alerts
