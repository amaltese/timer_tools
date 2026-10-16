def format_seconds(s: int) -> str:
    """Format seconds as MM:SS."""
    m = s // 60
    sec = s % 60
    return f"{m:02d}:{sec:02d}"
