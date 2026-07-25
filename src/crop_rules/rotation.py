# src/crop_rules/rotation.py


def check_crop_family_rules(
    current_layout,
    crops_df,
    past_layout=None
):
    """
    Checks if crops from the same crop family are planted
    in the same bed in consecutive years.

    Example:

        Previous year: Pumpkin
        Current year:  Zucchini

    Both are Cucurbits, so a rotation warning is generated.
    """

    alerts = []

    # No historical layout or crop data
    if (
        past_layout is None
        or crops_df.empty
    ):
        return alerts

    # Clean column names
    crops_df.columns = (
        crops_df.columns
        .str.strip()
    )

    # Make sure required columns exist
    if (
        "Abrv" not in crops_df.columns
        or "Crop Family" not in crops_df.columns
    ):
        return alerts

    # Create crop family lookup
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
        if not abrv:
            continue

        # Ignore missing crop families
        if (
            not family
            or family == "NAN"
        ):
            continue

        crop_families[abrv] = family

    # Compare current year against previous year
    for bed_id, current_abrv in current_layout.items():

        # Normalize current crop abbreviation
        current_crop = (
            str(current_abrv)
            .strip()
            .upper()
        )

        # Ignore empty current beds
        if (
            not current_crop
            or current_crop == "EMPTY"
        ):
            continue

        # Get previous year's crop
        past_abrv = past_layout.get(
            bed_id,
            "Empty"
        )

        # Normalize previous crop abbreviation
        past_crop = (
            str(past_abrv)
            .strip()
            .upper()
        )

        # Ignore empty previous beds
        if (
            not past_crop
            or past_crop == "EMPTY"
        ):
            continue

        # Get crop families
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

        # Check if both crops belong to
        # the same crop family
        if current_family == past_family:

            alerts.append(
                f"⚠️ **Crop Family Rotation Warning in {bed_id}:** "
                f"{past_abrv} last year → "
                f"{current_abrv} this year. "
                f"Both crops belong to the "
                f"{current_family.title()} family. "
                f"Consider rotating to a different crop family."
            )

    return alerts