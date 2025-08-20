import os
import sys

try:
    import openai
except ImportError:
    print("Please install openai package with: pip install openai")
    sys.exit(1)

def read_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def summarize_text(text, model="gpt-3.5-turbo"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("❌ OPENAI_API_KEY not set in environment variables.")
        return None

    print("📚 Sending transcript to GPT for summarization...")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the following class transcript into a list of bullet points and a concise paragraph overview."},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']

def main():
    if len(sys.argv) < 2:
        print("Usage: python summarize_transcript.py <transcript_file.txt>")
        return

    transcript_file = sys.argv[1]
    transcript = read_transcript(transcript_file)

    summary = summarize_text(transcript)
    if summary:
        out_file = os.path.splitext(transcript_file)[0] + "_summary.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"✅ Summary saved to {out_file}")

if __name__ == "__main__":
    main()
