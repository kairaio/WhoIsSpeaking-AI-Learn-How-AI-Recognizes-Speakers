from functools import lru_cache
from pathlib import Path

import numpy as np
import torch
import torchaudio
from speechbrain.inference.speaker import SpeakerRecognition


MODEL_SOURCE = "speechbrain/spkrec-ecapa-voxceleb"
MODEL_DIR = Path("models/spkrec-ecapa-voxceleb")


@lru_cache(maxsize=1)
def get_model() -> SpeakerRecognition:
    """
    Load the speaker recognition model once
    and reuse it for future requests.
    """

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    return SpeakerRecognition.from_hparams(
        source=MODEL_SOURCE,
        savedir=str(MODEL_DIR),
    )


def load_audio(audio_path: str) -> torch.Tensor:
    """
    Load an audio file and convert it to:
    - mono
    - 16 kHz sample rate
    """

    waveform, sample_rate = torchaudio.load(audio_path)

    if waveform.ndim != 2:
        raise ValueError("Unsupported audio format.")

    # Convert stereo/multi-channel audio to mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    target_sample_rate = 16000

    if sample_rate != target_sample_rate:
        waveform = torchaudio.functional.resample(
            waveform,
            orig_freq=sample_rate,
            new_freq=target_sample_rate,
        )

    return waveform


def extract_embedding(audio_path: str) -> np.ndarray:
    """
    Convert a voice recording into a normalized
    speaker embedding vector.
    """

    model = get_model()
    waveform = load_audio(audio_path)

    with torch.no_grad():
        embedding = model.encode_batch(waveform)

    embedding = (
        embedding
        .squeeze()
        .detach()
        .cpu()
        .numpy()
        .astype(np.float32)
    )

    norm = np.linalg.norm(embedding)

    if norm == 0:
        raise ValueError(
            "Could not create a valid speaker embedding."
        )

    return embedding / norm