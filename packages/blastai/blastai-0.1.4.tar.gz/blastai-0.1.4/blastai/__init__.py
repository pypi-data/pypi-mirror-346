"""BLAST - Browser-LLM Auto-Scaling Technology"""

from .logging_setup import setup_logging
from .config import Settings

# Set up logging with default settings
setup_logging()

# Import everything else
from .engine import Engine
from .server import app, init_app_state
from .config import Settings, Constraints

__all__ = [
    'Engine',
    'app',
    'init_app_state',
    'Settings',
    'Constraints',
]