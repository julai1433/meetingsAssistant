import os
import sys
import tempfile
import subprocess
from transcriber.whisper_cpp_runner import transcribe_chunk

def extract_audio_from_video(video_path, output_wav_path):
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        "-f", "wav",
        output_wav_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python transcribe_video.py <video_file>")
        return

    video_file = sys.argv[1]
    if not os.path.exists(video_file):
        print(f"❌ File not found: {video_file}")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        wav_path = tmp_audio.name

    print("🎞️ Extracting audio from video...")
    extract_audio_from_video(video_file, wav_path)

    print("🧠 Transcribing with whisper.cpp...")
    segments = transcribe_chunk(
        audio_path=wav_path,
        model_path="./whisper.cpp/models/ggml-base.en.bin",
        whisper_main_path="./whisper.cpp/main"
    )
    os.remove(wav_path)

    # Save to text file
    output_txt = os.path.splitext(video_file)[0] + ".txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(seg['text'].strip() + "\n")

    print(f"✅ Transcription saved to {output_txt}")

if __name__ == "__main__":
    main()
