def wrap_text(input: str, limit: int) -> str:
    words = input.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + (1 if current_line else 0) <= limit:
            current_line.append(word)
            current_length += len(word) + (1 if len(current_line) > 1 else 0)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)


def is_older(v1: str, v2: str) -> bool:
    """Compares two version strings (e.g., '1.2.3' and '1.3.0'). Returns True if v1 is older than v2."""
    v1_parts = [int(p) for p in v1.split(".")]
    v2_parts = [int(p) for p in v2.split(".")]

    return v1_parts < v2_parts
