def parse_time_str(time_str: str) -> int:
    """Convert time string like '10m' or '1h' to total minutes."""
    if time_str.endswith("m"):
        return int(time_str[:-1])
    elif time_str.endswith("h"):
        return int(time_str[:-1]) * 60
    raise ValueError("Time must end with 'm' (minutes) or 'h' (hours)")

def format_minutes(minutes: int) -> str:
    """Format minutes back into 'Xm' string."""
    return f"{minutes}m"
