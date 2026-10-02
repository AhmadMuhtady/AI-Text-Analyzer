import re

def summary_length_validation(text: str, length: str) -> str:
    summary_map = {
        'short': (1, 2),
        'medium': (3, 5),
        'long': (6, 10),
    }

    if length not in summary_map:
        raise ValueError(f"Invalid length option '{length}'. Choose from {list(summary_map.keys())}.")

    cleaned_text = re.sub(r'([,;:])([A-Za-z0-9"\'\(\[\{])', r'\1 \2', text.strip())


    cleaned_text = re.sub(r'([.!?])([A-Z])', r'\1 \2', cleaned_text)

    ABBREVIATION_MAP = {
        r"\bU\.S\.": "__US__",
        r"\bU\.K\.": "__UK__",
        r"\bDr\.": "__DR__",
        r"\bMr\.": "__MR__",
        r"\bMrs\.": "__MRS__",
        r"\bProf\.": "__PROF__",
        r"\be\.g\.": "__EG__",
        r"\bi\.e\.": "__IE__",
        r"\betc\.": "__ETC__",
    }

    RESTORE_MAP = {v: k.replace(r"\b", "").replace(r"\\.", ".") for k, v in ABBREVIATION_MAP.items()}
    
    masked_text = cleaned_text
    for pattern, placeholder in ABBREVIATION_MAP.items():
        masked_text = re.sub(pattern, placeholder, masked_text)

    sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z0-9])'
    raw_segments = re.split(sentence_pattern, masked_text.strip())

    restored_sentences = []
    for segment in raw_segments:
        clean = segment.strip()
        if not clean:
            continue
        for placeholder, original in RESTORE_MAP.items():
            clean = clean.replace(placeholder, original)
        restored_sentences.append(clean)

    sentence_length = len(restored_sentences)
    min_sentences, max_sentences = summary_map[length]

    if min_sentences <= sentence_length <= max_sentences:
        return cleaned_text

    raise ValueError(
        f"Expected {min_sentences}-{max_sentences} sentences for '{length}', received: {sentence_length}"
    )