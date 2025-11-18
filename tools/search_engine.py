def clean_text(t):
    return " ".join(t.split())

def simplify(text):
    # Simple explanation from longest sentence
    sentences = text.split(".")
    if not sentences:
        return text

    long = max(sentences, key=len).strip()
    return f"Easy explanation: {long}."
