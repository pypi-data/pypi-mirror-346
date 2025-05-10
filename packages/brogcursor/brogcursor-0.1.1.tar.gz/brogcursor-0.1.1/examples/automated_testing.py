"""
Automated Testing Example for BrogsCursor.

This example demonstrates how to use BrogsCursor for automated UI testing.
It records a sequence of actions, then plays them back to test a UI component.
"""

import os
import time
import tkinter as tk
from tkinter import ttk
import threading
from brogscursor import record

class TestApplication:
    """
    A simple application to demonstrate automated UI testing.
    
    This class creates a simple GUI with a counter that can be
    incremented and decremented using buttons. It also includes
    a reset button.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.root.title("BrogsCursor Test Application")
        self.root.geometry("400x300")
        
        self.count = 0
        self.expected_count = 0  # For testing
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create counter display
        self.count_var = tk.StringVar(value="0")
        ttk.Label(main_frame, text="Counter:", font=("Arial", 14)).pack(pady=10)
        ttk.Label(main_frame, textvariable=self.count_var, font=("Arial", 24, "bold")).pack(pady=10)
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Create buttons
        ttk.Button(button_frame, text="Decrement", command=self.decrement).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Increment", command=self.increment).pack(side=tk.LEFT, padx=10)
        
        # Create test status display
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 12))
        self.status_label.pack(pady=20)
    
    def increment(self):
        """Increment the counter."""
        self.count += 1
        self.count_var.set(str(self.count))
    
    def decrement(self):
        """Decrement the counter."""
        self.count -= 1
        self.count_var.set(str(self.count))
    
    def reset(self):
        """Reset the counter to zero."""
        self.count = 0
        self.count_var.set("0")
    
    def verify_count(self, expected):
        """Verify that the counter matches the expected value."""
        if self.count == expected:
            self.status_var.set(f"Test PASSED! Count: {self.count}, Expected: {expected}")
            self.status_label.config(foreground="green")
        else:
            self.status_var.set(f"Test FAILED! Count: {self.count}, Expected: {expected}")
            self.status_label.config(foreground="red")
    
    def run(self):
        """Run the application."""
        self.root.mainloop()
    
    def schedule_verification(self, expected, delay=2):
        """Schedule verification after a delay."""
        self.expected_count = expected
        self.status_var.set("Testing in progress...")
        self.status_label.config(foreground="blue")
        
        def verify_after_delay():
            time.sleep(delay)
            self.verify_count(expected)
        
        threading.Thread(target=verify_after_delay, daemon=True).start()
    
    def close(self):
        """Close the application."""
        self.root.destroy()


def record_test_sequence():
    """
    Record a test sequence for the application.
    
    This function:
    1. Launches the test application
    2. Records a sequence of button clicks
    3. Saves the recording for later use
    
    Returns:
        str: Path to the saved recording
    """
    print("Recording a test sequence...")
    
    # Create a recorder
    recorder = record()
    
    # Start the application in a separate thread
    app = TestApplication()
    app_thread = threading.Thread(target=app.run)
    app_thread.daemon = True
    app_thread.start()
    
    # Wait for the application to start
    time.sleep(1)
    
    print("\nPlease perform these actions:")
    print("1. Click 'Increment' three times")
    print("2. Click 'Decrement' once")
    print("3. Press Esc when done to stop recording")
    
    # Start recording
    recorder.start_recording()
    
    # Stop the application when recording is done
    app.close()
    
    # Save the recording
    recording_file = recorder.stop_recording()
    print(f"\nTest sequence recorded to: {recording_file}")
    
    return recording_file


def run_automated_test(recording_file):
    """
    Run an automated test using a recorded sequence.
    
    This function:
    1. Launches the test application
    2. Replays the recorded sequence
    3. Verifies the counter value matches the expected result
    
    Args:
        recording_file (str): Path to the recording file
    """
    print("\nRunning automated test...")
    
    # Create a recorder
    recorder = record()
    
    # Start the application in a separate thread
    app = TestApplication()
    app_thread = threading.Thread(target=app.run)
    app_thread.daemon = True
    app_thread.start()
    
    # Wait for the application to start
    time.sleep(1)
    
    # Schedule verification after replay
    # The expected count is 2 (3 increments - 1 decrement)
    app.schedule_verification(2, delay=5)
    
    # Replay the recording
    recorder.replay(recording_file)
    
    # Keep the application running for a few seconds to show the result
    time.sleep(5)
    
    # Close the application
    app.close()


def main():
    """Main entry point for the example."""
    print("BrogsCursor Automated Testing Example")
    print("====================================")
    
    # Ask if the user wants to record a new sequence or use an existing one
    use_existing = input("\nUse existing recording? (y/n): ").lower() == 'y'
    
    if use_existing:
        # List recordings directory
        recorder = record()
        recordings = recorder.list_recordings()
        
        if not recordings:
            print("No recordings found. Creating a new recording.")
            recording_file = record_test_sequence()
        else:
            print("\nAvailable recordings:")
            for i, recording in enumerate(recordings, 1):
                print(f"{i}. {recording}")
            
            try:
                selection = int(input("\nSelect recording number: ")) - 1
                if 0 <= selection < len(recordings):
                    recording_file = os.path.join(recorder.log_dir, recordings[selection])
                else:
                    print("Invalid selection. Creating a new recording.")
                    recording_file = record_test_sequence()
            except ValueError:
                print("Invalid input. Creating a new recording.")
                recording_file = record_test_sequence()
    else:
        recording_file = record_test_sequence()
    
    # Run the automated test
    run_automated_test(recording_file)
    
    print("\nTest completed!")


if __name__ == "__main__":
    main()