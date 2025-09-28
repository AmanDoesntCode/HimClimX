import logging

from .config import get_settings


def setup_logging() -> None:
    level = getattr(logging, get_settings().LOG_LEVEL.upper(), logging.INFO)
    # Keep it simple, let uvicorn handle access logs; we set root level here.
    logging.basicConfig(
        level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    # Quiet some noisy deps if needed
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
