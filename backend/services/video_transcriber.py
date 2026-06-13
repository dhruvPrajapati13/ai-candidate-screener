import os
import subprocess
import torch
from pathlib import Path
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
import numpy as np

# ── Load model once ───────────────────────────────────────
_transcriber = None

def _get_transcriber():
    global _transcriber
    if _transcriber is None:
        print("⏳ Loading Hinglish Whisper model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Use float32 on CPU (float16 causes errors on CPU)
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            "shunyalabs/zero-stt-hinglish",
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained("shunyalabs/zero-stt-hinglish")

        _transcriber = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )
        print(f"✅ Hinglish model loaded on {device}")
    return _transcriber


# ── Main entry point ──────────────────────────────────────
def transcribe_video(video_path: str) -> str:
    audio_path = _extract_audio(video_path)
    try:
        transcript = _transcribe_audio(audio_path)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    return transcript


# ── Step 1: Extract audio ─────────────────────────────────
def _extract_audio(video_path: str) -> str:
    audio_path = str(Path(video_path).with_suffix(".wav"))
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="ignore")
        raise RuntimeError(f"ffmpeg audio extraction failed:\n{error}")
    if not os.path.exists(audio_path):
        raise RuntimeError("ffmpeg ran but produced no output file.")
    return audio_path


# ── Step 2: Transcribe ────────────────────────────────────
def _transcribe_audio(audio_path: str) -> str:
    transcriber = _get_transcriber()

    result = transcriber(
        audio_path,
        chunk_length_s=30,       # smaller chunks = faster processing on CPU
        stride_length_s=2,       # reduced overlap
        generate_kwargs={
            "task": "translate",         # Hindi/Hinglish → English
            "language": "hindi",
            "num_beams": 4,              # greedy decoding = much faster (vs beam=5)
            "do_sample": False,
        },
        return_timestamps=False,
    )

    transcript = result["text"].strip()
    return transcript