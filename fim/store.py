# fim/store.py
import json
from pathlib import Path

class BaselineStore:
    def __init__(self, baseline_file="baseline.json"):
        self.baseline_file = Path(baseline_file)
        self.hashes = {}
        self._load()

    def _load(self):
        if self.baseline_file.exists():
            try:
                with open(self.baseline_file, "r", encoding="utf-8") as f:
                    self.hashes = json.load(f)
            except Exception as e:
                print(f"[!] Failed to load baseline file: {e}")
                self.hashes = {}
        else:
            self.hashes = {}

    def save(self):
        try:
            with open(self.baseline_file, "w", encoding="utf-8") as f:
                json.dump(self.hashes, f, indent=4)
        except Exception as e:
            print(f"[!] Failed to save baseline file: {e}")

    def get_hash(self, filepath):
        return self.hashes.get(filepath)

    def set_hash(self, filepath, filehash):
        self.hashes[filepath] = filehash
        self.save()

    def remove(self, filepath):
        if filepath in self.hashes:
            del self.hashes[filepath]
            self.save()
