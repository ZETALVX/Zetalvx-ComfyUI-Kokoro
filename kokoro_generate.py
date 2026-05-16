import argparse
import os
import sys
from datetime import datetime

import numpy as np
import soundfile as sf
from kokoro import KPipeline


LANG_MAP = {
    "en-us": "a",
    "en": "a",
    "en-gb": "b",
    "es": "e",
    "fr": "f",
    "hi": "h",
    "it": "i",
    "ja": "j",
    "pt-br": "p",
    "pt": "p",
    "zh": "z",
    "zh-cn": "z",
}


DEFAULT_VOICES = {
    "en": "af_heart",
    "en-us": "af_heart",
    "en-gb": "bf_emma",
    "it": "if_sara",
    "fr": "ff_siwis",
    "es": "ef_dora",
    "pt": "pf_dora",
    "pt-br": "pf_dora",
    "hi": "hf_alpha",
    "ja": "jf_alpha",
    "zh": "zf_xiaobei",
    "zh-cn": "zf_xiaobei",
}


def normalize_language(language: str) -> str:
    language = language.strip().lower()
    if language not in LANG_MAP:
        raise ValueError(
            f"Unsupported language '{language}'. Supported: {', '.join(sorted(LANG_MAP.keys()))}"
        )
    return LANG_MAP[language]


def default_voice_for_language(language: str) -> str:
    language = language.strip().lower()
    return DEFAULT_VOICES.get(language, DEFAULT_VOICES.get(language.split("-")[0], "af_heart"))


def main():
    parser = argparse.ArgumentParser(description="External Kokoro TTS wrapper for ComfyUI")

    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--language", default="en", help="Language code, example: en, it, fr")
    parser.add_argument("--voice", default="", help="Kokoro voice, example: af_heart")
    parser.add_argument("--out", required=True, help="Output wav path")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--split_pattern", default=r"\n+", help="Text split regex")
    parser.add_argument("--cuda", action="store_true", help="Accepted for compatibility, Kokoro script may still run CPU depending on backend")

    args = parser.parse_args()

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    lang_code = normalize_language(args.language)
    voice = args.voice.strip() or default_voice_for_language(args.language)

    print("Kokoro wrapper started")
    print("Time:", datetime.now().isoformat())
    print("Language:", args.language)
    print("Kokoro lang_code:", lang_code)
    print("Voice:", voice)
    print("Speed:", args.speed)
    print("Output:", out_path)
    print("CUDA flag:", args.cuda)

    try:
        pipeline = KPipeline(lang_code=lang_code)

        generator = pipeline(
            args.text,
            voice=voice,
            speed=args.speed,
            split_pattern=args.split_pattern,
        )

        chunks = []

        for i, (graphemes, phonemes, audio) in enumerate(generator):
            print(f"Chunk {i}")
            print("Text:", graphemes)
            print("Phonemes:", phonemes)

            audio_np = np.asarray(audio, dtype=np.float32)
            chunks.append(audio_np)

        if not chunks:
            print("ERROR: Kokoro generated no audio chunks", file=sys.stderr)
            sys.exit(1)

        final_audio = np.concatenate(chunks)
        sf.write(out_path, final_audio, 24000)

    except Exception as e:
        print(f"ERROR: Kokoro generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: generated {out_path}")


if __name__ == "__main__":
    main()
