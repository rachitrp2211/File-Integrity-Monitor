# utils.py
import json
import hashlib
import os

def compute_hash(file_path, algorithm="sha256"):
    """Compute hash of a file."""
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def load_baseline(baseline_file):
    """Load baseline JSON file."""
    if not os.path.exists(baseline_file):
        return {}
    with open(baseline_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_baseline(store, baseline_file):
    """Save baseline JSON file."""
    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=4)
