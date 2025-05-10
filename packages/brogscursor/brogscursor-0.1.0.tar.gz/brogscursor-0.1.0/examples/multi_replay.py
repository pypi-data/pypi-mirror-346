"""
Multiple recordings management example for BrogsCursor.

This example demonstrates how to work with multiple recordings,
list them, and replay a selected one.
"""

import os
from brogscursor import record
from brogscursor.utils import get_recording_info, merge_recordings

def main():
    """Multiple recordings example."""
    print("BrogsCursor Multiple Recordings Example")
    print("-------------------------------------")
    
    # Create a recorder
    recorder = record()
    
    # List available recordings
    recordings = recorder.list_recordings()
    
    if not recordings:
        print("\nNo recordings found. Please create some recordings first.")
        return
    
    print(f"\nFound {len(recordings)} recordings:")
    
    for i, recording in enumerate(recordings, 1):
        # Get recording details
        recording_path = os.path.join(recorder.log_dir, recording)
        info = get_recording_info(recording_path)
        
        print(f"\n{i}. {info['filename']}")
        print(f"   Date: {info['date']} at {info['time']}")
        print(f"   Events: {info['total_events']} ({info['mouse_events']} mouse, {info['keyboard_events']} keyboard)")
        print(f"   Duration: {info['duration']}")
    
    # Let user select a recording to replay
    try:
        selection = int(input("\nEnter recording number to replay (or 0 to merge recordings): "))
        
        if selection == 0:
            # Merge recordings example
            print("\nMerging Recordings Example")
            print("-------------------------")
            
            # Let user select recordings to merge
            print("Enter the numbers of recordings to merge (comma-separated):")
            merge_selections = input("> ").strip()
            merge_indices = [int(x.strip()) - 1 for x in merge_selections.split(",")]
            
            if all(0 <= i < len(recordings) for i in merge_indices):
                selected_paths = [os.path.join(recorder.log_dir, recordings[i]) for i in merge_indices]
                
                print(f"\nMerging {len(selected_paths)} recordings...")
                merged_path = merge_recordings(selected_paths)
                
                print(f"\nMerged recording saved to: {merged_path}")
                print("\nReplaying merged recording...")
                
                recorder.replay(merged_path)
            else:
                print("\nInvalid selection. Please enter valid recording numbers.")
        
        elif 1 <= selection <= len(recordings):
            selected_recording = recordings[selection - 1]
            recording_path = os.path.join(recorder.log_dir, selected_recording)
            
            print(f"\nSelected: {selected_recording}")
            
            # Ask for replay options
            print("\nReplay Options:")
            print("1. Normal speed")
            print("2. Fast (2x)")
            print("3. Slow (0.5x)")
            print("4. Loop 3 times")
            
            option = int(input("Select option (1-4): "))
            
            if option == 1:
                print("\nReplaying at normal speed...")
                recorder.speed_multiplier = 1.0
                recorder.replay(recording_path)
            elif option == 2:
                print("\nReplaying at 2x speed...")
                recorder.speed_multiplier = 2.0
                recorder.replay(recording_path)
            elif option == 3:
                print("\nReplaying at 0.5x speed...")
                recorder.speed_multiplier = 0.5
                recorder.replay(recording_path)
            elif option == 4:
                print("\nReplaying and looping 3 times...")
                recorder.speed_multiplier = 1.0
                recorder.replay(recording_path, loop_count=3)
            else:
                print("\nInvalid option. Using default settings.")
                recorder.replay(recording_path)
        else:
            print("\nInvalid selection.")
    
    except ValueError:
        print("\nInvalid input. Please enter a number.")

if __name__ == "__main__":
    main()