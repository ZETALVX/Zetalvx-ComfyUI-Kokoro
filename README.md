# Zetalvx-ComfyUI-Kokoro

A ComfyUI custom node and local integration for running **Kokoro TTS** inside modular AI workflows.

This repository is part of the **ZETALVX AI Automation Lab** ecosystem: local-first AI pipelines, reproducible environments, automation workflows and modular multimedia generation systems.

---

## Overview

`Zetalvx-ComfyUI-Kokoro` provides a bridge between **ComfyUI** and a dedicated local **Kokoro TTS** environment.

The node is designed to launch Kokoro generation externally while keeping dependencies isolated from the main ComfyUI installation.

This setup is especially useful for:

- local text-to-speech generation
- modular narration workflows
- AI video pipelines
- automation systems
- local-only multimedia generation
- reproducible environments with separated dependencies

---

## Features

- ComfyUI custom node for Kokoro TTS
- Dedicated external Python environment support
- Local speech synthesis
- WAV output generation
- Modular workflow integration
- Designed for local-first AI systems
- Easy integration with video, subtitle and narration pipelines

---

## Repository Structure

Recommended structure:

```text
Zetalvx-ComfyUI-Kokoro/
├── README.md
├── LICENSE
├── requirements.txt
├── nodes/
│   └── zetalvx_kokoro_node.py
├── scripts/
│   └── kokoro_generate.py
└── examples/
    └── workflow_example.json
```

Depending on implementation, file names may vary slightly.

---

## Recommended Setup

Recommended architecture:

1. ComfyUI environment
2. Dedicated Kokoro environment

This avoids dependency conflicts and keeps the installation cleaner and easier to maintain.

Example:

```bash
/home/theboss/ai/ComfyUI/venv311
/home/theboss/ai/kokoro/.venv
```

The ComfyUI node calls the external Kokoro script using the Kokoro environment Python interpreter.

---

## Installation

### 1. Clone the repository into ComfyUI custom nodes

```bash
cd /home/theboss/ai/ComfyUI/custom_nodes
git clone https://github.com/ZETALVX/Zetalvx-ComfyUI-Kokoro.git
```

Restart ComfyUI after installation.

---

### 2. Prepare the Kokoro environment

Example:

```bash
mkdir -p /home/theboss/ai/kokoro
cd /home/theboss/ai/kokoro

python3 -m venv .venv
source .venv/bin/activate
```

Install Kokoro and required dependencies following the official setup instructions.

If a `requirements.txt` is included:

```bash
pip install -r requirements.txt
```

---

## ComfyUI Node Usage

Inside ComfyUI, add the Kokoro node from this repository.

Typical inputs may include:

| Input | Description |
|---|---|
| `text` | Text to synthesize |
| `kokoro_python` | Full path to Kokoro environment Python |
| `script_path` | Full path to Kokoro generation script |
| `voice` | Voice preset or speaker |
| `language` | Language selection |
| `speed` | Speech speed |
| `output_dir` | Output directory for generated audio |

Example paths:

```text
kokoro_python:
/home/theboss/ai/kokoro/.venv/bin/python

script_path:
/home/theboss/ai/kokoro/kokoro_generate.py

output_dir:
/home/theboss/ai/ComfyUI/output/kokoro
```

---

## Example CLI Test

Before using the node inside ComfyUI, test Kokoro directly from terminal.

Example:

```bash
source /home/theboss/ai/kokoro/.venv/bin/activate

python /home/theboss/ai/kokoro/kokoro_generate.py \
  --text "This is a Kokoro local TTS test." \
  --output /home/theboss/ai/ComfyUI/output/kokoro/test.wav
```

If the terminal test works correctly, the ComfyUI integration should also work.

---

## Example Workflow

Typical workflow:

```text
Text Prompt
   ↓
Kokoro TTS Node
   ↓
Generated Audio
   ↓
Video / Narration / Multimedia Pipeline
```

Can be combined with:

- local LLMs
- subtitle generation
- image generation
- video generation
- animation workflows
- local AI automation systems

---

## Troubleshooting

### Node does not appear in ComfyUI

Check the repository location:

```bash
/home/theboss/ai/ComfyUI/custom_nodes/
```

Restart ComfyUI and inspect terminal logs for import errors.

---

### Kokoro works externally but not inside ComfyUI

Verify the Python path used by the node:

```bash
/home/theboss/ai/kokoro/.venv/bin/python
```

Avoid mixing environments unless intentionally configured.

---

### Audio file is not generated

Check:

- output directory permissions
- script path correctness
- model download completion
- CLI test outside ComfyUI
- external environment dependencies

---

### Dependency issues

Use a dedicated Kokoro environment.

This repository is designed around isolated environments to improve stability and reproducibility.

---

## Notes

This repository acts as an integration layer between ComfyUI and Kokoro TTS.

The node launches external scripts and returns generated audio paths back into the workflow.

This architecture helps maintain modular and stable AI environments.

---

## Credits

- Kokoro TTS project and contributors
- ComfyUI project and contributors
- ZETALVX AI Automation Lab

---

## License

Released under the license included in the `LICENSE` file.

Always verify the licenses associated with:

- pretrained models
- voices
- datasets
- external dependencies

Commercial usage depends on the licenses of the underlying models and datasets.

---

## Author

Created by **ZETALVX – AI Automation Lab**

Local AI workflows, automation pipelines, ComfyUI integrations and open-source experiments.
