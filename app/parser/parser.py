from app.parser.cleaners import fix_common_ocr_mistakes
from app.parser.patterns import EMAIL_RE, PHONE_RE, WEBSITE_RE
from app.parser.scorer import score_line


EMPTY_RESULT = {
    "name": None,
    "company": None,
    "designation": None,
    "phone": None,
    "email": None,
    "website": None,
    "address": None,
}


def parse_card_text(text):
    lines = [
        {"text": line, "confidence": 1.0, "x": 0, "y": index * 40}
        for index, line in enumerate(str(text).splitlines())
        if fix_common_ocr_mistakes(line)
    ]
    return parse_ocr_lines(lines)


def parse_ocr_lines(ocr_lines):
    data = EMPTY_RESULT.copy()
    normalized = _normalize_lines(ocr_lines)
    grouped = group_lines(normalized)

    non_contact = []
    for line in grouped:
        text = line["text"]
        data["email"] = data["email"] or _first_match(EMAIL_RE, text)
        data["phone"] = data["phone"] or _first_match(PHONE_RE, text)
        website = None if EMAIL_RE.search(text) else _first_match(WEBSITE_RE, text)
        if website:
            data["website"] = data["website"] or website
        if not (EMAIL_RE.search(text) or PHONE_RE.search(text) or WEBSITE_RE.search(text)):
            non_contact.append(line)

    context = {
        "max_y": max((line["y"] for line in grouped), default=1),
        "contact_lines": [line for line in grouped if line not in non_contact],
    }

    scored = []
    for line in non_contact:
        scores = score_line(line, context)
        scored.append({**line, **scores})

    data["designation"] = _pick_best(scored, "designation_score", minimum=25)
    data["name"] = _pick_best(
        [line for line in scored if line["text"] != data["designation"]],
        "name_score",
        minimum=35,
    )
    data["company"] = _pick_company(scored, data)
    data["address"] = _pick_address(scored, data)
    return data


def group_lines(lines, y_threshold=18):
    rows = []
    for line in sorted(lines, key=lambda item: (item["y"], item["x"])):
        for row in rows:
            if abs(row["y"] - line["y"]) <= y_threshold:
                row["items"].append(line)
                row["y"] = sum(item["y"] for item in row["items"]) / len(row["items"])
                break
        else:
            rows.append({"y": line["y"], "items": [line]})

    grouped = []
    for row in rows:
        items = sorted(row["items"], key=lambda item: item["x"])
        text = " ".join(item["text"] for item in items if item["text"]).strip()
        if text:
            grouped.append({
                "text": text,
                "confidence": min(item.get("confidence", 1.0) for item in items),
                "x": min(item["x"] for item in items),
                "y": row["y"],
            })
    return grouped


def _normalize_lines(ocr_lines):
    lines = []
    for index, item in enumerate(ocr_lines or []):
        text = fix_common_ocr_mistakes(item.get("text", ""))
        if not text:
            continue
        lines.append({
            "text": text,
            "confidence": float(item.get("confidence", 1.0) or 0),
            "x": float(item.get("x", 0) or 0),
            "y": float(item.get("y", index * 40) or 0),
        })
    return lines


def _pick_best(lines, key, minimum):
    candidates = [line for line in lines if line[key] >= minimum]
    if not candidates:
        return None
    return max(candidates, key=lambda line: (line[key], -line["y"]))["text"]


def _pick_company(lines, data):
    blocked = {data.get("name"), data.get("designation")}
    candidates = [
        line for line in lines
        if line["text"] not in blocked and line["company_score"] >= 18
    ]
    if not candidates:
        return None

    best = max(candidates, key=lambda line: (line["company_score"], -line["y"]))
    adjacent = [
        line for line in lines
        if line["text"] not in blocked
        and abs(line["y"] - best["y"]) <= 70
        and line["address_score"] < 25
        and line["designation_score"] < 25
        and line["name_score"] < 45
        and _is_company_mergeable(line)
    ]
    merged = sorted({line["text"]: line for line in adjacent + [best]}.values(), key=lambda line: line["y"])
    return " ".join(line["text"] for line in merged)


def _pick_address(lines, data):
    blocked = {data.get("name"), data.get("designation"), data.get("company")}
    candidates = [
        line for line in lines
        if line["text"] not in blocked and line["address_score"] >= 25
    ]
    if not candidates:
        return None
    return ", ".join(line["text"] for line in sorted(candidates, key=lambda line: line["y"]))


def _first_match(pattern, text):
    match = pattern.search(text)
    return match.group(0).strip() if match else None


def _is_company_mergeable(line):
    words = line["text"].split()
    lowered = line["text"].lower()
    return len(words) <= 3 and " and " not in f" {lowered} "

