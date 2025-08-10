import argparse
import sys
from pathlib import Path
import shutil

# pip install tqdm colorama
# Examples:
# python process_transcripts.py [INPUT_FOLDER] [OUTPUT_OPTION] [OPTIONAL_FLAGS]

# Basic usage:
# python process_transcripts.py raw_texts/ -o cleaned_texts/

# With logging:
# python process_transcripts.py raw_texts/ -o cleaned_texts/ -l changes.log

# Overwriting Original Files
# python process_transcripts.py raw_texts/ --overwrite

# Disabling the Audio Check
# python process_transcripts.py raw_texts/ -o cleaned_texts/ --no-audio-check


try:
    from tqdm import tqdm
    from colorama import Fore, Style, init
except ImportError:
    print("Error: Required libraries not found. Please run 'pip install tqdm colorama'")
    sys.exit(1)

init(autoreset=True)

AUDIO_EXTENSIONS = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
BAD_ENDINGS = (',', ':', ';', '-')
GOOD_ENDINGS = ('.', '!', '?')

def is_dir_empty(path: Path) -> bool:
    return not any(path.iterdir())

def process_text_content(content: str) -> str:
    text = content
    text = text.lstrip()
    if not text: return ""
    if text[0].islower(): text = text[0].upper() + text[1:]
    if text.endswith(BAD_ENDINGS): text = text[:-1] + '.'
    if not text.endswith(GOOD_ENDINGS): text = text + '.'
    return text

def main():
    parser = argparse.ArgumentParser(
        description="A user-friendly script to process .txt files, cleaning up common transcription issues.",
        epilog="Example: python process_transcripts.py ./my_audio -o ./cleaned -l changes.log",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('input_folder', type=Path, help="Path to the folder containing .txt and audio files.")
    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument('-o', '--output-folder', type=Path, help="Path to save processed .txt files.")
    output_group.add_argument('--overwrite', action='store_true', help="Overwrite the original .txt files.")
    parser.add_argument('-l', '--log-file', type=Path, help="Optional: Path to save a log of files whose content was modified.")
    parser.add_argument('--no-audio-check', action='store_true', help="Disable the check for a corresponding audio file.")

    args = parser.parse_args()

    input_path = args.input_folder
    if not input_path.is_dir():
        print(f"{Fore.RED}Error: Input folder not found at '{input_path}'"); sys.exit(1)

    if args.overwrite:
        confirm = input(f"{Fore.YELLOW}Overwrite original files? This is irreversible. (yes/no): ");
        if confirm.lower() != 'yes': print(f"{Fore.CYAN}Operation cancelled."); sys.exit(0)
        output_path = None
    else:
        output_path = args.output_folder
        if output_path.resolve() == input_path.resolve():
            print(f"{Fore.RED}Error: Input and output folders cannot be the same. Use --overwrite instead."); sys.exit(1)
        if output_path.exists():
            if not output_path.is_dir(): print(f"{Fore.RED}Error: Output path '{output_path}' exists but is a file."); sys.exit(1)
            if not is_dir_empty(output_path):
                confirm = input(f"{Fore.YELLOW}Output folder '{output_path}' is not empty. Files may be overwritten. Continue? (yes/no): ")
                if confirm.lower() != 'yes': print(f"{Fore.CYAN}Operation cancelled."); sys.exit(0)
        else:
            print(f"{Fore.GREEN}Output folder not found. Creating it at: {output_path}")
            output_path.mkdir(parents=True, exist_ok=True)

    txt_files = sorted([f for f in input_path.iterdir() if f.suffix.lower() == '.txt'])
    if not txt_files: print(f"{Fore.YELLOW}No .txt files found in the input folder."); sys.exit(0)

    processed_count, changed_count, warning_count, error_count = 0, 0, 0, 0
    changed_files_log = []

    print(f"\n{Fore.CYAN}Starting processing for {len(txt_files)} text files...{Style.RESET_ALL}")
    
    for file_path in (pbar := tqdm(txt_files, desc="Processing files", unit="file")):
        try:
            pbar.set_postfix_str(file_path.name, refresh=True)
            original_content = file_path.read_text(encoding='utf-8')
            processed_content = process_text_content(original_content)
            
            if original_content != processed_content:
                changed_count += 1
                changed_files_log.append(file_path.name)
                output_filepath = output_path / file_path.name if not args.overwrite else file_path
                output_filepath.write_text(processed_content, encoding='utf-8')
            else:
                if not args.overwrite:
                    shutil.copy2(file_path, output_path)

            processed_count += 1
            if not args.no_audio_check:
                if not any((file_path.with_suffix(ext)).exists() for ext in AUDIO_EXTENSIONS):
                    tqdm.write(f"{Fore.YELLOW}  -> WARNING: No corresponding audio file for {file_path.name}")
                    warning_count += 1
        except Exception as e:
            tqdm.write(f"{Fore.RED}  -> ERROR: Could not process file {file_path.name}. Reason: {e}")
            error_count += 1

    if args.log_file:
        try:
            args.log_file.parent.mkdir(parents=True, exist_ok=True)
            log_content = "# Log of files with changed content\n" + "\n".join(sorted(changed_files_log))
            args.log_file.write_text(log_content, encoding='utf-8')
            print(f"\n{Fore.GREEN}Log of changed files saved to: {args.log_file}")
        except Exception as e:
            print(f"\n{Fore.RED}Error: Could not write log file. Reason: {e}")
            
    # --- FINAL, UNAMBIGUOUS SUMMARY ---
    unchanged_count = processed_count - changed_count
    print(f"\n--- {Fore.GREEN}Processing Complete!{Style.RESET_ALL} ---")
    print(f"  Total files analyzed:           {processed_count}")
    print(f"  {Fore.GREEN}Files with modified content:  {changed_count}")
    print(f"  {Fore.CYAN}Files with identical content:   {unchanged_count}")
    if warning_count > 0: print(f"  {Fore.YELLOW}Files with warnings:            {warning_count}")
    if error_count > 0: print(f"  {Fore.RED}Files with errors:              {error_count}")

if __name__ == '__main__':
    main()
