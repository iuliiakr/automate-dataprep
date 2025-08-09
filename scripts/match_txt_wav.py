import os
import sys

def find_unmatched_txt_files(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    txt_files = set()
    wav_files = set()

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext == '.txt':
                txt_files.add(name)
            elif ext == '.wav':
                wav_files.add(name)

    unmatched_txt = txt_files - wav_files

    if unmatched_txt:
        print("TXT files without matching WAV files:")
        for name in sorted(unmatched_txt):
            print(f"{name}.txt")
    else:
        print("All TXT files have matching WAV files.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_folder>")
    else:
        find_unmatched_txt_files(sys.argv[1])
