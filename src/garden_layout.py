# ============================================================
# GARDEN LAYOUT
# ============================================================


# ============================================================
# BED TYPES
# ============================================================

BED_TYPES = {

    "BR": {
        "name": "BR Bed",
        "columns": 2,
        "rows": 5,
    },

    "RB": {
        "name": "RB Bed",
        "columns": 3,
        "rows": 5,
    },

    "FR": {
        "name": "FR Bed",
        "columns": 2,
        "rows": 5,
    },

    "DRB": {
        "name": "DRB Bed",
        "columns": 3,
        "rows": 5,
    },

    "TOWER": {
        "name": "Tower",
        "columns": 2,
        "rows": 2,
    },

    "W": {
        "name": "Water",
        "columns": 1,
        "rows": 1,
    },

    "TREE": {
        "name": "Tree",
        "columns": 1,
        "rows": 1,
    },

    "T": {
        "name": "PLANTER",
        "columns": 2,
        "rows": 2,
    },
}


# ============================================================
# PHYSICAL BEDS
# ============================================================

BEDS = {
    # BR Beds
    "BR1": {"type": "BR"},
    "BR2": {"type": "BR"},
    "BR3": {"type": "BR"},
    "BR4": {"type": "BR"},

    # RB Beds
    "RB1": {"type": "RB"},
    "RB2": {"type": "RB"},
    "RB3": {"type": "RB"},

    # FR Beds
    "FR1": {"type": "FR"},
    "FR2": {"type": "FR"},
    "FR3": {"type": "FR"},
    "FR4": {"type": "FR"},

    # DRB Bed
    "DRB": {"type": "DRB"},

    # Planter Towers
    "TOWER1": {"type": "TOWER"},
    "TOWER2": {"type": "TOWER"},

    # Plant Beds
    "PLANT1": {"type": "T"},
    "PLANT2": {"type": "T"},

    # Static Objects
    "W": {"type": "W"},
    "TREE": {"type": "TREE"},
}


# ============================================================
# PHYSICAL GARDEN MAP
# ============================================================

GARDEN_MAP = [
    # BR Beds
    [ None, "BR1", "BR2", "BR3", "BR4", None],

    # Towers and Tree
    ["TOWER1", None, "TREE", None, None],

    # RB Beds
    ["TOWER2", "RB1", "RB2", "RB3", None],

    # Water
    ["W", None, None, None, None],

    # DRB and FR Beds
    ["DRB", "FR1", "FR2", "FR3", "FR4"],

    # Plant Beds
    ["PLANT1", "PLANT2", None, None, None],
]