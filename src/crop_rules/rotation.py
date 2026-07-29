# src/crop_rules/rotation.py

def check_crop_family_rules(
current_layout,
crops_df,
past_layout=None,
):


    alerts = []

    # -------------------------------------------------
    # NO HISTORICAL LAYOUT OR CROP DATA
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
        crops_df.columns
        .str.strip()
    )

    # -------------------------------------------------
    # REQUIRED COLUMNS
    # -------------------------------------------------

    if (
        "Abrv" not in crops_df.columns
        or "Crop Family" not in crops_df.columns
    ):
        return alerts

    # -------------------------------------------------
    # CREATE CROP FAMILY LOOKUP
    # -------------------------------------------------

    crop_families = {}

    for _, row in crops_df.iterrows():

        abrv = (
            str(row["Abrv"])
            .strip()
            .upper()
        )

        family = (
            str(row["Crop Family"])
            .strip()
            .upper()
        )

        # Ignore missing crop abbreviations
        if (
            not abrv
            or abrv == "NAN"
        ):
            continue

        # Ignore missing crop families
        if (
            not family
            or family == "NAN"
        ):
            continue

        crop_families[
            abrv
        ] = family

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

            # Normalize current crop
            current_crop = (
                str(current_abrv)
                .strip()
                .upper()
            )

            # Ignore empty current cells
            if (
                not current_crop
                or current_crop == "EMPTY"
            ):
                continue

            # -------------------------------------------------
            # GET PREVIOUS YEAR'S CROP
            # -------------------------------------------------

            past_abrv = past_bed.get(
                position,
                "Empty"
            )

            # Normalize previous crop
            past_crop = (
                str(past_abrv)
                .strip()
                .upper()
            )

            # Ignore empty previous cells
            if (
                not past_crop
                or past_crop == "EMPTY"
            ):
                continue

            # -------------------------------------------------
            # GET CROP FAMILIES
            # -------------------------------------------------

            current_family = crop_families.get(
                current_crop
            )

            past_family = crop_families.get(
                past_crop
            )

            # Skip if either crop is not found
            # or has no family information
            if (
                not current_family
                or not past_family
            ):
                continue

            # -------------------------------------------------
            # CHECK SAME CROP FAMILY
            # -------------------------------------------------

            if current_family == past_family:

                row, column = position

                alerts.append(
                    f"⚠️ **Crop Family Rotation Warning "
                    f"in {bed_id} "
                    f"(Row {row + 1}, "
                    f"Column {column + 1}):** "
                    f"{past_abrv} last year → "
                    f"{current_abrv} this year. "
                    f"Both crops belong to the "
                    f"{current_family.title()} family. "
                    f"Consider rotating to a different "
                    f"crop family."
                )

    return alerts
