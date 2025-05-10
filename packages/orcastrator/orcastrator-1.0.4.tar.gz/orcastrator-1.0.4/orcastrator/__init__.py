"""Orcastrator - A tool for orchestrating ORCA quantum chemistry calculations"""

import logging
import os
from pathlib import Path

from orcastrator.logger import get_logger, setup_file_logging
from orcastrator.stats import MoleculeStats, PipelineStats, StepStats, Timer

__version__ = "1.0.4"
__all__ = ["MoleculeStats", "PipelineStats", "StepStats", "Timer"]

# Initialize the default logger
logger = get_logger()

# Set up file logging if environment variable is set
if os.environ.get("ORCASTRATOR_DEBUG") == "1":
    log_dir = os.environ.get("ORCASTRATOR_LOG_DIR")
    log_dir = Path(log_dir) if log_dir else None
    setup_file_logging(log_dir=log_dir, log_level=logging.DEBUG)
