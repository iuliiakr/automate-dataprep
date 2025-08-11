# automate-dataprep
Useful Python scripts to automate data processing for TTS and STS ML projects.

- [Get total duration of audio]()
- [Check duration distribution]()
- [Check for TXT and WAV matching files]()
- [Basic transcription cleaning]()

## Get total duration of audio in an input directory. Uses ffprobe.
[scripts/get_duration.py](https://github.com/iuliiakr/automate-dataprep/blob/main/scripts/get_duration.py)
Outputs total duration (hh:mm:ss) of all audio (mp3, opus, wav, flac, ogg, m4a, aac) in an input directory.
Example of usage:
```bash
python scripts/get_duration.py {PATH_TO_INPUT_DIR}
```


## Check duration distribution for your dataset
[scripts/analyze_wav_lengths.py](https://github.com/iuliiakr/automate-dataprep/blob/main/scripts/analyze_wav_lengths.py)
For TTS conversions duration of audio files in your training datasets matters.
This script outputs total number of files processed, total duration, average duration, shortest and longest (in seconds) and also a PNG file with a distribution of audio durations in the input directory.
Example of usage:
```bash
python scripts/analyze_wav_lengths.py {PATH_TO_INPUT_DIR}
```


## Check if all TXT files have matching WAV files
[scripts/match_txt_wav.py](https://github.com/iuliiakr/automate-dataprep/blob/main/scripts/match_txt_wav.py)
When you manually validate your TTS dataset you want to be sure that you have matching pairs of audio (wav) and transcription (txt) files. In case if you discarded one, bu accidentally kept another.
This script take a path to your TTS dataset directory and checks if each TXT file have a matching (same filename) WAV file.
Outputs success message or lists files without matches. 
Example of usage:
```bash
python scripts/match_txt_wav.py {PATH_TO_INPUT_DIR}
```


## Basic transcription cleaning
If your dataset was automatically transcribed, you might want to do preliminary cleaning before manual validation - capitalize first letter, add "." at the end, if needed, etc.
```bash
pip install tqdm colorama
```
Examples:
```bash
python process_transcripts.py [INPUT_FOLDER] [OUTPUT_OPTION] [OPTIONAL_FLAGS]
```

-o, --output-folder <PATH>

Specifies a directory where the processed .txt files will be saved. If the destination folder does not exist, it will be created. If the destination folder exists but is not empty, the script will prompt you for confirmation before proceeding, as existing files could be overwritten. Using the input folder as the output folder is not allowed; use --overwrite for that purpose. Files whose content was not changed will be copied to the output folder as-is.
```bash
python process_transcripts.py raw_texts/ -o cleaned_texts/
```

--overwrite

Modifies the original .txt files in the input folder directly. This is an in-place operation. This action is irreversible. 
```bash
python process_transcripts.py raw_texts/ --overwrite
```

OPTIONAL FLAGS:

-l, --log-file <PATH>

Creates a log file at the specified <PATH> that lists the names of all .txt files whose content was modified by the script. If the file's content was cleaned up (e.g., punctuation fixed, capitalization changed), its name will be added to this log. If the file's content was already clean and required no changes, it will not be included in the log.
```bash
python process_transcripts.py raw_texts/ -o cleaned_texts/ -l changes.log
```

--no-audio-check

Disables the check for a corresponding audio file for each .txt file. By default, the script checks if a .txt file (e.g., ep01.txt) has a matching audio file (e.g., ep01.wav, ep01.mp3, etc.) in the same folder. If no audio file is found, it prints a WARNING. Using this flag will suppress those warnings, which is useful if your dataset only contains text files.
```bash
python process_transcripts.py raw_texts/ -o cleaned_texts/ --no-audio-check
```
