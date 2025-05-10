import time
import os
import json
import threading
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

import pyautogui
from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener, Controller as MouseController, Button
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode


class BrogsCursorRecorder:
    """
    A comprehensive tool for recording and precisely replaying user cursor interactions.
    
    This class captures mouse and keyboard events with high fidelity, 
    allowing for exact replication of user actions with customizable settings.
    """
    
    def __init__(
        self, 
        log_dir: str = None,
        max_events: int = 50000, 
        record_keyboard: bool = True,
        speed_multiplier: float = 1.0
    ):
        """
        Initialize the cursor recorder with configurable parameters.

        Args:
            log_dir (str, optional): Directory to store recordings. Defaults to package directory.
            max_events (int, optional): Maximum number of events to record. Defaults to 50000.
            record_keyboard (bool, optional): Whether to record keyboard events. Defaults to True.
            speed_multiplier (float, optional): Speed multiplier for replay. Defaults to 1.0.
        """
        self.mouse_events: List[Dict[str, Any]] = []
        self.keyboard_events: List[Dict[str, Any]] = []
        self.recording = False
        self.record_keyboard = record_keyboard
        self.max_events = max_events
        self.speed_multiplier = speed_multiplier
        self.paused = False
        self.stop_replay = False
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Set up log directory
        if log_dir is None:
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recordings')
        else:
            base_dir = log_dir
            
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            self.logger.info(f"Created recordings directory: {base_dir}")
        
        self.log_dir = base_dir
        
        # Controllers
        self.mouse_controller = MouseController()
        self.keyboard_controller = keyboard.Controller()
        
        # Timing tracking
        self.start_time = 0
        self.pause_time = 0

        # Modifier key states
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False
    
    def _generate_log_filename(self) -> str:
        """Generate a unique recording filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"brogscursor_recording_{timestamp}.json"
        return os.path.join(self.log_dir, filename)
    
    def pause_recording(self) -> None:
        """Pause the recording process."""
        self.paused = True
        self.pause_time = time.time()
        self.logger.info("Recording paused.")
        print("Recording paused. Press 'p' to resume.")

    def resume_recording(self) -> None:
        """Resume the recording after being paused."""
        self.paused = False
        pause_duration = time.time() - self.pause_time
        self.start_time += pause_duration  # Adjust start time to account for pause
        self.logger.info("Recording resumed.")
        print("Recording resumed.")

    def on_move(self, x: int, y: int) -> None:
        """Record mouse movement events with precise timing."""
        if self.recording and not self.paused and len(self.mouse_events) < self.max_events:
            current_time = time.time()
            self.mouse_events.append({
                'type': 'move',
                'pos': (x, y),
                'relative_time': current_time - self.start_time,
                'screen_resolution': pyautogui.size()
            })
    
    def on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """Record mouse click events with precise timing and button details."""
        if self.recording and not self.paused and len(self.mouse_events) < self.max_events:
            current_time = time.time()
            self.mouse_events.append({
                'type': 'click',
                'pos': (x, y),
                'button': str(button),
                'pressed': pressed,
                'relative_time': current_time - self.start_time,
                'screen_resolution': pyautogui.size()
            })
    
    def on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Record mouse scroll events with precise timing."""
        if self.recording and not self.paused and len(self.mouse_events) < self.max_events:
            current_time = time.time()
            self.mouse_events.append({
                'type': 'scroll',
                'pos': (x, y),
                'dx': dx,
                'dy': dy,
                'relative_time': current_time - self.start_time,
                'screen_resolution': pyautogui.size(),
                'trackpad': True  # Indicate trackpad scroll
            })
    
    def on_press(self, key: Key) -> Any:
        """
        Record keyboard press events.
        Stops recording if Escape key is pressed.
        """
        if key == Key.esc:
            self.stop_recording()
            return False
        if isinstance(key, KeyCode) and hasattr(key, 'char') and key.char == 'p':
            if self.paused:
                self.resume_recording()
            else:
                self.pause_recording()
            return True
        
        if self.recording and not self.paused and self.record_keyboard:
            current_time = time.time()
            try:
                key_name = key.char  # For regular keys
            except AttributeError:
                key_name = str(key)  # For special keys

            # Update modifier key states
            if key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
                self.ctrl_pressed = True
            elif key == Key.alt or key == Key.alt_l or key == Key.alt_r:
                self.alt_pressed = True
            elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
                self.shift_pressed = True

            # Handle key combinations
            if key == Key.tab and self.ctrl_pressed:
                self._record_key_combo('ctrl', 'tab')
            elif key == Key.backspace and self.ctrl_pressed:
                self._record_key_combo('ctrl', 'backspace')
            else:
                self.keyboard_events.append({
                    'type': 'keypress',
                    'key': key_name,
                    'relative_time': current_time - self.start_time
                })
    
    def _record_key_combo(self, modifier: str, key: str) -> None:
        """Record a key combination as a sequence of keydown/keyup events."""
        current_time = time.time()
        relative_time = current_time - self.start_time
        
        self.keyboard_events.append({
            'type': 'keydown',
            'key': modifier,
            'relative_time': relative_time
        })
        self.keyboard_events.append({
            'type': 'keydown',
            'key': key,
            'relative_time': relative_time
        })
        self.keyboard_events.append({
            'type': 'keyup',
            'key': key,
            'relative_time': relative_time
        })
        self.keyboard_events.append({
            'type': 'keyup',
            'key': modifier,
            'relative_time': relative_time
        })
    
    def on_release(self, key: Key) -> Any:
        """
        Track key release events for modifier keys.
        """
        if key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
            self.ctrl_pressed = False
        elif key == Key.alt or key == Key.alt_l or key == Key.alt_r:
            self.alt_pressed = False
        elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
            self.shift_pressed = False
        
        return True

    def start_recording(self, timeout: Optional[int] = None) -> None:
        """
        Start recording user interactions (mouse and keyboard events).
        
        Args:
            timeout (int, optional): Recording will stop after this many seconds if specified.
        """
        self.mouse_events.clear()
        self.keyboard_events.clear()
        self.recording = True
        self.paused = False
        self.start_time = time.time()
        
        self.logger.info(f"Recording started. Press Esc to stop or 'p' to pause/resume.")
        print(f"Recording started. Press Esc to stop or 'p' to pause/resume.")
        
        # Start listeners in separate threads
        mouse_listener = MouseListener(
            on_move=self.on_move, 
            on_click=self.on_click, 
            on_scroll=self.on_scroll
        )
        keyboard_listener = KeyboardListener(
            on_press=self.on_press, 
            on_release=self.on_release
        )
        
        mouse_listener.start()
        keyboard_listener.start()
        
        # Handle timeout if specified
        if timeout:
            def stop_after_timeout():
                time.sleep(timeout)
                if self.recording:
                    print(f"Recording stopped after {timeout} seconds timeout.")
                    self.stop_recording()
            
            timeout_thread = threading.Thread(target=stop_after_timeout)
            timeout_thread.daemon = True
            timeout_thread.start()
        
        # Wait for keyboard listener to complete (when Escape is pressed)
        keyboard_listener.join()
        mouse_listener.stop()
    
    def stop_recording(self) -> str:
        """
        Stop recording and save the captured actions.

        Returns:
            str: Path to the saved recording file
        """
        self.recording = False
        
        if not self.mouse_events and not self.keyboard_events:
            self.logger.warning("No events to save.")
            return ""
        
        log_file = self._generate_log_filename()
        
        try:
            with open(log_file, 'w') as f:
                json.dump({
                    'mouse_events': self.mouse_events,
                    'keyboard_events': self.keyboard_events,
                    'metadata': {
                        'total_mouse_events': len(self.mouse_events),
                        'total_keyboard_events': len(self.keyboard_events),
                        'total_recording_time': self.mouse_events[-1]['relative_time'] if self.mouse_events else 0
                    }
                }, f, indent=2)
            
            self.logger.info(f"Recording saved to {log_file}")
            print(f"Recording saved to {log_file}")
            return log_file
        except Exception as e:
            self.logger.error(f"Error saving recording: {e}")
            print(f"Error saving recording: {e}")
            return ""
    
    def list_recordings(self) -> List[str]:
        """
        List all saved recordings in the log directory.
        
        Returns:
            List[str]: List of recording filenames
        """
        try:
            return [f for f in os.listdir(self.log_dir) if f.endswith('.json')]
        except Exception as e:
            self.logger.error(f"Error listing recordings: {e}")
            return []

    def replay(
        self, 
        recording_file: str, 
        precision_mode: bool = True, 
        filter_events: List[str] = None, 
        loop_count: int = 1,
        stop_key: str = 'p'
    ) -> bool:
        """
        Precisely replay recorded user actions.

        Args:
            recording_file (str): Path to the recording JSON file
            precision_mode (bool, optional): If True, maintains exact timing of original actions
            filter_events (List[str], optional): List of event types to filter out during replay
            loop_count (int, optional): Number of times to loop the replay (1-10)
            stop_key (str, optional): Key to press to stop replay
            
        Returns:
            bool: True if replay completed successfully, False otherwise
        """
        try:
            # Load recording file
            with open(recording_file, 'r') as f:
                recording_data = json.load(f)
            
            # Combine and sort events
            all_events = []
            all_events.extend([
                {**event, 'event_type': 'mouse'} 
                for event in recording_data.get('mouse_events', [])
            ])
            all_events.extend([
                {**event, 'event_type': 'keyboard'} 
                for event in recording_data.get('keyboard_events', [])
            ])
            
            # Sort events by relative time
            all_events.sort(key=lambda x: x['relative_time'])
            
            # Reset stop flag
            self.stop_replay = False
            
            # Start stop key listener in a background thread
            stop_thread = threading.Thread(target=self._listen_for_stop, args=(stop_key,))
            stop_thread.daemon = True
            stop_thread.start()
            
            # Replay events for specified number of loops
            for loop in range(loop_count):
                if self.stop_replay:
                    break
                    
                print(f"Starting replay loop {loop+1}/{loop_count}")
                
                for i, event in enumerate(all_events):
                    if self.stop_replay:
                        break
                        
                    # Skip filtered event types
                    if filter_events and event['type'] in filter_events:
                        continue
                    
                    # Wait for the precise moment if precision mode is enabled
                    if i > 0 and precision_mode:
                        wait_time = (event['relative_time'] - all_events[i-1]['relative_time']) / self.speed_multiplier
                        time.sleep(max(0, wait_time))
                    
                    # Handle different event types
                    if event['event_type'] == 'mouse':
                        self._replay_mouse_event(event)
                    elif event['event_type'] == 'keyboard':
                        self._replay_keyboard_event(event)
            
            self.logger.info("Replay completed successfully.")
            print("Replay completed successfully.")
            return True
        
        except FileNotFoundError:
            self.logger.error(f"Recording file not found: {recording_file}")
            print(f"Recording file not found: {recording_file}")
            return False
        except Exception as e:
            self.logger.error(f"Replay error: {e}")
            print(f"Replay error: {e}")
            return False
    
    def _listen_for_stop(self, stop_key: str) -> None:
        """Listen for stop key press during replay."""
        def on_press(key):
            if isinstance(key, KeyCode) and hasattr(key, 'char') and key.char == stop_key:
                self.stop_replay = True
                print(f"Replay stopped by user ('{stop_key}' key pressed).")
                return False
            return True
            
        with KeyboardListener(on_press=on_press) as listener:
            listener.join()
    
    def _replay_mouse_event(self, event: Dict[str, Any]) -> None:
        """
        Replay a specific mouse event with precise positioning.
        
        Args:
            event (Dict[str, Any]): Mouse event details
        """
        # Scale coordinates for current screen resolution
        original_resolution = event.get('screen_resolution', (1920, 1080))
        current_resolution = pyautogui.size()
        
        x, y = event['pos']
        scaled_x = int(x * (current_resolution[0] / original_resolution[0]))
        scaled_y = int(y * (current_resolution[1] / original_resolution[1]))
        
        if event['type'] == 'move':
            # Move immediately with no duration
            self.mouse_controller.position = (scaled_x, scaled_y)
        elif event['type'] == 'click':
            # Move instantly then click
            self.mouse_controller.position = (scaled_x, scaled_y)
            button = event['button'].lower()
            if 'left' in button:
                if event['pressed']:
                    pyautogui.mouseDown(scaled_x, scaled_y, button='left', duration=0)
                else:
                    pyautogui.mouseUp(scaled_x, scaled_y, button='left', duration=0)
            elif 'right' in button:
                if event['pressed']:
                    pyautogui.mouseDown(scaled_x, scaled_y, button='right', duration=0)
                else:
                    pyautogui.mouseUp(scaled_x, scaled_y, button='right', duration=0)
        elif event['type'] == 'scroll':
            pyautogui.scroll(event['dy'])

    def _replay_keyboard_event(self, event: Dict[str, Any]) -> None:
        """
        Replay a specific keyboard event with proper key simulation.
        
        Args:
            event (Dict[str, Any]): Keyboard event details
        """
        try:
            # Map string key names to pynput Key objects
            key_map = {
                'Key.shift': Key.shift,
                'Key.shift_r': Key.shift_r,
                'Key.shift_l': Key.shift_l,
                'Key.alt': Key.alt,
                'Key.alt_l': Key.alt_l,
                'Key.alt_r': Key.alt_r,
                'Key.ctrl': Key.ctrl,
                'Key.ctrl_l': Key.ctrl_l,
                'Key.ctrl_r': Key.ctrl_r,
                'Key.enter': Key.enter,
                'Key.caps_lock': Key.caps_lock,
                'Key.tab': Key.tab,
                'Key.space': Key.space,
                'Key.backspace': Key.backspace,
                'Key.delete': Key.delete,
                'Key.up': Key.up,
                'Key.down': Key.down,
                'Key.left': Key.left,
                'Key.right': Key.right,
                'Key.home': Key.home,
                'Key.end': Key.end,
                'Key.page_up': Key.page_up,
                'Key.page_down': Key.page_down,
                
                # Simplified mappings
                'ctrl': Key.ctrl,
                'tab': Key.tab,
                'backspace': Key.backspace,
            }

            event_type = event['type']
            key = event['key']

            if event_type == 'keydown':
                if key in key_map:
                    self.keyboard_controller.press(key_map[key])
                else:
                    self.keyboard_controller.press(key)
            elif event_type == 'keyup':
                if key in key_map:
                    self.keyboard_controller.release(key_map[key])
                else:
                    self.keyboard_controller.release(key)
            elif event_type == 'keypress':
                if key in key_map:
                    self.keyboard_controller.press(key_map[key])
                    self.keyboard_controller.release(key_map[key])
                else:
                    self.keyboard_controller.press(key)
                    self.keyboard_controller.release(key)

        except Exception as e:
            self.logger.error(f"Error replaying keyboard event: {e}")