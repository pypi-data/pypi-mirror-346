"""
Custom settings example for BrogsCursor.

This example demonstrates how to customize recording and replay settings.
"""

import os
import time
from brogscursor import record

def main():
    """Custom settings example."""
    print("BrogsCursor Custom Settings Example")
    print("---------------------------------")
    
    # Create a custom recordings directory
    custom_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_recordings")
    if not os.path.exists(custom_dir):
        os.makedirs(custom_dir)
    
    # Create a recorder with custom settings
    recorder = record(
        log_dir=custom_dir,        # Custom directory for saving recordings
        max_events=10000,          # Maximum number of events to record
        record_keyboard=True,      # Record keyboard events
        speed_multiplier=2.0       # Default playback speed (2x faster)
    )
    
    print(f"\nCustom Settings:")
    print(f"- Recordings will be saved to: {custom_dir}")
    print(f"- Max events: {recorder.max_events}")
    print(f"- Record keyboard: {recorder.record_keyboard}")
    print(f"- Default replay speed: {recorder.speed_multiplier}x")
    
    print("\n1. Recording with Timeout")
    print("Recording will automatically stop after 10 seconds.")
    print("Press Esc to stop early or 'p' to pause/resume.")
    print("Starting in 3 seconds...")
    
    time.sleep(3)
    
    # Start a background thread for recording with timeout
    import threading
    recording_thread = threading.Thread(target=recorder.start_recording, args=(10,))
    recording_thread.start()
    recording_thread.join()
    
    # Get the recording file path
    recording_file = recorder.stop_recording()
    
    if recording_file:
        print(f"\n2. Recording saved to: {recording_file}")
        
        print("\n3. Replaying with Custom Settings")
        print("Press 'p' to stop replay.")
        print("Starting replay in 3 seconds...")
        
        time.sleep(3)
        
        # Replay with custom settings
        recorder.replay(
            recording_file,
            precision_mode=True,       # Maintain exact timing
            filter_events=None,        # No events filtered out
            loop_count=2,              # Loop twice
            stop_key='s'               # Use 's' key to stop instead of 'p'
        )
    else:
        print("\nNo recording was created.")

if __name__ == "__main__":
    main()