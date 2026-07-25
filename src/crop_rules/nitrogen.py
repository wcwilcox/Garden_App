def check_nitrogen_rules(
    current_layout,
    crops_df,
    past_layout=None
):
    """
    Checks if a High Nitrogen crop is planted in a bed
    where a High Nitrogen crop was planted the previous year.
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
        crops_df.columns.str.strip()
    )

    # Find nitrogen-related column
    nitro_col = None

    for col in crops_df.columns:

        if "nitrogen" in col.lower():

            nitro_col = col
            break

    # No nitrogen column found
    if not nitro_col:
        return alerts

    # Get all High Nitrogen crops
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


    # Compare current year against previous year
    for bed_id, current_abrv in current_layout.items():

        # Ignore empty current beds
        if (
            not current_abrv
            or current_abrv == "Empty"
        ):
            continue

        # Get previous year's crop
        past_abrv = past_layout.get(
            bed_id,
            "Empty"
        )

        # Ignore empty previous beds
        if (
            not past_abrv
            or past_abrv == "Empty"
        ):
            continue

        # Check BOTH crops
        if (
            current_abrv in high_n_crops
            and past_abrv in high_n_crops
        ):

            alerts.append(
                f"⚠️ **Crop Rotation Warning in {bed_id}:** "
                f"Consecutive High Nitrogen crops "
                f"({past_abrv} last year → "
                f"{current_abrv} this year)."
            )

    return alerts