"""Module for recording keyboard and mouse operations"""

import json
import logging
import threading
from datetime import datetime
from typing import List, Dict, Any

from pynput import keyboard, mouse

logger = logging.getLogger(__name__)


class Recorder:
    """Records keyboard and mouse operations with timestamps"""

    def __init__(self):
        """Initialize the recorder"""
        self.events = []
        self.is_recording = False
        self.start_time = None
        self.listener = None
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start recording operations"""
        if self.is_recording:
            logger.warning("Recording already in progress")
            return

        self.events = []
        self.is_recording = True
        self.start_time = datetime.now()

        # Start keyboard listener
        self.kb_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.kb_listener.start()

        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll
        )
        self.mouse_listener.start()

        logger.info("Recording started")

    def stop(self) -> List[Dict[str, Any]]:
        """Stop recording and return events"""
        if not self.is_recording:
            logger.warning("No recording in progress")
            return []

        self.is_recording = False

        # Stop listeners
        if hasattr(self, 'kb_listener'):
            self.kb_listener.stop()
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()

        logger.info(f"Recording stopped. Captured {len(self.events)} events")
        return self.events

    def get_events(self) -> List[Dict[str, Any]]:
        """Get recorded events"""
        with self._lock:
            return self.events.copy()

    def clear_events(self) -> None:
        """Clear all recorded events"""
        with self._lock:
            self.events = []
        logger.info("Events cleared")

    def _on_key_press(self, key) -> None:
        """Handle key press event"""
        if not self.is_recording:
            return

        try:
            timestamp = (datetime.now() - self.start_time).total_seconds()
            event = {
                'type': 'key_press',
                'key': str(key),
                'timestamp': timestamp
            }
            with self._lock:
                self.events.append(event)
            logger.debug(f"Key pressed: {key} at {timestamp:.2f}s")
        except Exception as e:
            logger.error(f"Error recording key press: {e}")

    def _on_key_release(self, key) -> None:
        """Handle key release event"""
        if not self.is_recording:
            return

        try:
            timestamp = (datetime.now() - self.start_time).total_seconds()
            event = {
                'type': 'key_release',
                'key': str(key),
                'timestamp': timestamp
            }
            with self._lock:
                self.events.append(event)
            logger.debug(f"Key released: {key} at {timestamp:.2f}s")
        except Exception as e:
            logger.error(f"Error recording key release: {e}")

    def _on_mouse_move(self, x: int, y: int) -> None:
        """Handle mouse move event"""
        if not self.is_recording:
            return

        try:
            timestamp = (datetime.now() - self.start_time).total_seconds()
            event = {
                'type': 'mouse_move',
                'x': x,
                'y': y,
                'timestamp': timestamp
            }
            with self._lock:
                self.events.append(event)
            logger.debug(f"Mouse moved to ({x}, {y}) at {timestamp:.2f}s")
        except Exception as e:
            logger.error(f"Error recording mouse move: {e}")

    def _on_mouse_click(self, x: int, y: int, button, pressed: bool) -> None:
        """Handle mouse click event"""
        if not self.is_recording:
            return

        try:
            timestamp = (datetime.now() - self.start_time).total_seconds()
            event = {
                'type': 'mouse_click',
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed,
                'timestamp': timestamp
            }
            with self._lock:
                self.events.append(event)
            action = "pressed" if pressed else "released"
            logger.debug(f"Mouse {action} at ({x}, {y}) at {timestamp:.2f}s")
        except Exception as e:
            logger.error(f"Error recording mouse click: {e}")

    def _on_mouse_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handle mouse scroll event"""
        if not self.is_recording:
            return

        try:
            timestamp = (datetime.now() - self.start_time).total_seconds()
            event = {
                'type': 'mouse_scroll',
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'timestamp': timestamp
            }
            with self._lock:
                self.events.append(event)
            logger.debug(f"Mouse scrolled at ({x}, {y}) at {timestamp:.2f}s")
        except Exception as e:
            logger.error(f"Error recording mouse scroll: {e}")
