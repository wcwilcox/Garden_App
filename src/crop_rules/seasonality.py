def check_seasonality(
    current_layout,
    selected_season,
    crops_df,
):
    """
    Warns if a crop is placed in a season it doesn't
    support according to 'Grow Season'.
    """

    alerts = []

    for bed_id, bed_layout in current_layout.items():

        # ---------------------------------------------
        # LOOP THROUGH CELLS IN THE BED
        # ---------------------------------------------

        for position, abrv in bed_layout.items():

            # -----------------------------------------
            # SKIP EMPTY CELLS
            # -----------------------------------------

            if not abrv or abrv == "Empty":
                continue

            # -----------------------------------------
            # FIND CROP
            # -----------------------------------------

            crop_row = crops_df[
                crops_df["Abrv"] == abrv
            ]

            # -----------------------------------------
            # SKIP UNKNOWN CROPS
            # -----------------------------------------

            if crop_row.empty:
                continue

            # -----------------------------------------
            # GET VALID SEASONS
            # -----------------------------------------

            valid_seasons = str(
                crop_row["Grow Season"].values[0]
            )

            # -----------------------------------------
            # CHECK SEASONALITY
            # -----------------------------------------

            if (
                selected_season not in valid_seasons
                and "Perennial" not in valid_seasons
                and "Full Season" not in valid_seasons
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