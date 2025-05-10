"""
Basic usage example for BrogsCursor.

This example demonstrates the simplest way to record and replay user interactions.
"""

import time
from brogscursor import record

def main():
    """Simple record and replay example."""
    print("BrogsCursor Basic Example")
    print("-------------------------")
    
    # Create a recorder instance
    recorder = record()
    
    print("\n1. Recording User Actions")
    print("Press Esc to stop recording or 'p' to pause/resume.")
    print("Starting in 3 seconds...")
    
    time.sleep(3)
    
    # Start recording
    recorder.start_recording()
    
    # Recording will continue until user presses Escape
    # The recorder.start_recording() function will block until recording is stopped
    
    # Get the recording file path
    recording_file = recorder.stop_recording()
    
    if recording_file:
        print(f"\n2. Recording saved to: {recording_file}")
        
        print("\n3. Replaying Recording")
        print("Press 'p' to stop replay.")
        print("Starting replay in 3 seconds...")
        
        time.sleep(3)
        
        # Replay the recording
        recorder.replay(recording_file)
    else:
        print("\nNo recording was created.")

if __name__ == "__main__":
    main()