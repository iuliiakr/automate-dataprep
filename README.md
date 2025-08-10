# automate-dataprep
Useful Python scripts to automate data processing for TTS and STS ML projects.

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

- Basic usage:
```bash
python process_transcripts.py raw_texts/ -o cleaned_texts/
```
- With logging:
```bash
python process_transcripts.py raw_texts/ -o cleaned_texts/ -l changes.log
```
- Overwriting Original Files
```bash
python process_transcripts.py raw_texts/ --overwrite
```
- Disabling the Audio Check
```bash
python process_transcripts.py raw_texts/ -o cleaned_texts/ --no-audio-check
```
