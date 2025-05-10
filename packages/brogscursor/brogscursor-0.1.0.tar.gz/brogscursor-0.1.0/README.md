# BrogsCursor

[![PyPI version](https://img.shields.io/pypi/v/brogscursor.svg)](https://pypi.org/project/brogscursor/)
[![Python versions](https://img.shields.io/pypi/pyversions/brogscursor.svg)](https://pypi.org/project/brogscursor/)
[![License](https://img.shields.io/github/license/yourusername/brogscursor.svg)](https://github.com/yourusername/brogscursor/blob/main/LICENSE)

A precise mouse and keyboard action recorder and replayer for Python.

BrogsCursor allows you to record user interactions with high fidelity and replay them exactly as they were performed. Perfect for automation, testing, and demonstrations.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage](#usage)
  - [Basic Recording](#basic-recording)
  - [Replay Options](#replay-options)
  - [Command-Line Interface](#command-line-interface)
  - [Customizing Settings](#customizing-settings)
- [Examples](#examples)
- [API Reference](#api-reference)
- [License](#license)

## Installation

Install the latest stable version from PyPI:

```bash
pip install brogscursor
```

When using this package in your application, it's recommended to pin to at least the major version:

```bash
pip install brogscursor==0.1.*
```

## Quick Start

Record and replay user actions in just 4 lines of code:

```python
from brogscursor import record

recorder = record()
recorder.start_recording()  # Press Esc to stop recording
recorder.replay(recorder.stop_recording())
```

Or use the command-line interface:

```bash
# Launch the interactive CLI
brogscursor
```

## Features

- 🎯 **Precise Recording**: Capture mouse movements, clicks, scrolls, and keyboard events with high precision
- ⏱️ **Exact Timing**: Replay actions with the same timing as the original recording
- ⚙️ **Customizable**: Adjust playback speed, loop count, and more
- 🛑 **Control**: Pause/resume recording, stop replay with a hotkey
- 🖥️ **Resolution Aware**: Automatically scales recorded actions to the current screen resolution
- 📊 **Rich CLI**: Beautiful terminal interface with the Rich library
- 🔄 **Multi-format Export**: Save recordings as JSON, CSV, or human-readable text
- 📝 **Robust API**: Comprehensive Python API for integration into your projects

## Usage

### Basic Recording

```python
from brogscursor import record

# Create a recorder instance
recorder = record()

# Start recording (this will block until Escape is pressed)
recorder.start_recording()

# Save the recording
recording_file = recorder.stop_recording()
print(f"Recording saved to: {recording_file}")
```

### Replay Options

```python
from brogscursor import record

recorder = record()

# Replay with default settings
recorder.replay("path/to/recording.json")

# Customize replay
recorder.replay(
    "path/to/recording.json",
    precision_mode=True,       # Maintain exact timing
    filter_events=["scroll"],  # Skip scroll events
    loop_count=3,              # Repeat 3 times
    stop_key='s'               # Use 's' to stop instead of 'p'
)

# Change playback speed
recorder.speed_multiplier = 2.0  # 2x faster
recorder.replay("path/to/recording.json")
```

### Command-Line Interface

The package includes a command-line interface for easy use:

```bash
# Launch the interactive CLI
brogscursor
```

CLI Features:
- Start recording with optional timeout
- List and manage saved recordings
- Replay recordings with various settings
- Customize configuration

### Customizing Settings

```python
from brogscursor import record

# Create a recorder with custom settings
recorder = record(
    log_dir="my_recordings",   # Custom directory to save recordings
    max_events=10000,          # Maximum number of events to record
    record_keyboard=True,      # Record keyboard events
    speed_multiplier=1.5       # Default replay speed
)

# Start recording with a 30-second timeout
recorder.start_recording(timeout=30)
```

## Examples

Several example scripts are included to demonstrate the package's functionality:

- `examples/basic_usage.py`: Simple recording and replay
- `examples/custom_settings.py`: Using custom settings
- `examples/multi_replay.py`: Working with multiple recordings
- `examples/save_recordings.py`: Exporting recordings to different formats

## API Reference

### `BrogsCursorRecorder`

Main class for recording and replaying user actions.

#### Constructor

```python
recorder = BrogsCursorRecorder(
    log_dir=None,              # Directory to store recordings
    max_events=50000,          # Maximum events to record
    record_keyboard=True,      # Whether to record keyboard events
    speed_multiplier=1.0       # Default replay speed
)
```

#### Methods

- `start_recording(timeout=None)`: Start recording user actions
- `stop_recording()`: Stop recording and save to file
- `pause_recording()`: Pause ongoing recording
- `resume_recording()`: Resume paused recording
- `list_recordings()`: List all saved recordings
- `replay(recording_file, precision_mode=True, filter_events=None, loop_count=1, stop_key='p')`: Replay a recording

### Utility Functions

- `get_recording_info(recording_path)`: Get information about a recording
- `export_recording(recording_path, export_format, output_path)`: Export to different formats
- `merge_recordings(recording_paths, output_path)`: Merge multiple recordings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.