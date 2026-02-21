import os
import hashlib
from datetime import datetime

SYLLABI_STORAGE_DIR = "data/syllabi"


def ensure_storage_directory():
    if not os.path.exists(SYLLABI_STORAGE_DIR):
        os.makedirs(SYLLABI_STORAGE_DIR)


def compute_sha256(file_bytes):
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()


def generate_versioned_filename(university_name, extension=".pdf"):
    """
    Example:
    IIT Delhi CSE -> iit_delhi_cse_2025_01_15.pdf
    """
    clean_name = (
        university_name.lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    date_str = datetime.utcnow().strftime("%Y_%m_%d")
    filename = f"{clean_name}_{date_str}{extension}"

    return filename


def save_file(file_bytes, university_name, extension=".pdf"):
    """
    Saves file safely with version-based naming.
    Returns full file path.
    """
    ensure_storage_directory()

    filename = generate_versioned_filename(university_name, extension)
    file_path = os.path.join(SYLLABI_STORAGE_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path