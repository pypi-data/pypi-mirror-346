# **************************************************************************************

# @package        pwi
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************


def convert_arcminutes_to_degrees(arcminutes: float) -> float:
    """
    Convert arcminutes to degrees.

    Args:
        arcminutes (float): The value in arcminutes.

    Returns:
        float: The value in degrees.
    """
    return arcminutes / 60.0


# **************************************************************************************


def convert_arcseconds_to_degrees(arcseconds: float) -> float:
    """
    Convert arcseconds to degrees.

    Args:
        arcseconds (float): The value in arcseconds.

    Returns:
        float: The value in degrees.
    """
    return arcseconds / 3600.0


# **************************************************************************************
