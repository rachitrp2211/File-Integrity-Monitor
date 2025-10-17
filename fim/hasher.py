# fim/hasher.py
import hashlib
from pathlib import Path

def compute_hash(path: Path, algo: str = "sha256", chunk_size: int = 8192) -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()
