"""Main GUI window for Joe Auto Test"""

import sys
import logging
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem, QSlider,
    QSpinBox, QFileDialog, QMessageBox, QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from src.recorder import Recorder
from src.player import Player
from src.screenshot_matcher import ScreenshotMatcher
from src.script_manager import ScriptManager
from src import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        """Initialize main window"""
        super().__init__()
        self.setWindowTitle("Joe Auto Test - OS Automation Testing")
        self.setGeometry(100, 100, config.GUI_WINDOW_WIDTH, config.GUI_WINDOW_HEIGHT)

        # Initialize components
        self.recorder = Recorder()
        self.script_manager = ScriptManager()
        self.screenshot_matcher = ScreenshotMatcher(threshold=config.SIMILARITY_THRESHOLD)
        self.player = None

        # Setup UI
        self.setup_ui()
        self.load_scripts_list()

    def setup_ui(self) -> None:
        """Setup the user interface"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create tabs
        self.recording_tab = self.create_recording_tab()
        self.playback_tab = self.create_playback_tab()
        self.screenshot_tab = self.create_screenshot_tab()

        self.tabs.addTab(self.recording_tab, "Recording")
        self.tabs.addTab(self.playback_tab, "Playback")
        self.tabs.addTab(self.screenshot_tab, "Screenshot")

    def create_recording_tab(self) -> QWidget:
        """Create recording tab"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Recording Operations")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)

        # Script name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Script Name:"))
        self.recording_name_input = QLineEdit()
        self.recording_name_input.setPlaceholderText("Enter script name")
        name_layout.addWidget(self.recording_name_input)
        layout.addLayout(name_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_recording_btn = QPushButton("Start Recording")
        self.start_recording_btn.clicked.connect(self.start_recording)
        button_layout.addWidget(self.start_recording_btn)

        self.stop_recording_btn = QPushButton("Stop Recording")
        self.stop_recording_btn.clicked.connect(self.stop_recording)
        self.stop_recording_btn.setEnabled(False)
        button_layout.addWidget(self.stop_recording_btn)

        capture_screenshot_btn = QPushButton("Capture Screenshot")
        capture_screenshot_btn.clicked.connect(self.capture_screenshot)
        button_layout.addWidget(capture_screenshot_btn)

        layout.addLayout(button_layout)

        # Status
        self.recording_status = QLabel("Status: Ready")
        layout.addWidget(self.recording_status)

        # Log
        log_label = QLabel("Recording Log:")
        layout.addWidget(log_label)
        self.recording_log = QTextEdit()
        self.recording_log.setReadOnly(True)
        layout.addWidget(self.recording_log)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_playback_tab(self) -> QWidget:
        """Create playback tab"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Playback Recordings")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)

        # Scripts list
        list_label = QLabel("Available Scripts:")
        layout.addWidget(list_label)
        self.playback_scripts_list = QListWidget()
        self.playback_scripts_list.itemSelectionChanged.connect(self.on_script_selected)
        layout.addWidget(self.playback_scripts_list)

        # Speed control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Playback Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(5)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(10)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        speed_layout.addWidget(self.speed_slider)
        self.speed_label = QLabel("1.0x")
        speed_layout.addWidget(self.speed_label)
        self.speed_slider.sliderMoved.connect(self.update_speed_label)
        layout.addLayout(speed_layout)

        # Progress
        self.playback_progress = QProgressBar()
        layout.addWidget(self.playback_progress)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_playback_btn = QPushButton("Start Playback")
        self.start_playback_btn.clicked.connect(self.start_playback)
        button_layout.addWidget(self.start_playback_btn)

        self.pause_playback_btn = QPushButton("Pause")
        self.pause_playback_btn.clicked.connect(self.pause_playback)
        self.pause_playback_btn.setEnabled(False)
        button_layout.addWidget(self.pause_playback_btn)

        self.resume_playback_btn = QPushButton("Resume")
        self.resume_playback_btn.clicked.connect(self.resume_playback)
        self.resume_playback_btn.setEnabled(False)
        button_layout.addWidget(self.resume_playback_btn)

        self.stop_playback_btn = QPushButton("Stop")
        self.stop_playback_btn.clicked.connect(self.stop_playback)
        self.stop_playback_btn.setEnabled(False)
        button_layout.addWidget(self.stop_playback_btn)

        layout.addLayout(button_layout)

        # Refresh button
        refresh_btn = QPushButton("Refresh Scripts")
        refresh_btn.clicked.connect(self.load_scripts_list)
        layout.addWidget(refresh_btn)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_screenshot_tab(self) -> QWidget:
        """Create screenshot comparison tab"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Screenshot Comparison")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)

        # Buttons
        button_layout = QHBoxLayout()
        capture_btn = QPushButton("Capture Screenshot")
        capture_btn.clicked.connect(self.capture_screenshot)
        button_layout.addWidget(capture_btn)

        compare_btn = QPushButton("Compare Screenshots")
        compare_btn.clicked.connect(self.compare_screenshots)
        button_layout.addWidget(compare_btn)

        layout.addLayout(button_layout)

        # Comparison result
        result_label = QLabel("Comparison Result:")
        layout.addWidget(result_label)
        self.comparison_result = QTextEdit()
        self.comparison_result.setReadOnly(True)
        layout.addWidget(self.comparison_result)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def start_recording(self) -> None:
        """Start recording"""
        if not self.recording_name_input.text().strip():
            QMessageBox.warning(self, "Error", "Please enter a script name")
            return

        self.recorder.start()
        self.start_recording_btn.setEnabled(False)
        self.stop_recording_btn.setEnabled(True)
        self.recording_name_input.setEnabled(False)
        self.recording_status.setText("Status: Recording...")
        self.recording_log.append("[INFO] Recording started")
        logger.info("Recording started via GUI")

    def stop_recording(self) -> None:
        """Stop recording"""
        events = self.recorder.stop()
        script_name = self.recording_name_input.text().strip()

        if self.script_manager.save_script(script_name, events, "Recorded via GUI"):
            self.recording_status.setText(f"Status: Saved {len(events)} events")
            self.recording_log.append(f"[INFO] Recording stopped and saved ({len(events)} events)")
            QMessageBox.information(self, "Success", f"Script saved: {script_name}")
            self.load_scripts_list()
        else:
            self.recording_status.setText("Status: Error saving script")
            self.recording_log.append("[ERROR] Failed to save script")
            QMessageBox.critical(self, "Error", "Failed to save script")

        self.start_recording_btn.setEnabled(True)
        self.stop_recording_btn.setEnabled(False)
        self.recording_name_input.setEnabled(True)
        self.recording_name_input.clear()

    def capture_screenshot(self) -> None:
        """Capture a screenshot"""
        screenshot = self.screenshot_matcher.capture_screenshot()
        if screenshot is not None:
            filename = f"screenshot_{len(list(config.SCREENSHOTS_DIR.glob('*.png'))) + 1}.png"
            filepath = config.SCREENSHOTS_DIR / filename
            self.screenshot_matcher.save_screenshot(screenshot, str(filepath))
            QMessageBox.information(self, "Success", f"Screenshot saved: {filename}")
            self.recording_log.append(f"[INFO] Screenshot captured: {filename}")
        else:
            QMessageBox.critical(self, "Error", "Failed to capture screenshot")
            self.recording_log.append("[ERROR] Failed to capture screenshot")

    def load_scripts_list(self) -> None:
        """Load scripts list"""
        self.playback_scripts_list.clear()
        scripts = self.script_manager.list_scripts()
        for script in scripts:
            item = QListWidgetItem(f"{script['name']} ({script['event_count']} events)")
            item.setData(Qt.UserRole, script)
            self.playback_scripts_list.addItem(item)

    def on_script_selected(self) -> None:
        """Handle script selection"""
        pass

    def update_speed_label(self) -> None:
        """Update speed label"""
        speed = 0.5 + (self.speed_slider.value() - 5) * 0.1
        self.speed_label.setText(f"{speed:.1f}x")

    def start_playback(self) -> None:
        """Start playback"""
        selected_items = self.playback_scripts_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Please select a script")
            return

        script_data = selected_items[0].data(Qt.UserRole)
        events = script_data.get('events', [])

        if not events:
            QMessageBox.warning(self, "Error", "No events in script")
            return

        speed = 0.5 + (self.speed_slider.value() - 5) * 0.1
        self.player = Player(events)
        self.player.playback(speed=speed, progress_callback=self.update_playback_progress)

        self.start_playback_btn.setEnabled(False)
        self.pause_playback_btn.setEnabled(True)
        self.stop_playback_btn.setEnabled(True)
        self.playback_scripts_list.setEnabled(False)

    def pause_playback(self) -> None:
        """Pause playback"""
        if self.player:
            self.player.pause()
            self.pause_playback_btn.setEnabled(False)
            self.resume_playback_btn.setEnabled(True)

    def resume_playback(self) -> None:
        """Resume playback"""
        if self.player:
            self.player.resume()
            self.pause_playback_btn.setEnabled(True)
            self.resume_playback_btn.setEnabled(False)

    def stop_playback(self) -> None:
        """Stop playback"""
        if self.player:
            self.player.stop()
        self.playback_progress.setValue(0)
        self.start_playback_btn.setEnabled(True)
        self.pause_playback_btn.setEnabled(False)
        self.resume_playback_btn.setEnabled(False)
        self.stop_playback_btn.setEnabled(False)
        self.playback_scripts_list.setEnabled(True)

    def update_playback_progress(self, progress: float, current: int, total: int) -> None:
        """Update playback progress"""
        self.playback_progress.setValue(int(progress))

    def compare_screenshots(self) -> None:
        """Compare two screenshots"""
        files = QFileDialog.getOpenFileNames(self, "Select two screenshots", str(config.SCREENSHOTS_DIR), "Images (*.png *.jpg)")
        if len(files[0]) >= 2:
            img1 = self.screenshot_matcher.load_screenshot(files[0][0])
            img2 = self.screenshot_matcher.load_screenshot(files[0][1])
            similarity = self.screenshot_matcher.compare(img1, img2)
            self.comparison_result.setText(f"Similarity: {similarity:.2%}")
        else:
            QMessageBox.warning(self, "Error", "Please select exactly 2 screenshots")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
