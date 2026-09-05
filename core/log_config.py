# -*- coding: utf-8 -*-
"""Unified logging configuration for the power_topology_verify project.

All modules should use:
    from core.log_config import get_logger
    logger = get_logger(__name__)

Instead of bare `print()` or `logging.basicConfig()` scattered across files.
"""
import logging
import os
import sys
from config.settings import OUTPUT_LOG

_INITIALIZED = False


def _init_root_logger():
    global _INITIALIZED
    if _INITIALIZED:
        return
    _INITIALIZED = True

    os.makedirs(OUTPUT_LOG, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        os.path.join(OUTPUT_LOG, "topology_verify.log"),
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    # Avoid duplicate handlers on re-init
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the project's unified configuration."""
    _init_root_logger()
    return logging.getLogger(name)
