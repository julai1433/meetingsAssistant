import sounddevice as sd
import numpy as np
import tempfile
import time
import os
from transcriber.srt_writer import write_srt_segment
from transcriber.whisper_cpp_runner import transcribe_chunk

CHUNK_DURATION = 5  # seconds
SAMPLE_RATE = 16000
CHANNELS = 1
SRT_FILE = "live_transcript.srt"
MODEL_PATH = "./whisper.cpp/models/ggml-base.en.bin"
WHISPER_MAIN = "./whisper.cpp/main"

segment_counter = 1
start_time = time.time()

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def callback(indata, frames, time_info, status):
    global segment_counter, start_time

    audio_data = indata[:, 0]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        wav_path = temp_wav.name
        from scipy.io.wavfile import write
        write(wav_path, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))

    print("🔍 Transcribing chunk...")
    segments = transcribe_chunk(wav_path, MODEL_PATH, WHISPER_MAIN)

    for seg in segments:
        abs_start = start_time + seg['start']
        abs_end = start_time + seg['end']
        write_srt_segment(SRT_FILE, segment_counter, abs_start, abs_end, seg['text'])
        segment_counter += 1

    os.remove(wav_path)
    start_time += CHUNK_DURATION

print("🎙️ Recording... Press Ctrl+C to stop.")
try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback,
                        blocksize=int(SAMPLE_RATE * CHUNK_DURATION), dtype='float32'):
        while True:
            sd.sleep(int(CHUNK_DURATION * 1000))
except KeyboardInterrupt:
    print("🛑 Transcription stopped.")
