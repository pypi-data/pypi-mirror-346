from datetime import timedelta


def timedelta_to_hours_and_seconds_string(delta: timedelta) -> str:
    """Convert a timedelta to a string in the format HH:MM."""
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02}:{minutes:02}"
