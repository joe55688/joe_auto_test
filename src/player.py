"""Module for playing back recorded operations"""

import json
import logging
import threading
import time
from typing import List, Dict, Any, Callable, Optional

from pynput import keyboard, mouse

logger = logging.getLogger(__name__)


class Player:
    """Plays back recorded keyboard and mouse operations"""

    def __init__(self, events: List[Dict[str, Any]]):
        """Initialize the player with events
        
        Args:
            events: List of recorded events
        """
        self.events = events
        self.is_playing = False
        self.is_paused = False
        self.speed = 1.0
        self.current_index = 0
        self.controller_keyboard = keyboard.Controller()
        self.controller_mouse = mouse.Controller()
        self.playback_thread = None
        self.progress_callback = None

    def playback(self, speed: float = 1.0, progress_callback: Optional[Callable] = None) -> None:
        """Start playback in a separate thread
        
        Args:
            speed: Playback speed multiplier (0.5 - 2.0)
            progress_callback: Function to call with progress updates
        """
        if self.is_playing:
            logger.warning("Playback already in progress")
            return

        if not self.events:
            logger.warning("No events to play back")
            return

        self.speed = max(0.5, min(2.0, speed))
        self.progress_callback = progress_callback
        self.is_playing = True
        self.is_paused = False
        self.current_index = 0

        self.playback_thread = threading.Thread(target=self._playback_thread)
        self.playback_thread.daemon = True
        self.playback_thread.start()

        logger.info(f"Playback started with speed {self.speed}x")

    def pause(self) -> None:
        """Pause playback"""
        self.is_paused = True
        logger.info("Playback paused")

    def resume(self) -> None:
        """Resume playback"""
        self.is_paused = False
        logger.info("Playback resumed")

    def stop(self) -> None:
        """Stop playback"""
        self.is_playing = False
        logger.info("Playback stopped")

    def set_speed(self, speed: float) -> None:
        """Set playback speed
        
        Args:
            speed: Speed multiplier (0.5 - 2.0)
        """
        self.speed = max(0.5, min(2.0, speed))
        logger.info(f"Playback speed set to {self.speed}x")

    def _playback_thread(self) -> None:
        """Thread function for playback"""
        try:
            start_time = time.time()

            for i, event in enumerate(self.events):
                if not self.is_playing:
                    break

                # Handle pause
                while self.is_paused and self.is_playing:
                    time.sleep(0.1)

                if not self.is_playing:
                    break

                # Calculate wait time
                event_time = event['timestamp']
                if i > 0:
                    prev_event = self.events[i - 1]
                    event_time = (event['timestamp'] - prev_event['timestamp']) / self.speed
                else:
                    event_time = event['timestamp'] / self.speed

                time.sleep(event_time)

                # Execute event
                self._execute_event(event)
                self.current_index = i + 1

                # Call progress callback
                if self.progress_callback:
                    progress = (i + 1) / len(self.events) * 100
                    self.progress_callback(progress, i + 1, len(self.events))

            logger.info("Playback completed")
            self.is_playing = False

        except Exception as e:
            logger.error(f"Error during playback: {e}")
            self.is_playing = False

    def _execute_event(self, event: Dict[str, Any]) -> None:
        """Execute a single recorded event
        
        Args:
            event: The event to execute
        """
        try:
            event_type = event['type']

            if event_type == 'key_press':
                self._execute_key_press(event)
            elif event_type == 'key_release':
                self._execute_key_release(event)
            elif event_type == 'mouse_move':
                self._execute_mouse_move(event)
            elif event_type == 'mouse_click':
                self._execute_mouse_click(event)
            elif event_type == 'mouse_scroll':
                self._execute_mouse_scroll(event)
            else:
                logger.warning(f"Unknown event type: {event_type}")

        except Exception as e:
            logger.error(f"Error executing event: {e}")

    def _execute_key_press(self, event: Dict[str, Any]) -> None:
        """Execute key press"""
        try:
            key_str = event['key'].strip("'")
            if key_str.startswith('Key.'):
                key_name = key_str.split('.')[-1]
                key = getattr(keyboard.Key, key_name)
            else:
                key = key_str[0] if len(key_str) > 0 else ' '
            self.controller_keyboard.press(key)
        except Exception as e:
            logger.debug(f"Could not press key {event['key']}: {e}")

    def _execute_key_release(self, event: Dict[str, Any]) -> None:
        """Execute key release"""
        try:
            key_str = event['key'].strip("'")
            if key_str.startswith('Key.'):
                key_name = key_str.split('.')[-1]
                key = getattr(keyboard.Key, key_name)
            else:
                key = key_str[0] if len(key_str) > 0 else ' '
            self.controller_keyboard.release(key)
        except Exception as e:
            logger.debug(f"Could not release key {event['key']}: {e}")

    def _execute_mouse_move(self, event: Dict[str, Any]) -> None:
        """Execute mouse move"""
        self.controller_mouse.position = (event['x'], event['y'])

    def _execute_mouse_click(self, event: Dict[str, Any]) -> None:
        """Execute mouse click"""
        self.controller_mouse.position = (event['x'], event['y'])
        if event['pressed']:
            self.controller_mouse.press(mouse.Button.left)
        else:
            self.controller_mouse.release(mouse.Button.left)

    def _execute_mouse_scroll(self, event: Dict[str, Any]) -> None:
        """Execute mouse scroll"""
        self.controller_mouse.scroll(event['dx'], event['dy'])
