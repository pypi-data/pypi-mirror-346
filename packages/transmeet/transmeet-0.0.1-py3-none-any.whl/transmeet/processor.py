import argparse
from pathlib import Path
from datetime import datetime
import configparser
from pydub import AudioSegment
from groq import Groq

from transmeet.utils.general_utils import (
    extract_datetime_from_filename,
    get_logger,
    ROOT_DIR,
)

from transmeet.utils.audio_utils import (
    get_audio_size_mb,
    split_audio_by_target_size,
)

from transmeet.clients.llm_client import generate_meeting_minutes
from transmeet.clients.transcription_client import transcribe_with_groq, transcribe_with_google

CONFIG_FILE = ROOT_DIR / "transmeet/config.ini"
logger = get_logger(__name__)



def load_config(config_path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def handle_transcription(config, audio: AudioSegment, file_size_mb: float) -> str:
    use_groq = config["transcription"].getboolean("use_groq")

    if use_groq:
        model = config["transcription"]["groq_model"]
        chunk_target_mb = config["transcription"].getint("groq_chunk_target_mb")
        api_key = config["api"]["GROQ_API_KEY"]

        if file_size_mb > chunk_target_mb:
            logger.info(f"File is {file_size_mb:.2f} MB — splitting into chunks...")
            chunks = split_audio_by_target_size(audio, chunk_target_mb)
        else:
            chunks = [audio]
            logger.info("Audio is small enough — using Groq directly...")

        return transcribe_with_groq(chunks, model, api_key)

    logger.info("Using Google Speech Recognition...")
    return transcribe_with_google(audio)


def save_transcription(transcript: str, transcription_path: Path) -> Path:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = transcription_path / f"transcription_{timestamp}.txt"
    path.write_text(transcript, encoding="utf-8")
    logger.info(f"Saved transcription to {path}")
    return path


def save_meeting_minutes(transcript: str, config, meeting_datetime: datetime, meeting_minutes_path: Path) -> Path:
    client = Groq(api_key=config["api"]["GROQ_API_KEY"])
    model = config["api"]["GROQ_MODEL_LLM"]
    minutes = generate_meeting_minutes(transcript, client, model, meeting_datetime)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = meeting_minutes_path / f"meeting_minutes_{timestamp}.md"
    path.write_text(minutes, encoding="utf-8")
    logger.info(f"Saved meeting minutes to {path}")
    return path


def generate_meeting_transcript_and_minutes(audio_path_str: str):
    try:
        logger.info("Starting transcription and meeting minutes generation...")
        logger.debug(f"Audio path: {audio_path_str}")
        AUDIO_DIR = Path(audio_path_str).parent

        TRANSCRIPTION_PATH = AUDIO_DIR / "data/transcriptions"
        MEETING_MINUTES_PATH = AUDIO_DIR / "data/meeting_minutes"

        TRANSCRIPTION_PATH.mkdir(parents=True, exist_ok=True)
        MEETING_MINUTES_PATH.mkdir(parents=True, exist_ok=True)
        
        config = load_config(CONFIG_FILE)
        audio_path = Path(audio_path_str)
        
        audio = AudioSegment.from_file(audio_path)
        file_size_mb = get_audio_size_mb(audio)

        transcript = handle_transcription(config, audio, file_size_mb)
        save_transcription(transcript, TRANSCRIPTION_PATH)

        meeting_datetime = extract_datetime_from_filename(audio_path.name)
        save_meeting_minutes(transcript, config, meeting_datetime, MEETING_MINUTES_PATH)

    except Exception as e:
        logger.exception("❌ Unexpected error during processing.")
