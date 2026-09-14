import re

OCR_REPLACEMENTS = {
    "|": "I",
    "—": "-",
    "–": "-",
    "•": "",
    "ﬁ": "fi",
    "ﬂ": "fl",
}


def normalize_text(text):
    if text is None:
        return ""

    value = str(text)
    for bad, good in OCR_REPLACEMENTS.items():
        value = value.replace(bad, good)

    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"^[^\w+@#(]+|[^\w).@/-]+$", "", value.strip())
    return value


def fix_common_ocr_mistakes(text):
    value = normalize_text(text)
    value = re.sub(r"\bL imited\b", "Limited", value, flags=re.I)
    value = re.sub(r"\bL td\b", "Ltd", value, flags=re.I)
    value = re.sub(r"\bGmaiI\b", "Gmail", value, flags=re.I)
    value = re.sub(r"\bmaiI\b", "mail", value, flags=re.I)
    return value


def tokens(text):
    return re.findall(r"[a-z0-9]+", normalize_text(text).lower())
