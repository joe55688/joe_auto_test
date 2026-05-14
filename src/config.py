"""Configuration settings for Joe Auto Test"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Create directories if they don't exist
SCRIPTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Recording settings
RECORDING_FRAME_RATE = 30  # frames per second

# Playback settings
MIN_PLAYBACK_SPEED = 0.5
MAX_PLAYBACK_SPEED = 2.0
DEFAULT_PLAYBACK_SPEED = 1.0

# Screenshot comparison settings
SIMILARITY_THRESHOLD = 0.85  # 0-1 range
MIN_MATCH_PERCENT = 70  # percentage

# GUI settings
GUI_WINDOW_WIDTH = 1200
GUI_WINDOW_HEIGHT = 800
GUI_THEME = "fusion"  # or "Windows", "Macintosh"

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# File formats
SCRIPT_EXTENSION = ".json"
SCREENSHOT_EXTENSION = ".png"
