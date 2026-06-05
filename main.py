"""OCR helper for detecting promotional codes in a configured screen region.

The script captures a region of the screen, runs Tesseract OCR against it, and sends a newly
detected code through a local macOS Shortcut. It is a personal automation experiment, not a
production service.
"""

import os
import time
from subprocess import call

import imageio
import mss
import pyperclip
import pytesseract

COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
SCREENSHOT_FILE = "screenshot.png"
SHORTCUT_NAME = "ChipotleBurrito"

sent_code = ""


def capture_screenshot(left, top, width, height, output_file):
    """Capture a rectangular screen region to an image file."""
    with mss.mss() as screen:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        screenshot = screen.grab(monitor)
        imageio.imwrite(output_file, screenshot)


def extract_text_from_screenshot(image_path):
    """Run OCR on the saved screenshot."""
    return pytesseract.image_to_string(image_path)


def process_screenshot(left, top, width, height):
    """Capture, read, and then remove the temporary screenshot."""
    try:
        capture_screenshot(left, top, width, height, SCREENSHOT_FILE)
        return extract_text_from_screenshot(SCREENSHOT_FILE)
    finally:
        if os.path.exists(SCREENSHOT_FILE):
            os.remove(SCREENSHOT_FILE)


def make_single_line(text):
    return text.replace("\n", " ").replace("\r", " ")


def send_code_to_shortcut(code):
    """Send each detected code only once."""
    global sent_code

    if sent_code == code:
        print("Code already sent")
        return

    sent_code = code
    call(["shortcuts", "run", SHORTCUT_NAME])
    print("Code sent")


def extract_code(text):
    start_word = "text"
    end_word = "to"

    start_index = text.find(start_word)
    if start_index == -1:
        return None

    stop_index = text.find(end_word, start_index + len(start_word))
    if stop_index == -1:
        return None

    return text[start_index + len(start_word):stop_index].strip().upper()


def main():
    capture_area_left = 100
    capture_area_top = 700
    capture_area_width = 700
    capture_area_height = 400

    while True:
        text = process_screenshot(
            capture_area_left,
            capture_area_top,
            capture_area_width,
            capture_area_height,
        )
        code = extract_code(make_single_line(text).lower())

        if code:
            pyperclip.copy(code)
            print(f"{COLOR_GREEN}{code}{COLOR_RESET} copied to clipboard")
            send_code_to_shortcut(code)

        time.sleep(3)


if __name__ == "__main__":
    main()
