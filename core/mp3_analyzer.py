import os
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import tempfile
import whisper
from llm.prompt_builder import generate_response


def extract_metadata(file_path: str):
    """
    Extract MP3 tags like title, artist, album, etc.
    """
    audio = MP3(file_path, ID3=ID3)
    tags = audio.tags
    metadata = {}

    if tags:
        for key in tags.keys():
            metadata[key] = str(tags[key])
    else:
        metadata["info"] = "No ID3 metadata found."

    return metadata


def transcribe_audio(file_path: str, model_size="base"):
    """
    Transcribes speech from the MP3 using OpenAI Whisper.
    """
    print("🎙️ Transcribing audio with Whisper...")
    model = whisper.load_model(model_size)

    # Convert MP3 to WAV for Whisper
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        sound = AudioSegment.from_mp3(file_path)
        sound.export(temp_wav.name, format="wav")
        result = model.transcribe(temp_wav.name)
        os.remove(temp_wav.name)

    return result["text"]


def build_prompt(transcript: str, question: str, metadata=None):
    """
    Constructs a prompt for the LLM using metadata and transcription.
    """
    meta_info = "\n".join(f"{k}: {v}" for k, v in metadata.items()) if metadata else ""
    if question:
        return f"{question}\n\nMetadata:\n{meta_info}\n\nTranscript:\n{transcript}"
    else:
        return (
            f"Analyze the following audio transcript. Identify the topic, mood, tone, and any relevant keywords.\n\n"
            f"Metadata:\n{meta_info}\n\nTranscript:\n{transcript}"
        )


def analyze(file_path: str, question: str):
    """
    Main analysis function for MP3 files.
    """
    if not os.path.exists(file_path) or not file_path.endswith(".mp3"):
        raise ValueError("❌ Please provide a valid MP3 file.")

    print(f"🎧 Analyzing MP3 file: {file_path}")

    metadata = extract_metadata(file_path)
    transcript = transcribe_audio(file_path)

    if not transcript.strip():
        return "❌ No speech detected or transcription failed."

    prompt = build_prompt(transcript, question, metadata)
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
