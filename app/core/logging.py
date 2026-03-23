"""Logging bootstrap utilities for the API service."""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Configure process-wide logging.

    TODO(phase1): emit JSON logs in production profile.
    """

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
