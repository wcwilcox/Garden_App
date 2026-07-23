# src/crop_rules.py

def check_nitrogen_rules(current_layout, crops_df, past_layout=None):
    """
    Checks if a High Nitrogen crop is planted where another High Nitrogen 
    crop was planted in the previous year.
    """
    alerts = []
    if past_layout is None or crops_df.empty:
        return alerts  # Skip check if no past layout or empty dataframe

    # Clean up column names (strips whitespace)
    crops_df.columns = crops_df.columns.str.strip()

    # Look for the nitrogen column (handles 'Nitrogen Level', 'Nitrogen', etc.)
    nitro_col = None
    for col in crops_df.columns:
        if "nitrogen" in col.lower():
            nitro_col = col
            break

    if not nitro_col:
        # If no nitrogen column exists in Excel, return without crashing
        return alerts

    # Filter high nitrogen crops (case-insensitive check for 'High')
    high_n_crops = crops_df[
        crops_df[nitro_col].astype(str).str.strip().str.lower() == "high"
    ]["Abrv"].tolist()

    for bed_id, current_abrv in current_layout.items():
        if current_abrv in high_n_crops:
            past_abrv = past_layout.get(bed_id)
            if past_abrv in high_n_crops:
                alerts.append(
                    f"⚠️ **Crop Rotation Warning in {bed_id}:** "
                    f"Consecutive High Nitrogen crops ({past_abrv} last year → {current_abrv} this year)."
                )

    return alerts



def check_seasonality(current_layout, selected_season, crops_df):
    """
    Warns if a crop is placed in a season it doesn't support according to 'Grow Season'.
    """
    alerts = []
    
    for bed_id, abrv in current_layout.items():
        if abrv == "Empty" or not abrv:
            continue
            
        crop_row = crops_df[crops_df["Abrv"] == abrv]
        if not crop_row.empty:
            valid_seasons = str(crop_row["Grow Season"].values[0])
            
            # Check if selected season is within the crop's allowed seasons
            if selected_season not in valid_seasons and "Perennial" not in valid_seasons and "Full Season" not in valid_seasons:
                alerts.append(
                    f"📅 **Seasonality Alert in {bed_id}:** {abrv} typically grows in "
                    f"'{valid_seasons}', but current layout is set to '{selected_season}'."
                )
    return alerts