def check_nitrogen_rules(
    current_layout,
    crops_df,
    past_layout=None,
):
    """
    Checks if a High Nitrogen crop is planted in the same
    bed cell where a High Nitrogen crop was planted the
    previous year.
    """

    alerts = []

    # -------------------------------------------------
    # NO HISTORY OR CROP DATA
    # -------------------------------------------------

    if (
        past_layout is None
        or crops_df.empty
    ):
        return alerts

    # -------------------------------------------------
    # CLEAN COLUMN NAMES
    # -------------------------------------------------

    crops_df.columns = (
        crops_df.columns.str.strip()
    )

    # -------------------------------------------------
    # FIND NITROGEN COLUMN
    # -------------------------------------------------

    nitro_col = None

    for col in crops_df.columns:

        if "nitrogen" in col.lower():

            nitro_col = col
            break

    # No nitrogen column found
    if not nitro_col:
        return alerts

    # -------------------------------------------------
    # GET HIGH NITROGEN CROPS
    # -------------------------------------------------

    high_n_crops = set(
        crops_df[
            crops_df[nitro_col]
            .astype(str)
            .str.strip()
            .str.lower()
            == "high"
        ]["Abrv"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    # -------------------------------------------------
    # COMPARE CURRENT YEAR TO PREVIOUS YEAR
    # -------------------------------------------------

    for bed_id, current_bed in current_layout.items():

        # Get previous year's bed
        past_bed = past_layout.get(
            bed_id,
            {}
        )

        # Make sure previous bed is a dictionary
        if not isinstance(
            past_bed,
            dict
        ):
            continue

        # -------------------------------------------------
        # CHECK EACH CELL
        # -------------------------------------------------

        for position, current_abrv in current_bed.items():

            # Ignore empty current cells
            if (
                not current_abrv
                or current_abrv == "Empty"
            ):
                continue

            # Get previous year's crop
            past_abrv = past_bed.get(
                position,
                "Empty"
            )

            # Ignore empty previous cells
            if (
                not past_abrv
                or past_abrv == "Empty"
            ):
                continue

            # -------------------------------------------------
            # CHECK BOTH CROPS
            # -------------------------------------------------

            if (
                current_abrv in high_n_crops
                and past_abrv in high_n_crops
            ):

                row, column = position

                alerts.append(
                    f"⚠️ **Crop Rotation Warning in "
                    f"{bed_id} "
                    f"(Row {row + 1}, "
                    f"Column {column + 1}):** "
                    f"Consecutive High Nitrogen crops "
                    f"({past_abrv} last year → "
                    f"{current_abrv} this year)."
                )

    return alerts