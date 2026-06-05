# CFinalsBot

Experimental OCR automation script for detecting promotional codes from a screen region and
sending them through a configured macOS Shortcut.

## Important

This was a personal automation experiment and is not intended for contest abuse, production use,
or unattended messaging.

## Requirements

- macOS with the `shortcuts` CLI available
- A Shortcut named `ChipotleBurrito`
- Tesseract OCR installed locally
- Python dependencies from `requirements.txt`

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The capture area is configured near the bottom of `main.py`; adjust it for the screen region
that should be scanned.
