from brogscursor.utils import get_recording_info, export_recording, merge_recordings

# Get info about a recording
info = get_recording_info("path/to/recording.json")

# Export recording to different format
export_recording("path/to/recording.json", "csv")

# Merge multiple recordings
merge_recordings(["recording1.json", "recording2.json"])