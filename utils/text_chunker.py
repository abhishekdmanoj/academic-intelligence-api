import re


def chunk_by_units(text):
    """
    Primary strategy:
    - Split by UNIT headings if available

    Fallback:
    - Split by paragraph blocks if no UNIT headings found
    """

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Try to split by UNIT pattern
    pattern = r'(UNIT\s+\d+[:\-].*?)'
    splits = re.split(pattern, text, flags=re.IGNORECASE)

    chunks = []

    # If UNIT structure detected
    if len(splits) > 1:
        for i in range(1, len(splits), 2):
            unit_title = splits[i].strip()
            unit_content = splits[i + 1].strip() if i + 1 < len(splits) else ""

            chunks.append({
                "subject": None,
                "unit": unit_title,
                "text": unit_content
            })

        return chunks

    # 🔥 Fallback: paragraph chunking
    paragraphs = re.split(r'\.\s+', text)

    for idx, para in enumerate(paragraphs):
        para = para.strip()
        if len(para) > 100:  # ignore very small fragments
            chunks.append({
                "subject": None,
                "unit": f"Section {idx+1}",
                "text": para
            })

    return chunks