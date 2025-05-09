import hashlib
import os

# Store hashes to check for unauthorized modifications
hash_store = {}

def compute_hash(path):
    """Compute SHA-256 hash of a file."""
    if not os.path.isfile(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def verify_file(path):
    """Verify file integrity by comparing its hash to the stored one."""
    current_hash = compute_hash(path)
    if current_hash is None:
        return False
    if path not in hash_store:
        hash_store[path] = current_hash
        return True
    return hash_store[path] == current_hash
