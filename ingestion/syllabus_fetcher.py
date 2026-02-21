import requests
from ingestion.storage_manager import compute_sha256, save_file
from ingestion.registry_manager import find_by_hash, add_new_document

# 🔹 Controlled academic sources
TRUSTED_SOURCES = {
    "Kerala University Mathematics 2025":
    "https://cdnbbsr.s3waas.gov.in/s388a839f2f6f1427879fc33ee4acf4f66/uploads/2025/12/20251213831928732.pdf"
}


def fetch_syllabus(source_key):
    """
    Fetch syllabus from trusted sources,
    perform hash-based deduplication,
    register new version if updated.
    """

    if source_key not in TRUSTED_SOURCES:
        return {"status": "error", "message": "Invalid source key"}

    url = TRUSTED_SOURCES[source_key]

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        return {"status": "error", "message": f"Download failed: {str(e)}"}

    file_bytes = response.content
    file_hash = compute_sha256(file_bytes)

    # 🔹 Check for duplicate via hash
    existing_doc = find_by_hash(file_hash)
    if existing_doc:
        return {
            "status": "duplicate",
            "message": "Syllabus already exists in registry",
            "document_id": existing_doc["id"]
        }

    # 🔹 Save file locally (versioned)
    file_path = save_file(file_bytes, source_key, extension=".pdf")

    # 🔹 Register new version
    new_doc = add_new_document(
        university_name=source_key,
        source_url=url,
        file_hash=file_hash,
        file_path=file_path
    )

    return {
        "status": "success",
        "message": "New syllabus version ingested",
        "document_id": new_doc["id"]
    }