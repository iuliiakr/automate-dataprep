# automate-dataprep
Useful Python scripts to automate data processing for TTS and STS ML projects.

## Check duration distribution for your dataset [scripts/analyze_wav_lengths.py]
For TTS conversions duration of audio files in your training datasets matters.
This script outputs total number of files processed, total duration, average duration, shortest and longest (in seconds) and also a PNG file with a distribution of audio durations in the input directory.
Example of usage:
```bash
python3 ../scripts/analyze_wav_lengths.py {PATH_TO_INPUT_DIR}
```
