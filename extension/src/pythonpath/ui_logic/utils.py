def is_older(v1: str, v2: str) -> bool:
    """Compares two version strings (e.g., '1.2.3' and '1.3.0'). Returns True if v1 is older than v2."""
    v1_parts = [int(p) for p in v1.split(".")]
    v2_parts = [int(p) for p in v2.split(".")]

    return v1_parts < v2_parts
