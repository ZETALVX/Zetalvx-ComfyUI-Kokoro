import os
import random
import subprocess
import uuid

import torchaudio


KOKORO_PYTHON = "/home/theboss/ai/kokoro-test/.venv/bin/python"
KOKORO_SCRIPT = "/home/theboss/ai/kokoro-test/kokoro_generate.py"
COMFY_OUTPUT_DIR = "/home/theboss/ai/ComfyUI/output"


ALL_VOICES = [
    "af_heart",
    "af_alloy",
    "af_aoede",
    "af_bella",
    "af_jessica",
    "af_kore",
    "af_nicole",
    "af_nova",
    "af_river",
    "af_sarah",
    "af_sky",

    "am_adam",
    "am_echo",
    "am_eric",
    "am_fenrir",
    "am_liam",
    "am_michael",
    "am_onyx",
    "am_puck",
    "am_santa",

    "bf_alice",
    "bf_emma",
    "bf_isabella",
    "bf_lily",

    "bm_daniel",
    "bm_fable",
    "bm_george",
    "bm_lewis",

    "ef_dora",
    "em_alex",
    "em_santa",

    "ff_siwis",

    "hf_alpha",
    "hf_beta",
    "hm_omega",
    "hm_psi",

    "if_sara",
    "im_nicola",

    "jf_alpha",
    "jf_gongitsune",
    "jf_nezumi",
    "jf_tebukuro",
    "jm_kumo",

    "pf_dora",
    "pm_alex",
    "pm_santa",

    "zf_xiaobei",
    "zf_xiaoni",
    "zf_xiaoxiao",
    "zf_xiaoyi",

    "zm_yunjian",
    "zm_yunxi",
    "zm_yunxia",
    "zm_yunyang",
]


MALE_PREFIXES = ("am_", "bm_", "em_", "hm_", "im_", "jm_", "pm_", "zm_")
FEMALE_PREFIXES = ("af_", "bf_", "ef_", "ff_", "hf_", "if_", "jf_", "pf_", "zf_")


MALE_VOICES = [v for v in ALL_VOICES if v.startswith(MALE_PREFIXES)]
FEMALE_VOICES = [v for v in ALL_VOICES if v.startswith(FEMALE_PREFIXES)]


LANGUAGES = [
    "en",
    "en-us",
    "en-gb",
    "it",
    "fr",
    "es",
    "pt",
    "pt-br",
    "hi",
    "ja",
    "zh",
    "zh-cn",
]


def _sanitize_filename(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
    return safe.strip("_") or "zetalvx_kokoro_output"


def _load_wav_as_comfy_audio(wav_path: str):
    waveform, sample_rate = torchaudio.load(wav_path)

    if waveform.ndim == 2:
        waveform = waveform.unsqueeze(0)

    return {
        "waveform": waveform,
        "sample_rate": sample_rate,
    }


class ZetalvxKokoroGenerate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "voice_mode": (["selected", "male_random", "female_random"], {
                    "default": "selected"
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, this is a test generated with Kokoro inside ComfyUI"
                }),
                "language": (LANGUAGES, {
                    "default": "en"
                }),
                "voice": (ALL_VOICES, {
                    "default": "af_heart"
                }),
                "speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.05,
                }),
                "output_name": ("STRING", {
                    "default": "zetalvx_kokoro_output"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "AUDIO")
    RETURN_NAMES = ("audio_path", "selected_voice", "audio")
    FUNCTION = "generate"
    CATEGORY = "ZetaLvx/Audio"
    OUTPUT_NODE = True

    def generate(self, voice_mode, text, language, voice, speed, output_name):
        if not os.path.exists(KOKORO_PYTHON):
            raise FileNotFoundError(f"Kokoro python not found: {KOKORO_PYTHON}")

        if not os.path.exists(KOKORO_SCRIPT):
            raise FileNotFoundError(f"Kokoro script not found: {KOKORO_SCRIPT}")

        if voice_mode == "male_random":
            selected_voice = random.choice(MALE_VOICES)
        elif voice_mode == "female_random":
            selected_voice = random.choice(FEMALE_VOICES)
        else:
            selected_voice = voice

        safe_name = _sanitize_filename(output_name)
        unique_id = uuid.uuid4().hex[:8]
        out_path = os.path.join(COMFY_OUTPUT_DIR, f"{safe_name}_{unique_id}.wav")

        cmd = [
            KOKORO_PYTHON,
            KOKORO_SCRIPT,
            "--text", text,
            "--language", language,
            "--voice", selected_voice,
            "--speed", str(speed),
            "--out", out_path,
        ]

        print("[ZetalvxKokoro] Running:")
        print(" ".join(f'"{x}"' if " " in x else x for x in cmd))
        print(f"[ZetalvxKokoro] voice_mode: {voice_mode}")
        print(f"[ZetalvxKokoro] selected_voice: {selected_voice}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("[ZetalvxKokoro STDOUT]")
        print(result.stdout)

        if result.returncode != 0:
            print("[ZetalvxKokoro STDERR]")
            print(result.stderr)
            raise RuntimeError(f"Kokoro generation failed:\n{result.stderr}")

        if not os.path.exists(out_path):
            raise FileNotFoundError(f"Kokoro finished but output file was not found: {out_path}")

        audio = _load_wav_as_comfy_audio(out_path)

        return (out_path, selected_voice, audio)


NODE_CLASS_MAPPINGS = {
    "ZetalvxKokoroGenerate": ZetalvxKokoroGenerate
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZetalvxKokoroGenerate": "Zetalvx Kokoro Generate Audio"
}
