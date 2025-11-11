# utils.py
import os, sys, datetime
from pathlib import Path

def ensure_dir(d):
    Path(d).mkdir(parents=True, exist_ok=True)

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def save_screenshot(page, path):
    try:
        page.screenshot(path=path, full_page=True)
    except Exception as e:
        print("[ERROR] Screenshot failed:", e)

def log_info(msg):
    print(f"[INFO] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
