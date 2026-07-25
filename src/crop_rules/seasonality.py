def check_seasonality(
        current_layout, 
        selected_season, 
        crops_df
    ):
    """
    Warns if a crop is placed in a season it doesn't support according to 'Grow Season'.
    """

    alerts = []
    
    for bed_id, abrv in current_layout.items():

        if abrv == "Empty" or not abrv:
            continue
            
        crop_row = crops_df[
            crops_df["Abrv"] == abrv
        ]
        
        if not crop_row.empty:

            valid_seasons = str(crop_row["Grow Season"].values[0])
            
            # Check if selected season is within the crop's allowed seasons
            if (
                selected_season 
                not in valid_seasons 
                and "Perennial" 
                not in valid_seasons 
                and "Full Season" 
                not in valid_seasons
            ):


                alerts.append(
                    f"📅 **Seasonality Alert in {bed_id}:** {abrv} typically grows in "
                    f"'{valid_seasons}', but current layout is set to '{selected_season}'."
                )
    return alerts