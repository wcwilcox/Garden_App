from .nitrogen import check_nitrogen_rules
from .rotation import check_crop_family_rules
from .seasonality import check_seasonality


def validate_layout(
    current_layout,
    past_layout,
    selected_season,
    crops_df
):

    alerts = []

    alerts.extend(
        check_nitrogen_rules(
            current_layout,
            crops_df,
            past_layout
        )
    )

    alerts.extend(
        check_crop_family_rules(
            current_layout,
            crops_df,
            past_layout
        )
    )

    alerts.extend(
        check_seasonality(
            current_layout,
            selected_season,
            crops_df
        )
    )

    return alerts