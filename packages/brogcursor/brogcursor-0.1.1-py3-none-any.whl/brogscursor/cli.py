import os
import time
import threading
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from .recorder import BrogsCursorRecorder


class BrogsCursorCLI:
    """Command-line interface for BrogsCursor."""
    
    def __init__(self):
        """Initialize the CLI with a console and recorder."""
        self.console = Console()
        self.recorder = BrogsCursorRecorder()
    
    def display_welcome(self) -> None:
        """Display welcome message and package information."""
        self.console.print(
            Panel.fit(
                "[bold blue]BrogsCursor[/bold blue] - [italic]Precise Mouse & Keyboard Action Recorder[/italic]",
                subtitle="Press Esc to stop recording, 'p' to pause/resume",
                border_style="blue"
            )
        )
    
    def display_menu(self) -> str:
        """
        Display the main menu and get user choice.
        
        Returns:
            str: User's menu choice
        """
        self.console.print("\n[bold cyan]BrogsCursor Menu[/bold cyan]")
        
        table = Table(show_header=False, box=None)
        table.add_column("Choice", style="cyan")
        table.add_column("Description")
        
        table.add_row("1", "Start Recording")
        table.add_row("2", "List Recordings")
        table.add_row("3", "Replay Recording")
        table.add_row("4", "Settings")
        table.add_row("5", "Exit")
        
        self.console.print(table)
        return Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"], default="1")
    
    def handle_start_recording(self) -> None:
        """Handle the start recording option."""
        use_timeout = Confirm.ask("Set a recording timeout?")
        timeout = None
        
        if use_timeout:
            timeout_str = Prompt.ask("Enter timeout in seconds", default="60")
            try:
                timeout = int(timeout_str)
                if timeout <= 0:
                    self.console.print("[yellow]Invalid timeout. Using default of 60 seconds.[/yellow]")
                    timeout = 60
            except ValueError:
                self.console.print("[yellow]Invalid timeout. Using default of 60 seconds.[/yellow]")
                timeout = 60
                
            self.console.print(f"[yellow]Recording will stop after {timeout} seconds.[/yellow]")
        
        self.console.print("[bold green]Starting recording...[/bold green]")
        self.console.print("[italic]Press Esc to stop recording or 'p' to pause/resume.[/italic]")
        
        # Small countdown
        for i in range(3, 0, -1):
            self.console.print(f"Starting in {i}...")
            time.sleep(1)
            
        # Start recording in a separate thread
        recording_thread = threading.Thread(target=self.recorder.start_recording, args=(timeout,))
        recording_thread.start()
        recording_thread.join()
    
    def handle_list_recordings(self) -> List[str]:
        """
        Handle the list recordings option.
        
        Returns:
            List[str]: List of available recordings
        """
        recordings = self.recorder.list_recordings()
        
        if not recordings:
            self.console.print("[yellow]No recordings found.[/yellow]")
            return []
        
        self.console.print("[bold green]Available Recordings:[/bold green]")
        
        table = Table(show_header=True)
        table.add_column("#", style="cyan")
        table.add_column("Recording")
        table.add_column("Date", style="green")
        table.add_column("Time", style="green")
        
        for i, recording in enumerate(recordings, 1):
            # Parse date and time from filename
            parts = recording.replace("brogscursor_recording_", "").replace(".json", "").split("_")
            if len(parts) >= 2:
                date = parts[0]
                date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
                time = parts[1]
                time = f"{time[:2]}:{time[2:4]}:{time[4:6]}"
            else:
                date = "Unknown"
                time = "Unknown"
                
            table.add_row(str(i), recording, date, time)
        
        self.console.print(table)
        return recordings
    
    def handle_replay_recording(self) -> None:
        """Handle the replay recording option."""
        recordings = self.handle_list_recordings()
        
        if not recordings:
            return
        
        try:
            selection_str = Prompt.ask(
                "Enter recording number to replay",
                default="1"
            )
            try:
                selection = int(selection_str)
                if selection < 1 or selection > len(recordings):
                    self.console.print(f"[bold red]Error:[/bold red] Selection must be between 1 and {len(recordings)}")
                    return
            except ValueError:
                self.console.print("[bold red]Error:[/bold red] Please enter a valid number")
                return
                
            selected_recording = recordings[selection - 1]
            recording_path = os.path.join(self.recorder.log_dir, selected_recording)
            
            # Configure replay options
            precision = Confirm.ask("Enable precise timing?", default=True)
            
            speed_options = {
                "1": 0.5,  # Half speed
                "2": 1.0,  # Normal speed
                "3": 2.0,  # Double speed
                "4": 5.0,  # 5x speed
            }
            
            speed_table = Table(title="Speed Options")
            speed_table.add_column("Option", style="cyan")
            speed_table.add_column("Speed")
            
            for option, multiplier in speed_options.items():
                speed_desc = f"{multiplier}x " + ("(slower)" if multiplier < 1 else "normal" if multiplier == 1 else "(faster)")
                speed_table.add_row(option, speed_desc)
            
            self.console.print(speed_table)
            
            speed_choice = Prompt.ask(
                "Select replay speed",
                choices=list(speed_options.keys()),
                default="2"
            )
            self.recorder.speed_multiplier = speed_options[speed_choice]
            
            loop = Confirm.ask("Loop the replay?")
            loop_count = 1
            
            if loop:
                loop_count_str = Prompt.ask(
                    "Enter number of times to loop (1-10)",
                    default="2"
                )
                try:
                    loop_count = int(loop_count_str)
                    if loop_count < 1 or loop_count > 10:
                        self.console.print("[bold yellow]Warning:[/bold yellow] Value out of range. Using default of 2 loops.")
                        loop_count = 2
                except ValueError:
                    self.console.print("[bold yellow]Warning:[/bold yellow] Invalid input. Using default of 2 loops.")
                    loop_count = 2
            
            self.console.print("\n[bold green]Starting replay...[/bold green]")
            self.console.print("[italic]Press 'p' to stop replay.[/italic]")
            
            # Small countdown
            for i in range(3, 0, -1):
                self.console.print(f"Starting in {i}...")
                time.sleep(1)
            
            # Start replay in a separate thread
            self.recorder.replay(recording_path, precision_mode=precision, loop_count=loop_count)
            
        except (ValueError, IndexError) as e:
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    def handle_settings(self) -> None:
        """Handle the settings option."""
        self.console.print("[bold cyan]Settings[/bold cyan]")
        
        settings_table = Table(show_header=False)
        settings_table.add_column("Setting", style="green")
        settings_table.add_column("Value")
        settings_table.add_column("Description")
        
        settings_table.add_row(
            "1. Log Directory", 
            self.recorder.log_dir,
            "Where recordings are saved"
        )
        settings_table.add_row(
            "2. Max Events", 
            str(self.recorder.max_events),
            "Maximum events to record"
        )
        settings_table.add_row(
            "3. Record Keyboard", 
            str(self.recorder.record_keyboard),
            "Whether to record keyboard events"
        )
        settings_table.add_row(
            "4. Speed Multiplier", 
            str(self.recorder.speed_multiplier),
            "Default replay speed multiplier"
        )
        
        self.console.print(settings_table)
        
        setting_choice = Prompt.ask(
            "Select setting to change",
            choices=["1", "2", "3", "4", "0"],
            default="0"
        )
        
        if setting_choice == "0":
            return
        elif setting_choice == "1":
            new_dir = Prompt.ask("Enter new log directory", default=self.recorder.log_dir)
            if not os.path.exists(new_dir):
                create = Confirm.ask(f"Directory {new_dir} doesn't exist. Create it?")
                if create:
                    try:
                        os.makedirs(new_dir)
                        self.recorder.log_dir = new_dir
                        self.console.print(f"[green]Log directory changed to {new_dir}[/green]")
                    except Exception as e:
                        self.console.print(f"[bold red]Error creating directory:[/bold red] {str(e)}")
            else:
                self.recorder.log_dir = new_dir
                self.console.print(f"[green]Log directory changed to {new_dir}[/green]")
        elif setting_choice == "2":
            new_max_str = Prompt.ask(
                "Enter maximum events to record (100-1000000)",
                default=str(self.recorder.max_events)
            )
            try:
                new_max = int(new_max_str)
                if 100 <= new_max <= 1000000:
                    self.recorder.max_events = new_max
                    self.console.print(f"[green]Max events changed to {new_max}[/green]")
                else:
                    self.console.print("[red]Invalid value. Must be between 100 and 1000000.[/red]")
            except ValueError:
                self.console.print("[red]Invalid input. Please enter a number.[/red]")
        elif setting_choice == "3":
            new_value = Confirm.ask("Record keyboard events?", default=self.recorder.record_keyboard)
            self.recorder.record_keyboard = new_value
            self.console.print(f"[green]Record keyboard set to {new_value}[/green]")
        elif setting_choice == "4":
            new_speed_str = Prompt.ask(
                "Enter speed multiplier (0.1-10)",
                default=str(self.recorder.speed_multiplier)
            )
            try:
                new_speed = float(new_speed_str)
                if 0.1 <= new_speed <= 10:
                    self.recorder.speed_multiplier = new_speed
                    self.console.print(f"[green]Speed multiplier changed to {new_speed}[/green]")
                else:
                    self.console.print("[red]Invalid speed multiplier. Must be between 0.1 and 10.[/red]")
            except ValueError:
                self.console.print("[red]Invalid input. Please enter a number.[/red]")
    
    def run(self) -> None:
        """Run the CLI application."""
        self.display_welcome()
        
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.handle_start_recording()
            elif choice == "2":
                self.handle_list_recordings()
            elif choice == "3":
                self.handle_replay_recording()
            elif choice == "4":
                self.handle_settings()
            elif choice == "5":
                self.console.print("[bold blue]Goodbye![/bold blue]")
                break


def main():
    """Entry point for the CLI."""
    cli = BrogsCursorCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        cli.console.print("\n[bold red]Program interrupted by user.[/bold red]")
    except Exception as e:
        cli.console.print(f"\n[bold red]An error occurred:[/bold red] {str(e)}")


if __name__ == "__main__":
    main()