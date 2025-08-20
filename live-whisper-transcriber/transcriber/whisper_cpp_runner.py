import subprocess
import json
import os
import tempfile

def transcribe_chunk(audio_path, model_path, whisper_main_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as output_file:
        json_path = output_file.name

    command = [
        whisper_main_path,
        "-m", model_path,
        "-f", audio_path,
        "-otxt", "-of", json_path,
        "-nt"
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    segments = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                segments.append({
                    "start": i * 5.0,
                    "end": (i + 1) * 5.0,
                    "text": line.strip()
                })
        os.remove(json_path)

    return segments
