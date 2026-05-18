"""Global hotkey manager for recording control"""

import logging
import threading
from typing import Optional, Callable

try:
    from pynput import keyboard
except ImportError:
    keyboard = None

logger = logging.getLogger(__name__)


class HotKeyManager:
    """Manages global hotkeys for recording control"""

    def __init__(self):
        """Initialize hotkey manager"""
        self.listener = None
        self.on_f2_callback = None
        self.on_f3_callback = None
        self._lock = threading.Lock()

    def register_hotkeys(self, on_f2: Optional[Callable] = None, on_f3: Optional[Callable] = None) -> None:
        """Register global hotkeys
        
        Args:
            on_f2: Callback function for F2 key press
            on_f3: Callback function for F3 key press
        """
        if keyboard is None:
            logger.error("pynput keyboard module not available")
            return

        self.on_f2_callback = on_f2
        self.on_f3_callback = on_f3

        # Start listener thread
        self.listener = keyboard.Listener(on_press=self._on_key_press)
        self.listener.start()
        logger.info("Global hotkey listener started")

    def unregister_hotkeys(self) -> None:
        """Unregister global hotkeys"""
        if self.listener:
            self.listener.stop()
            self.listener = None
            logger.info("Global hotkey listener stopped")

    def _on_key_press(self, key) -> None:
        """Handle global key press event
        
        Args:
            key: The key that was pressed
        """
        try:
            # Check for F2 key
            if key == keyboard.Key.f2:
                if self.on_f2_callback:
                    logger.debug("F2 hotkey pressed")
                    self.on_f2_callback()
            # Check for F3 key
            elif key == keyboard.Key.f3:
                if self.on_f3_callback:
                    logger.debug("F3 hotkey pressed")
                    self.on_f3_callback()
        except AttributeError:
            # Handle edge cases where key might not have expected attributes
            pass
        except Exception as e:
            logger.error(f"Error handling hotkey: {e}")

    def __del__(self):
        """Cleanup on object destruction"""
        try:
            self.unregister_hotkeys()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
