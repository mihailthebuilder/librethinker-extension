def is_older(v1: str, v2: str) -> bool:
    """Compares two version strings (e.g., '1.2.3' and '1.3.0'). Returns True if v1 is older than v2."""
    v1_parts = [int(p) for p in v1.split(".")]
    v2_parts = [int(p) for p in v2.split(".")]

    return v1_parts < v2_parts


# sh/ollama/ is deprecated in favour of sh/, but still accepted.
# Longest first so sh/ollama/ is stripped before the generic sh/ prefix.
SELF_HOSTED_PREFIXES = ("sh/ollama/", "sh/")


def is_self_hosted(model: str) -> bool:
    return model.startswith("sh/")


def self_hosted_model(model: str) -> str:
    for prefix in SELF_HOSTED_PREFIXES:
        if model.startswith(prefix):
            return model[len(prefix) :]
    return model
