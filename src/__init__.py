"""Joe Auto Test - OS Automation Testing Framework"""

__version__ = "1.0.0"
__author__ = "joe55688"

from .recorder import Recorder
from .player import Player
from .screenshot_matcher import ScreenshotMatcher
from .script_manager import ScriptManager

__all__ = [
    'Recorder',
    'Player',
    'ScreenshotMatcher',
    'ScriptManager',
]
