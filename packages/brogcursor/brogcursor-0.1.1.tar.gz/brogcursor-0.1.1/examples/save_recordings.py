"""
Export recordings example for BrogsCursor.

This example demonstrates how to export recordings to different formats.
"""

import os
from brogscursor import record
from brogscursor.utils import export_recording

def main():
    """Export recordings to different formats."""
    print("BrogsCursor Export Recordings Example")
    print("-----------------------------------")
    
    # Create a recorder
    recorder = record()
    
    # List available recordings
    recordings = recorder.list_recordings()
    
    if not recordings:
        print("\nNo recordings found. Please create some recordings first.")
        return
    
    print(f"\nFound {len(recordings)} recordings:")
    
    for i, recording in enumerate(recordings, 1):
        print(f"{i}. {recording}")
    
    # Let user select a recording to export
    try:
        selection = int(input("\nEnter recording number to export: "))
        
        if 1 <= selection <= len(recordings):
            selected_recording = recordings[selection - 1]
            recording_path = os.path.join(recorder.log_dir, selected_recording)
            
            print(f"\nSelected: {selected_recording}")
            
            # Ask for export format
            print("\nExport Format:")
            print("1. JSON (default)")
            print("2. CSV")
            print("3. TXT (human-readable)")
            
            format_option = int(input("Select format (1-3): "))
            
            export_format = "json"
            if format_option == 2:
                export_format = "csv"
            elif format_option == 3:
                export_format = "txt"
            
            # Export the recording
            print(f"\nExporting to {export_format.upper()} format...")
            
            # Create exports directory
            exports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
            if not os.path.exists(exports_dir):
                os.makedirs(exports_dir)
            
            # Generate output filename
            base_name = os.path.basename(recording_path).replace(".json", "")
            output_path = os.path.join(exports_dir, f"{base_name}.{export_format}")
            
            # Export the recording
            try:
                exported_path = export_recording(recording_path, export_format, output_path)
                print(f"\nRecording exported to: {exported_path}")
                
                # Show preview based on format
                if export_format == "csv":
                    print("\nCSV Preview (first few lines):")
                    with open(exported_path, 'r') as f:
                        lines = f.readlines()[:6]  # Read first 6 lines
                        for line in lines:
                            print(f"  {line.strip()}")
                    print("  ...")
                
                elif export_format == "txt":
                    print("\nTXT Preview (first few lines):")
                    with open(exported_path, 'r') as f:
                        lines = f.readlines()[:10]  # Read first 10 lines
                        for line in lines:
                            print(f"  {line.strip()}")
                    print("  ...")
                
                elif export_format == "json":
                    print("\nJSON export successful. This is a structured format suitable for programmatic use.")
            
            except Exception as e:
                print(f"\nError exporting recording: {str(e)}")
        
        else:
            print("\nInvalid selection.")
    
    except ValueError:
        print("\nInvalid input. Please enter a number.")

if __name__ == "__main__":
    main()