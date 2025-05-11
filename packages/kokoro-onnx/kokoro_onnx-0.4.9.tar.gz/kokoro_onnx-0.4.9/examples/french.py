"""
Usage:
1.
    Install uv from https://docs.astral.sh/uv/getting-started/installation
2.
    Copy this file to new folder
3.
    Download these files
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
4. Run
    uv venv --seed -p 3.12
    source .venv/bin/activate
    uv pip install -U kokoro-onnx soundfile 'misaki[en]'
    uv run main.py

For other languages read https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
"""

import soundfile as sf
from misaki import espeak
from misaki.espeak import EspeakG2P

from kokoro_onnx import Kokoro

# Misaki G2P with espeak-ng fallback
fallback = espeak.EspeakFallback(british=False)
g2p = EspeakG2P(language="fr-fr")

# Kokoro
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

# Phonemize
text = "On ne voit bien qu’avec le cœur. L’essentiel est invisible pour les yeux."
phonemes, _ = g2p(text)

# Create
samples, sample_rate = kokoro.create(phonemes, "ff_siwis", is_phonemes=True)

# Save
sf.write("audio.wav", samples, sample_rate)
print("Created audio.wav")
