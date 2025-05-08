from .hivetrace import (
    HivetraceSDK,
    InvalidParameterError,
    MissingConfigError,
    UnauthorizedError,
)

try:
    from .crewai_adapter import CrewAIAdapter, track_crew

    __all__ = [
        "HivetraceSDK",
        "InvalidParameterError",
        "MissingConfigError",
        "UnauthorizedError",
        "CrewAIAdapter",
        "track_crew",
    ]
except ImportError:
    __all__ = [
        "HivetraceSDK",
        "InvalidParameterError",
        "MissingConfigError",
        "UnauthorizedError",
    ]
