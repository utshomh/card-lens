import re

from app.parser.cleaners import tokens
from app.parser.patterns import (
    ADDRESS_KEYWORDS,
    ADDRESS_NUMBER_RE,
    COMPANY_KEYWORDS,
    DESIGNATION_TERMS,
    DESIGNATION_WORDS,
    EMAIL_RE,
    PHONE_RE,
    POSTAL_RE,
    WEBSITE_RE,
)


def score_line(line, context):
    text = line["text"]
    lower_tokens = set(tokens(text))
    word_count = len(text.split())
    alpha_chars = sum(ch.isalpha() for ch in text)
    total_chars = max(len(text), 1)
    alpha_ratio = alpha_chars / total_chars
    topness = 1 - (line.get("y", 0) / max(context.get("max_y", 1), 1))
    near_contact = _near_contact(line, context.get("contact_lines", []))

    company_hits = len(lower_tokens & COMPANY_KEYWORDS)
    address_hits = len(lower_tokens & ADDRESS_KEYWORDS)
    designation_score = _designation_score(text, lower_tokens)

    name_score = 0
    if 2 <= word_count <= 4:
        name_score += 25
    if alpha_ratio >= 0.75:
        name_score += 20
    if _looks_like_person_name(text):
        name_score += 30
    if near_contact:
        name_score += 12
    if _mostly_title_case(text):
        name_score += 10
    name_score -= company_hits * 18
    name_score -= address_hits * 15
    name_score -= min(designation_score, 40)
    if _contains_contact(text):
        name_score -= 50

    company_score = company_hits * 22
    if topness > 0.55:
        company_score += 12
    if 1 <= word_count <= 5 and alpha_ratio >= 0.55:
        company_score += 8
    if text.isupper() and word_count <= 5:
        company_score += 6
    company_score -= address_hits * 6
    if _contains_contact(text):
        company_score -= 45

    address_score = address_hits * 18
    if any(ch.isdigit() for ch in text):
        address_score += 10
    if POSTAL_RE.search(text):
        address_score += 12
    if ADDRESS_NUMBER_RE.search(text):
        address_score += 18
    if word_count >= 4:
        address_score += 8
    if _contains_contact(text):
        address_score -= 30

    return {
        "name_score": max(name_score, 0),
        "company_score": max(company_score, 0),
        "designation_score": max(designation_score, 0),
        "address_score": max(address_score, 0),
    }


def _designation_score(text, lower_tokens):
    normalized = " ".join(tokens(text))
    score = 0
    for term in DESIGNATION_TERMS:
        term_value = " ".join(tokens(term))
        if term_value and term_value in normalized:
            score = max(score, 35 + len(term_value.split()) * 8)

    score += len(lower_tokens & DESIGNATION_WORDS) * 12
    if 1 <= len(text.split()) <= 5:
        score += 8
    if _contains_contact(text):
        score -= 40
    return score


def _looks_like_person_name(text):
    words = [word.strip(".") for word in text.split()]
    if not 2 <= len(words) <= 4:
        return False
    return all(re.fullmatch(r"[A-Za-z][A-Za-z.'-]*", word) for word in words)


def _mostly_title_case(text):
    words = [word for word in text.split() if any(ch.isalpha() for ch in word)]
    if not words:
        return False
    good = sum(word[:1].isupper() and not word.isupper() for word in words)
    return good / len(words) >= 0.6


def _contains_contact(text):
    return bool(EMAIL_RE.search(text) or PHONE_RE.search(text) or WEBSITE_RE.search(text))


def _near_contact(line, contact_lines):
    if not contact_lines:
        return False
    y = line.get("y", 0)
    return min(abs(y - item.get("y", 0)) for item in contact_lines) <= 180
