import os
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    sys.exit("GROQ_API_KEY is missing. Check backend/.env.")

if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/test_groq.py <path-to-audio-file>")

audio_path = sys.argv[1]

client = Groq(api_key=api_key)

with open(audio_path, "rb") as audio_file:
    result = client.audio.transcriptions.create(
        file=(os.path.basename(audio_path), audio_file.read()),
        model="whisper-large-v3-turbo",
        response_format="verbose_json",
    )

print("Transcript:")
print(result.text)
print()
print(f"Duration: {getattr(result, 'duration', 'unknown')} seconds")