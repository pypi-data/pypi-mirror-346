import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Define log levels with their numeric values for reference
# DEBUG = 10 - Detailed information, typically of interest only when diagnosing problems
# INFO = 20 - Confirmation that things are working as expected
# WARNING = 30 - An indication that something unexpected happened, but the program still works
# ERROR = 40 - Due to a more serious problem, the program has not been able to perform a function
# CRITICAL = 50 - A serious error, indicating that the program itself may be unable to continue running

# Global logger instance
_logger = None


def get_logger(name: str = "orcastrator") -> logging.Logger:
    """Get the orcastrator logger instance.
    
    Args:
        name: Logger name, defaults to 'orcastrator'
        
    Returns:
        The configured logger instance
    """
    global _logger
    if _logger is not None:
        return _logger
        
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Default level
    
    # Prevent adding handlers multiple times
    if not logger.handlers:
        # Console handler (for standard output)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    _logger = logger
    return logger


def setup_file_logging(log_dir: Optional[Path] = None, log_level: int = logging.DEBUG) -> None:
    """Set up file logging with detailed output.
    
    Args:
        log_dir: Directory to store log files. If None, logs are stored in ./logs/
        log_level: Logging level for file output (default: DEBUG)
    """
    logger = get_logger()
    
    if log_dir is None:
        log_dir = Path("logs")
    
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f"orcastrator-{timestamp}.log"
    
    # File handler (for detailed logs)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_format = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_format)
    
    logger.addHandler(file_handler)
    logger.debug(f"File logging initialized: {log_file}")
    
    # Update the global log level if debug is enabled
    if log_level <= logging.DEBUG:
        logger.setLevel(log_level)


def set_log_level(level: int) -> None:
    """Set the log level for the orcastrator logger.
    
    Args:
        level: Logging level (use logging.DEBUG, logging.INFO, etc.)
    """
    logger = get_logger()
    logger.setLevel(level)
    
    # Update handler levels for console
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
            handler.setLevel(level)
            
    logger.debug(f"Log level set to: {level}")


def debug(msg: str, *args, **kwargs) -> None:
    """Log a debug message."""
    get_logger().debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    """Log an info message."""
    get_logger().info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    """Log a warning message."""
    get_logger().warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    """Log an error message."""
    get_logger().error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs) -> None:
    """Log a critical message."""
    get_logger().critical(msg, *args, **kwargs)


def exception(msg: str, *args, **kwargs) -> None:
    """Log an exception message with traceback."""
    get_logger().exception(msg, *args, **kwargs)