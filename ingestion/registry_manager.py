import json
import os
import uuid
from datetime import datetime

REGISTRY_PATH = "data/registry.json"


def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"documents": []}

    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(registry_data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry_data, f, indent=4)


def get_active_documents():
    registry = load_registry()
    active_docs = []

    for doc in registry["documents"]:
        if doc.get("active", False):
            active_docs.append({
                "id": doc["id"],
                "university": doc["university"],
                "file_path": doc["file_path"],
                "version_date": doc["version_date"]
            })

    return active_docs


def find_by_hash(file_hash):
    registry = load_registry()

    for doc in registry["documents"]:
        if doc["hash"] == file_hash:
            return doc

    return None


def deactivate_previous_versions(university_name):
    registry = load_registry()

    for doc in registry["documents"]:
        if doc["university"] == university_name:
            doc["active"] = False

    save_registry(registry)


def add_new_document(university_name, source_url, file_hash, file_path):
    registry = load_registry()

    # Deactivate older versions
    deactivate_previous_versions(university_name)

    new_entry = {
        "id": str(uuid.uuid4()),
        "university": university_name,
        "source_url": source_url,
        "hash": file_hash,
        "version_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "active": True,
        "file_path": file_path
    }

    registry["documents"].append(new_entry)
    save_registry(registry)

    return new_entry