# Live Transcription with Whisper.cpp

This project provides a simple way to transcribe meetings in near real-time using OpenAI's Whisper model via `whisper.cpp`. It captures microphone input, processes audio in chunks, and writes transcriptions into a `.srt` subtitle file compatible with VLC or other media players.

## Features

- Live audio transcription from your microphone.
- Export to `.srt` format (standard subtitle format).
- Adjustable chunk duration for transcription.
- Fast CPU-based transcription using `whisper.cpp`.

## Requirements

### System Dependencies

- `ffmpeg`
- C++ compiler
- Python 3.7+
- `whisper.cpp` compiled locally

### Python Dependencies

Install required Python packages:

```bash
pip install sounddevice numpy
```

## Setup

1. Clone and build `whisper.cpp`:
```bash
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make
```

2. Download a model (e.g., `base.en`):
```bash
./models/download-ggml-model.sh base.en
```

3. Run the live transcription script (see `live_transcribe.py`).

## Usage

```bash
python live_transcribe.py
```

This will:
- Start capturing audio from your default input device.
- Transcribe every 5 seconds.
- Append each chunk as subtitles in `live_transcript.srt`.

Stop with `Ctrl+C`.

## License

MIT License. Based on [whisper.cpp](https://github.com/ggerganov/whisper.cpp) by Georgi Gerganov.
