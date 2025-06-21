from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

from llm.prompt_builder import generate_response


def extract_video_id(youtube_url):
    """
    Extracts the video ID from a YouTube URL.
    """
    parsed = urlparse(youtube_url)
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname in ['youtu.be']:
        return parsed.path[1:]
    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(video_id, language='en'):
    """
    Retrieves the transcript for a YouTube video.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except TranscriptsDisabled:
        return "❌ Transcript is disabled for this video."
    except NoTranscriptFound:
        return "❌ No transcript available for this video."
    except Exception as e:
        return f"❌ Error fetching transcript: {e}"


def build_prompt(transcript_text: str, question: str):
    """
    Builds a prompt for the LLM based on the transcript.
    """
    return f"{question}\n\nVideo Transcript:\n\n{transcript_text}"


def analyze(youtube_url: str, question: str):
    """
    Main analysis function for YouTube content.
    """
    print(f"▶️ Analyzing YouTube URL: {youtube_url}")
    video_id = extract_video_id(youtube_url)

    print("⏬ Fetching transcript...")
    transcript = get_transcript(video_id)

    if transcript.startswith("❌"):
        return transcript

    prompt = build_prompt(transcript[:5000], question)  # Limit to 5000 chars
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
