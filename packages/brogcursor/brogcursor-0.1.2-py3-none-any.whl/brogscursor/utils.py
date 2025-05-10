"""Utility functions for the BrogsCursor package."""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


def get_recording_info(recording_path: str) -> Dict[str, Any]:
    """
    Get information about a recording file.
    
    Args:
        recording_path (str): Path to the recording file
        
    Returns:
        Dict[str, Any]: Information about the recording
    """
    try:
        with open(recording_path, 'r') as f:
            data = json.load(f)
        
        # Extract filename without path
        filename = os.path.basename(recording_path)
        
        # Parse timestamp from filename
        timestamp_str = filename.replace("brogscursor_recording_", "").replace(".json", "")
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            date = timestamp.strftime("%Y-%m-%d")
            time = timestamp.strftime("%H:%M:%S")
        except ValueError:
            date = "Unknown"
            time = "Unknown"
        
        # Extract metadata
        metadata = data.get('metadata', {})
        total_mouse_events = metadata.get('total_mouse_events', 0)
        total_keyboard_events = metadata.get('total_keyboard_events', 0)
        total_recording_time = metadata.get('total_recording_time', 0)
        
        return {
            "filename": filename,
            "date": date,
            "time": time,
            "mouse_events": total_mouse_events,
            "keyboard_events": total_keyboard_events,
            "duration": f"{total_recording_time:.2f} seconds",
            "total_events": total_mouse_events + total_keyboard_events
        }
    except Exception as e:
        return {
            "filename": os.path.basename(recording_path),
            "error": str(e)
        }


def export_recording(recording_path: str, export_format: str = "json", output_path: Optional[str] = None) -> str:
    """
    Export a recording to different formats.
    
    Args:
        recording_path (str): Path to the recording file
        export_format (str): Format to export to (json, csv, txt)
        output_path (str, optional): Path to save the exported file
        
    Returns:
        str: Path to the exported file
    """
    try:
        with open(recording_path, 'r') as f:
            data = json.load(f)
        
        # Default output path
        if output_path is None:
            directory = os.path.dirname(recording_path)
            base_name = os.path.basename(recording_path).replace(".json", "")
            output_path = os.path.join(directory, f"{base_name}.{export_format}")
        
        # Export based on format
        if export_format.lower() == "json":
            # Already in JSON format, just copy
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
        
        elif export_format.lower() == "csv":
            import csv
            
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["Event Type", "Action", "X", "Y", "Key", "Time", "Button", "Pressed"])
                
                # Write mouse events
                for event in data.get('mouse_events', []):
                    x, y = event.get('pos', (0, 0))
                    writer.writerow([
                        'mouse',
                        event.get('type', ''),
                        x, y,
                        '',
                        event.get('relative_time', 0),
                        event.get('button', ''),
                        event.get('pressed', '')
                    ])
                
                # Write keyboard events
                for event in data.get('keyboard_events', []):
                    writer.writerow([
                        'keyboard',
                        event.get('type', ''),
                        '', '',
                        event.get('key', ''),
                        event.get('relative_time', 0),
                        '', ''
                    ])
        
        elif export_format.lower() == "txt":
            with open(output_path, 'w') as f:
                # Write header
                f.write(f"BrogsCursor Recording Export\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Original file: {os.path.basename(recording_path)}\n\n")
                
                # Write metadata
                metadata = data.get('metadata', {})
                f.write(f"Total mouse events: {metadata.get('total_mouse_events', 0)}\n")
                f.write(f"Total keyboard events: {metadata.get('total_keyboard_events', 0)}\n")
                f.write(f"Recording duration: {metadata.get('total_recording_time', 0):.2f} seconds\n\n")
                
                # Write event summary
                f.write(f"EVENT SUMMARY:\n")
                f.write(f"-------------\n")
                
                # Write mouse events
                f.write(f"\nMOUSE EVENTS:\n")
                for i, event in enumerate(data.get('mouse_events', []), 1):
                    event_type = event.get('type', '')
                    x, y = event.get('pos', (0, 0))
                    time = event.get('relative_time', 0)
                    
                    if event_type == 'move':
                        f.write(f"{i}. MOVE to ({x}, {y}) at {time:.3f}s\n")
                    elif event_type == 'click':
                        button = event.get('button', '')
                        pressed = "pressed" if event.get('pressed', False) else "released"
                        f.write(f"{i}. CLICK {button} {pressed} at ({x}, {y}) at {time:.3f}s\n")
                    elif event_type == 'scroll':
                        dy = event.get('dy', 0)
                        direction = "down" if dy < 0 else "up"
                        f.write(f"{i}. SCROLL {direction} at ({x}, {y}) at {time:.3f}s\n")
                
                # Write keyboard events
                f.write(f"\nKEYBOARD EVENTS:\n")
                for i, event in enumerate(data.get('keyboard_events', []), 1):
                    event_type = event.get('type', '')
                    key = event.get('key', '')
                    time = event.get('relative_time', 0)
                    
                    f.write(f"{i}. {event_type.upper()} key '{key}' at {time:.3f}s\n")
        
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        return output_path
    
    except Exception as e:
        raise Exception(f"Export error: {str(e)}")


def merge_recordings(recording_paths: List[str], output_path: Optional[str] = None) -> str:
    """
    Merge multiple recordings into a single file.
    
    Args:
        recording_paths (List[str]): List of paths to recording files
        output_path (str, optional): Path to save the merged file
        
    Returns:
        str: Path to the merged file
    """
    try:
        # Load all recordings
        all_mouse_events = []
        all_keyboard_events = []
        time_offset = 0.0
        
        for path in recording_paths:
            with open(path, 'r') as f:
                data = json.load(f)
            
            # Get events
            mouse_events = data.get('mouse_events', [])
            keyboard_events = data.get('keyboard_events', [])
            
            # Adjust relative times
            for event in mouse_events:
                event['relative_time'] += time_offset
            
            for event in keyboard_events:
                event['relative_time'] += time_offset
            
            # Add events to combined lists
            all_mouse_events.extend(mouse_events)
            all_keyboard_events.extend(keyboard_events)
            
            # Update time offset for next recording
            max_time = max(
                [event['relative_time'] for event in mouse_events] if mouse_events else [0],
                [event['relative_time'] for event in keyboard_events] if keyboard_events else [0]
            )
            time_offset += max_time + 1.0  # Add 1 second gap between recordings
        
        # Create merged data
        merged_data = {
            'mouse_events': all_mouse_events,
            'keyboard_events': all_keyboard_events,
            'metadata': {
                'total_mouse_events': len(all_mouse_events),
                'total_keyboard_events': len(all_keyboard_events),
                'total_recording_time': time_offset,
                'merged_from': [os.path.basename(path) for path in recording_paths]
            }
        }
        
        # Default output path
        if output_path is None:
            directory = os.path.dirname(recording_paths[0])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(directory, f"brogscursor_merged_{timestamp}.json")
        
        # Save merged recording
        with open(output_path, 'w') as f:
            json.dump(merged_data, f, indent=2)
        self.logger.info(f"Finished merging recordings into: {output_path}")
        print(f"Finished merging recordings into: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Merge error: {str(e)}")