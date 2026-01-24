from typing import Optional

def available(introduced: str, deprecated: Optional[str] = None, removed: Optional[str] = None):
    """
    Decorator to mark an endpoint's availability.

    Args:
        introduced: The version this endpoint was introduced (e.g. "0.1")
        deprecated: The version this endpoint became deprecated (e.g. "0.9")
        removed: The version this endpoint was removed (e.g. "1.0")
    """
    def decorator(func):
        # Store metadata on the function object itself
        func._api_version_intro = introduced
        func._api_version_depr = deprecated
        func._api_version_rem = removed
        return func
    return decorator
