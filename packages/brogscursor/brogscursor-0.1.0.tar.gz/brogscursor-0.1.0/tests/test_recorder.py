"""
Tests for the BrogsCursorRecorder class.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import json

from brogscursor import record
from brogscursor.recorder import BrogsCursorRecorder


class TestBrogsCursorRecorder(unittest.TestCase):
    """Tests for the BrogsCursorRecorder class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for test recordings
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = BrogsCursorRecorder(log_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up the test environment."""
        # Remove all files in the temporary directory
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        # Remove the temporary directory
        os.rmdir(self.temp_dir)
    
    def test_init(self):
        """Test initialization of the recorder."""
        # Check default values
        self.assertEqual(self.recorder.log_dir, self.temp_dir)
        self.assertEqual(self.recorder.max_events, 50000)
        self.assertTrue(self.recorder.record_keyboard)
        self.assertEqual(self.recorder.speed_multiplier, 1.0)
        self.assertFalse(self.recorder.recording)
        self.assertFalse(self.recorder.paused)
        self.assertFalse(self.recorder.stop_replay)
        self.assertEqual(self.recorder.mouse_events, [])
        self.assertEqual(self.recorder.keyboard_events, [])
        
        # Check custom values
        custom_recorder = BrogsCursorRecorder(
            log_dir=self.temp_dir,
            max_events=10000,
            record_keyboard=False,
            speed_multiplier=2.0
        )
        self.assertEqual(custom_recorder.log_dir, self.temp_dir)
        self.assertEqual(custom_recorder.max_events, 10000)
        self.assertFalse(custom_recorder.record_keyboard)
        self.assertEqual(custom_recorder.speed_multiplier, 2.0)
    
    def test_generate_log_filename(self):
        """Test generation of log filenames."""
        filename = self.recorder._generate_log_filename()
        
        # Check that the file is in the right directory
        self.assertTrue(filename.startswith(self.temp_dir))
        
        # Check that the filename has the correct format
        basename = os.path.basename(filename)
        self.assertTrue(basename.startswith("brogscursor_recording_"))
        self.assertTrue(basename.endswith(".json"))
        
        # Check that the timestamp has the right format (20 chars for timestamp)
        timestamp = basename.replace("brogscursor_recording_", "").replace(".json", "")
        self.assertEqual(len(timestamp), 15)  # YYYYmmdd_HHMMSS
    
    @patch('time.time', return_value=12345.0)
    def test_on_move(self, mock_time):
        """Test recording of mouse move events."""
        # Set recorder to recording mode
        self.recorder.recording = True
        self.recorder.start_time = 12340.0
        
        # Mock mouse move event
        self.recorder.on_move(100, 200)
        
        # Check that the event was recorded
        self.assertEqual(len(self.recorder.mouse_events), 1)
        event = self.recorder.mouse_events[0]
        self.assertEqual(event['type'], 'move')
        self.assertEqual(event['pos'], (100, 200))
        self.assertEqual(event['relative_time'], 5.0)  # 12345 - 12340
    
    @patch('time.time', return_value=12345.0)
    def test_on_click(self, mock_time):
        """Test recording of mouse click events."""
        # Set recorder to recording mode
        self.recorder.recording = True
        self.recorder.start_time = 12340.0
        
        # Mock mouse click event
        self.recorder.on_click(100, 200, "Button.left", True)
        
        # Check that the event was recorded
        self.assertEqual(len(self.recorder.mouse_events), 1)
        event = self.recorder.mouse_events[0]
        self.assertEqual(event['type'], 'click')
        self.assertEqual(event['pos'], (100, 200))
        self.assertEqual(event['button'], "Button.left")
        self.assertEqual(event['pressed'], True)
        self.assertEqual(event['relative_time'], 5.0)  # 12345 - 12340
    
    def test_stop_recording(self):
        """Test stopping recording and saving events."""
        # Add some mock events
        self.recorder.recording = True
        self.recorder.mouse_events = [
            {'type': 'move', 'pos': (100, 200), 'relative_time': 1.0, 'screen_resolution': (1920, 1080)},
            {'type': 'click', 'pos': (100, 200), 'button': 'Button.left', 'pressed': True, 'relative_time': 2.0, 'screen_resolution': (1920, 1080)}
        ]
        self.recorder.keyboard_events = [
            {'type': 'keypress', 'key': 'a', 'relative_time': 1.5}
        ]
        
        # Stop recording
        log_file = self.recorder.stop_recording()
        
        # Check that recording has stopped
        self.assertFalse(self.recorder.recording)
        
        # Check that the log file exists
        self.assertTrue(os.path.exists(log_file))
        
        # Check that the log file has the correct content
        with open(log_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data['mouse_events']), 2)
        self.assertEqual(len(data['keyboard_events']), 1)
        self.assertEqual(data['metadata']['total_mouse_events'], 2)
        self.assertEqual(data['metadata']['total_keyboard_events'], 1)
        self.assertEqual(data['metadata']['total_recording_time'], 2.0)
    
    def test_list_recordings(self):
        """Test listing of recordings."""
        # Create some mock recording files
        filenames = [
            "brogscursor_recording_20250101_120000.json",
            "brogscursor_recording_20250101_120100.json",
            "brogscursor_recording_20250101_120200.json"
        ]
        
        for filename in filenames:
            with open(os.path.join(self.temp_dir, filename), 'w') as f:
                f.write("{}")
        
        # List recordings
        recordings = self.recorder.list_recordings()
        
        # Check that all recordings are listed
        self.assertEqual(len(recordings), 3)
        for filename in filenames:
            self.assertIn(filename, recordings)


if __name__ == '__main__':
    unittest.main()