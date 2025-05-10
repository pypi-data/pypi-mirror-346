#!/usr/bin/env python
"""
Batch Processing Script for BrogsCursor Recordings

This script allows you to:
1. Convert all recordings to CSV or TXT format
2. Merge multiple recordings into a single file
3. Run multiple recordings sequentially
4. Generate statistics about recordings

Usage:
    python -m scripts.batch_process [--option] [--args]
"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import List, Dict, Any
import time

# Add parent directory to path to import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brogscursor import record
from brogscursor.utils import get_recording_info, export_recording, merge_recordings


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Batch process BrogsCursor recordings")
    
    parser.add_argument(
        "--action", 
        required=True, 
        choices=["export", "merge", "run", "stats"], 
        help="Action to perform"
    )
    
    parser.add_argument(
        "--dir", 
        default=None, 
        help="Directory containing recordings (default: package recordings directory)"
    )
    
    parser.add_argument(
        "--format", 
        default="csv", 
        choices=["csv", "txt", "json"], 
        help="Export format (for --action=export)"
    )
    
    parser.add_argument(
        "--output", 
        default="exports", 
        help="Output directory for exports or merged file"
    )
    
    parser.add_argument(
        "--files", 
        default=None, 
        help="Comma-separated list of recording filenames to process"
    )
    
    parser.add_argument(
        "--speed", 
        type=float, 
        default=1.0, 
        help="Playback speed multiplier (for --action=run)"
    )
    
    parser.add_argument(
        "--delay", 
        type=int, 
        default=2, 
        help="Delay between recordings in seconds (for --action=run)"
    )
    
    return parser.parse_args()


def list_all_recordings(directory: str) -> List[str]:
    """List all recordings in a directory."""
    return [f for f in os.listdir(directory) if f.endswith('.json')]


def export_all_recordings(directory: str, output_dir: str, format_type: str) -> None:
    """Export all recordings to a specific format."""
    recordings = list_all_recordings(directory)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Exporting {len(recordings)} recordings to {format_type} format...")
    
    for i, recording in enumerate(recordings, 1):
        recording_path = os.path.join(directory, recording)
        base_name = os.path.basename(recording_path).replace(".json", "")
        output_path = os.path.join(output_dir, f"{base_name}.{format_type}")
        
        try:
            exported_path = export_recording(recording_path, format_type, output_path)
            print(f"[{i}/{len(recordings)}] Exported: {os.path.basename(exported_path)}")
        except Exception as e:
            print(f"[{i}/{len(recordings)}] Error exporting {recording}: {str(e)}")


def merge_selected_recordings(directory: str, filenames: List[str], output_dir: str) -> None:
    """Merge selected recordings into a single file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    recording_paths = [os.path.join(directory, f) for f in filenames]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"brogscursor_merged_{timestamp}.json")
    
    try:
        merged_path = merge_recordings(recording_paths, output_path)
        print(f"Successfully merged {len(filenames)} recordings to: {os.path.basename(merged_path)}")
    except Exception as e:
        print(f"Error merging recordings: {str(e)}")


def run_recordings_sequentially(directory: str, filenames: List[str], speed: float, delay: int) -> None:
    """Run multiple recordings one after another."""
    recorder = record(speed_multiplier=speed)
    
    print(f"Running {len(filenames)} recordings at {speed}x speed...")
    
    for i, filename in enumerate(filenames, 1):
        recording_path = os.path.join(directory, filename)
        
        if not os.path.exists(recording_path):
            print(f"[{i}/{len(filenames)}] Error: {filename} does not exist. Skipping.")
            continue
        
        print(f"[{i}/{len(filenames)}] Running: {filename}")
        print(f"Press 'p' to stop replay. Next recording starts in {delay} seconds after completion.")
        
        try:
            recorder.replay(recording_path)
            if i < len(filenames):
                print(f"Waiting {delay} seconds before next recording...")
                time.sleep(delay)
        except Exception as e:
            print(f"Error running {filename}: {str(e)}")


def generate_statistics(directory: str, filenames: List[str]) -> None:
    """Generate and display statistics about recordings."""
    all_stats = []
    
    for filename in filenames:
        recording_path = os.path.join(directory, filename)
        info = get_recording_info(recording_path)
        all_stats.append(info)
    
    # Sort by date and time
    all_stats.sort(key=lambda x: f"{x['date']} {x['time']}")
    
    # Calculate totals
    total_mouse_events = sum(stat['mouse_events'] for stat in all_stats)
    total_keyboard_events = sum(stat['keyboard_events'] for stat in all_stats)
    
    # Extract durations and convert to float
    durations = []
    for stat in all_stats:
        try:
            # Extract number from "X.XX seconds" format
            duration_str = stat['duration'].split()[0]
            durations.append(float(duration_str))
        except (ValueError, IndexError):
            continue
    
    total_duration = sum(durations)
    avg_duration = total_duration / len(durations) if durations else 0
    
    # Print summary statistics
    print("\n=== RECORDING STATISTICS ===")
    print(f"Total recordings: {len(all_stats)}")
    print(f"Total duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    print(f"Average duration: {avg_duration:.2f} seconds")
    print(f"Total mouse events: {total_mouse_events}")
    print(f"Total keyboard events: {total_keyboard_events}")
    print(f"Total events: {total_mouse_events + total_keyboard_events}")
    
    # Print table header
    print("\n{:<30} {:<20} {:<10} {:<10} {:<15}".format(
        "Recording", "Date & Time", "Mouse", "Keyboard", "Duration"
    ))
    print("-" * 85)
    
    # Print each recording's stats
    for stat in all_stats:
        print("{:<30} {:<20} {:<10} {:<10} {:<15}".format(
            stat['filename'][:30],
            f"{stat['date']} {stat['time']}",
            stat['mouse_events'],
            stat['keyboard_events'],
            stat['duration']
        ))


def main():
    """Main entry point."""
    args = parse_args()
    
    # Determine recordings directory
    if args.dir:
        directory = args.dir
    else:
        # Use default recordings directory from the package
        recorder = record()
        directory = recorder.log_dir
    
    # Get list of files to process
    if args.files:
        filenames = [f.strip() for f in args.files.split(",")]
    else:
        filenames = list_all_recordings(directory)
    
    if not filenames:
        print(f"No recordings found in {directory}")
        return
    
    print(f"Found {len(filenames)} recordings in {directory}")
    
    # Perform the selected action
    if args.action == "export":
        export_all_recordings(directory, args.output, args.format)
    elif args.action == "merge":
        merge_selected_recordings(directory, filenames, args.output)
    elif args.action == "run":
        run_recordings_sequentially(directory, filenames, args.speed, args.delay)
    elif args.action == "stats":
        generate_statistics(directory, filenames)


if __name__ == "__main__":
    main()