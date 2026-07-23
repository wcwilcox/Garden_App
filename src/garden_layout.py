# Map beds to their visual sections
BED_SECTIONS = {
    "Back Rows": ["BR1", "BR2", "BR3", "BR4"],
    "Raised Beds": ["RB1", "RB2", "RB3"],
    "Front Rows": ["FR1", "FR2", "FR3", "FR4"],
    "Special Plots": ["DRB", "Tower_1", "Tower_2", "T1", "T2"]
}

# Define physical neighbors for spatial rule checks
BED_NEIGHBORS = {
    "FR1": ["FR2", "DRB"],
    "FR2": ["FR1", "FR3", "Tree"],
    "FR3": ["FR2", "FR4"],
    "BR1": ["BR2"],
    "BR2": ["BR1", "BR3"],
    "BR3": ["BR2", "BR4"],
    # Add remaining bed connections...
}