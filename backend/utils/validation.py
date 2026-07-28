from typing import Optional
from utils.errors import APIError

def parse_int(
    val: Optional[str],
    default: int,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    field_name: str = "field",
) -> int:
    """Parse an integer from query parameters, using a default if missing."""
    if val is None or val.strip() == "":
        return default
    try:
        parsed = int(val)
    except ValueError:
        raise APIError(f"Invalid integer for '{field_name}' parameter.", status_code=400)
    
    if minimum is not None and parsed < minimum:
        raise APIError(f"Parameter '{field_name}' must be >={minimum}.", status_code=400)
    if maximum is not None and parsed > maximum:
        raise APIError(f"Parameter '{field_name}' must be <={maximum}.", status_code=400)
    
    return parsed


def require_str(val: Optional[str], field_name: str = "field") -> str:
    """Require a string parameter to be present and non-empty."""
    if not val or not val.strip():
        raise APIError(f"Missing required parameter: '{field_name}'", status_code=400)
    return val.strip()
