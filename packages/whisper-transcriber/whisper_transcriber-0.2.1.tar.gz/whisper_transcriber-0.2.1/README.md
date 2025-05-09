# Whisper Transcriber

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whisper-transcriber?logo=python&logoColor=white)](https://pypi.org/project/whisper-transcriber/)

A Python library for transcribing audio files using Whisper models with intelligent silence detection and segmentation.

## Installation

```bash
pip install whisper-transcriber
```

## Requirements

- Python 3.7 or higher
- ffmpeg and ffprobe installed on your system

## Features

- Intelligent silence detection for natural segmentation
- Adaptive audio analysis for optimal threshold detection
- Memory-efficient processing of large audio files
- Parallel processing for faster silence detection
- Two-pass transcription for improved segment boundaries
- Enhanced generation parameters for controlling output quality
- High-quality transcription using Whisper models
- Support for various audio formats
- Optional SRT subtitle output
- Control over transcript output (quiet mode, JSON output)
- Verbose/silent operation modes

## Usage

### Command Line

```bash
# Basic usage
whisper-transcribe audio_file.mp3

# Advanced usage
whisper-transcribe audio_file.mp3 -m openai/whisper-small \
  --min-segment 5 \
  --max-segment 15 \
  --silence-duration 0.2 \
  --sample-rate 16000 \
  --batch-size 8 \
  --normalize \
  --hf-token YOUR_HF_TOKEN \
  --no-timestamps

# Memory-efficient processing with parallel jobs
whisper-transcribe long_audio.mp3 --chunk-size 900 --parallel-jobs 4

# Enhanced generation with two-pass transcription
whisper-transcribe podcast.mp3 --two-pass --temperature 0.1 --beam-size 8

# Run in quiet mode (no transcript printing during processing)
whisper-transcribe audio_file.mp3 --quiet

# Output results as JSON
whisper-transcribe audio_file.mp3 --json
```

#### Available Arguments:

- `input`: Input audio file or directory (required)
- `-o, --output`: Output file path (optional)
- `-m, --model`: Whisper model to use (default: openai/whisper-small)
- `--hf-token`: HuggingFace API token
- `--min-segment`: Minimum segment length in seconds (default: 5)
- `--max-segment`: Maximum segment length in seconds (default: 15)
- `--silence-duration`: Minimum silence duration in seconds (default: 0.2)
- `--sample-rate`: Audio sample rate (default: 16000)
- `--batch-size`: Batch size for transcription (default: 8)
- `--normalize`: Normalize audio volume
- `--no-text-normalize`: Skip text normalization
- `--no-timestamps`: Don't print timestamps during processing
- `--quiet`: Run in quiet mode (suppress transcript printing)
- `--json`: Output results as JSON instead of text
- `--chunk-size`: Size of audio chunks in seconds for memory-efficient processing (default: 600)
- `--parallel-jobs`: Number of parallel jobs for silence detection (default: automatic)
- `--two-pass`: Use two-pass transcription for improved segment boundaries
- `--temperature`: Temperature for sampling, higher values make output more random (default: 0.0)
- `--top-p`: Top-p sampling probability threshold (default: None)
- `--beam-size`: Beam size for beam search (default: 5)

### Python Library

```python
from whisper_transcriber import WhisperTranscriber

# Initialize the transcriber
transcriber = WhisperTranscriber(model_name="openai/whisper-small", hf_token="YOUR_HF_TOKEN")

# Basic transcription
results = transcriber.transcribe(
    "audio_file.mp3",
    min_segment=5,
    max_segment=15,
    silence_duration=0.2,
    sample_rate=16000,
    batch_size=8,
    normalize=True,
    normalize_text=True,
    print_timestamps=True,
    verbose=True
)

# Advanced transcription with memory optimization and enhanced generation
results = transcriber.transcribe(
    "long_audio.mp3",
    output="transcript.srt",
    min_segment=5,
    max_segment=15,
    silence_duration=0.2,
    sample_rate=16000,
    batch_size=8,
    normalize=True,
    normalize_text=True,
    print_timestamps=True,
    verbose=True,
    # New advanced parameters
    two_pass=True,              # Use two-pass transcription for better segments
    chunk_size=900,             # Process in 15-min chunks (memory efficient)
    parallel_jobs=4,            # Use 4 parallel processes for silence detection
    temperature=0.1,            # Slightly non-deterministic output
    top_p=0.95,                 # Nucleus sampling for more natural text
    beam_size=8                 # Larger beam search for better quality
)

# Access the transcription results manually
for i, segment in enumerate(results):
    print(f"\n[{segment['start']} --> {segment['end']}]")
    print(f"Segment {i+1}: {segment['transcript']}")
```

## Parameters Explained

- `model_name`: Which Whisper model to use (e.g., "openai/whisper-tiny", "openai/whisper-small", "openai/whisper-medium", "openai/whisper-large")
- `min_segment`: Minimum length in seconds for audio segments (shorter segments will be merged)
- `max_segment`: Maximum length in seconds for audio segments (longer segments will be split)
- `silence_duration`: How long a silence needs to be (in seconds) to be considered a natural break point
- `sample_rate`: Audio sample rate in Hz for processing
- `batch_size`: Number of segments to process at once (higher values use more memory but can be faster with GPU)
- `normalize`: Whether to normalize audio volume
- `normalize_text`: Whether to normalize transcription text
- `print_timestamps`: Whether to include timestamps when printing transcripts
- `verbose`: Whether to print processing information and transcripts during transcription

### Advanced Parameters

- `two_pass`: Use two-pass transcription to refine segment boundaries based on linguistic analysis
- `chunk_size`: Size of audio chunks in seconds for memory-efficient processing of large files
- `parallel_jobs`: Number of parallel jobs for silence detection (None for automatic)
- `temperature`: Controls randomness in generation (0.0 for deterministic, higher for more variety)
- `top_p`: Top-p probability threshold for nucleus sampling (between 0 and 1)
- `beam_size`: Beam size for beam search during generation (higher values = better quality but slower)

## License

MIT
