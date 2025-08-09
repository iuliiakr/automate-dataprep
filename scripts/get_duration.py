import os
import sys
import argparse
import subprocess
from math import floor

## Example:
# python3 get_duration.py {PATH_TO_INPUT_DIR}



AUDIO_EXTS = {".mp3", ".opus", ".wav", ".flac", ".ogg", ".m4a", ".aac"}  # add more if needed

def iter_audio_files(root: str, follow_symlinks: bool):
    # Fast, memory-friendly recursive walk using os.scandir
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            with os.scandir(d) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=follow_symlinks):
                            # skip hidden directories quickly
                            if entry.name.startswith("."):
                                continue
                            stack.append(entry.path)
                        elif entry.is_file(follow_symlinks=follow_symlinks):
                            # filter by extension without allocating big lists
                            name = entry.name
                            dot = name.rfind(".")
                            if dot != -1 and name[dot:].lower() in AUDIO_EXTS:
                                yield entry.path
                    except OSError:
                        # ignore permission/IO errors on individual entries
                        continue
        except OSError:
            continue

def get_duration_seconds(path: str) -> float:
    # Use ffprobe to avoid decoding full audio; robust across formats
    # Outputs just the duration (seconds, float). Fallback to 0 on errors.
    try:
        cp = subprocess.run(
            ["ffprobe", "-v", "error",
             "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True
        )
        if cp.returncode != 0:
            return 0.0
        s = (cp.stdout or "").strip()
        return float(s) if s and s.lower() != "n/a" else 0.0
    except Exception:
        return 0.0

def format_hhmmss(total_seconds: float) -> str:
    t = int(floor(total_seconds + 0.5))  # round to nearest second
    h = t // 3600
    m = (t % 3600) // 60
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def main():
    parser = argparse.ArgumentParser(
        description="Sum durations of audio files and print HH:MM:SS."
    )
    parser.add_argument("directory", help="Root directory to scan")
    parser.add_argument("--workers", type=int,
                        default=max(8, (os.cpu_count() or 2) * 4),
                        help="Parallel ffprobe workers (default: 4x CPU, min 8)")
    parser.add_argument("--follow-symlinks", action="store_true",
                        help="Follow symlinks when walking directories")
    args = parser.parse_args()

    root = os.path.abspath(args.directory)
    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Stream paths and process in parallel
    total = 0.0
    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = []
        for p in iter_audio_files(root, args.follow_symlinks):
            futures.append(ex.submit(get_duration_seconds, p))
            # Submit in batches to keep memory bounded for gigantic trees
            if len(futures) >= args.workers * 64:
                for f in as_completed(futures):
                    total += f.result()
                futures.clear()
        # Drain remaining
        for f in as_completed(futures):
            total += f.result()

    print(f"Total duration of audio: {format_hhmmss(total)}")

if __name__ == "__main__":
    main()
