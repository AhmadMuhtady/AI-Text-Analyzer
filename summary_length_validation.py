import re

def summary_length_validation(text: str) -> list[str]:

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
    masked_text = text
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

    return restored_sentences
