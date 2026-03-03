"""
Structured logging configuration
"""

import logging
import sys
from typing import Any


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output"""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """Get configured logger instance"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        # Use colored formatter in development
        from app.core.config import settings
        if settings.ENVIRONMENT == "development":
            formatter = ColoredFormatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%H:%M:%S",
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Set level from settings
        level = logging.DEBUG if settings.DEBUG else logging.INFO
        logger.setLevel(level)
    
    return logger