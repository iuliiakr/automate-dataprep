import argparse
import wave
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Union # <-- ADD THIS IMPORT

## Example usage:
# python3 scripts/analyze_wav_lengths.py {PATH_TO_INPUT_DIR}
##

def get_wav_duration(file_path: Path) -> Union[float, None]: # <-- CHANGE THIS LINE
    """
    Calculates the duration of a WAV file in seconds.

    Args:
        file_path: A Path object pointing to the .wav file.

    Returns:
        The duration in seconds as a float, or None if the file is invalid.
    """
    try:
        with wave.open(str(file_path), 'rb') as wf:
            n_frames = wf.getnframes()
            framerate = wf.getframerate()
            
            # Avoid division by zero for corrupted or empty files
            if framerate == 0:
                print(f"  ! Warning: File '{file_path.name}' has a framerate of 0. Skipping.")
                return None
                
            duration = n_frames / float(framerate)
            return duration
    except wave.Error as e:
        print(f"  ! Warning: Could not process '{file_path.name}'. Not a valid WAV file. Error: {e}")
        return None
    except Exception as e:
        print(f"  ! An unexpected error occurred with file '{file_path.name}': {e}")
        return None

def main():
    """Main function to parse arguments, analyze files, and plot the distribution."""
    parser = argparse.ArgumentParser(
        description="Analyzes the distribution of audio lengths for all .wav files in a folder."
    )
    parser.add_argument(
        "folder_path", 
        type=str, 
        help="The path to the folder containing .wav files."
    )
    parser.add_argument(
        "--output", 
        type=str,
        default="audio_length_distribution.png",
        help="The filename for the output graph image (default: audio_length_distribution.png)."
    )
    parser.add_argument(
        "--bins", 
        type=int,
        default=50,
        help="The number of bins to use in the histogram (default: 50)."
    )
    args = parser.parse_args()
    
    root_path = Path(args.folder_path)

    if not root_path.is_dir():
        print(f"Error: The path '{root_path}' is not a valid directory.")
        return

    print(f"Scanning for .wav files in '{root_path}' and its subfolders...\n")
    
    # Use glob to find all .wav files recursively
    wav_files = list(root_path.glob('**/*.wav'))
    
    if not wav_files:
        print("No .wav files found in the specified directory.")
        return

    durations = []
    print("Processing files to get durations:")
    for file_path in wav_files:
        print(f" - {file_path.relative_to(root_path)}")
        duration = get_wav_duration(file_path)
        if duration is not None:
            durations.append(duration)

    if not durations:
        print("\nCould not calculate duration for any of the found files.")
        return

    # --- Print Summary Statistics ---
    total_files = len(durations)
    total_duration_s = sum(durations)
    avg_duration = total_duration_s / total_files
    min_duration = min(durations)
    max_duration = max(durations)

    print("\n--- Audio Dataset Summary ---")
    print(f"Total files processed: {total_files}")
    print(f"Total audio length: {total_duration_s / 3600:.2f} hours ({total_duration_s / 60:.2f} minutes)")
    print(f"Average file length: {avg_duration:.2f} seconds")
    print(f"Shortest file:       {min_duration:.2f} seconds")
    print(f"Longest file:        {max_duration:.2f} seconds")
    print("-----------------------------\n")

    # --- Generate the Plot ---
    print(f"Generating distribution graph and saving to '{args.output}'...")
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 7))

    plt.hist(durations, bins=args.bins, color='skyblue', edgecolor='black')

    plt.title('Distribution of Audio File Lengths', fontsize=16)
    plt.xlabel('Duration (seconds)', fontsize=12)
    plt.ylabel('Number of Files', fontsize=12)
    
    plt.axvline(avg_duration, color='red', linestyle='dashed', linewidth=2, label=f'Average: {avg_duration:.2f}s')
    plt.legend()
    
    plt.tight_layout()
    
    try:
        plt.savefig(args.output)
        print(f"Graph successfully saved to {args.output}")
    except Exception as e:
        print(f"Error saving the graph: {e}")

if __name__ == "__main__":
    main()
