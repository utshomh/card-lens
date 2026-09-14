import re

DESIGNATIONS = [
    # Leadership
    "ceo",
    "chief executive officer",
    "coo",
    "chief operating officer",
    "cfo",
    "chief financial officer",
    "cto",
    "chief technology officer",
    "chairman",
    "vice chairman",
    "president",
    "vice president",
    "vp",
    "general manager",
    "assistant general manager",
    "deputy general manager",
    "managing director",
    "md",
    "executive director",
    "director",
    "deputy director",

    # Management
    "manager",
    "assistant manager",
    "senior manager",
    "branch manager",
    "area manager",
    "regional manager",
    "operations manager",
    "project manager",
    "product manager",
    "sales manager",
    "marketing manager",
    "finance manager",
    "hr manager",
    "human resource manager",

    # Sales / Business
    "sales executive",
    "sales representative",
    "sales officer",
    "business development manager",
    "business development executive",
    "account manager",
    "key account manager",
    "commercial manager",

    # Technical
    "engineer",
    "senior engineer",
    "software engineer",
    "technical manager",
    "technical director",
    "consultant",
    "architect",
    "developer",

    # General
    "advisor",
    "specialist",
    "analyst",
    "administrator",
    "coordinator",
    "officer",
    "executive",
    "associate",
    "assistant",

    # Owner
    "owner",
    "founder",
    "co-founder",
    "partner",
    "proprietor",
    "principal",

    # Academic / Medical
    "professor",
    "doctor",
    "dr",
    "researcher",

    # Abbreviation
    "gm",
    "agm",
    "dgm",
    "pm",
]

COMPANY_WORDS = [
    "ltd",
    "limited",
    "company",
    "co.",
    "corp",
    "corporation",
    "group",
    "enterprise",
    "trading",
    "international",
    "industries",
    "industry",
    "technology",
    "tech",
    "solutions",
    "systems",
    "services",
    "fashion",
    "express",
    "import",
    "export",
]

ADDRESS_WORDS = [
    "road",
    "street",
    "st.",
    "avenue",
    "ave",
    "city",
    "district",
    "province",
    "country",
    "bangladesh",
    "china",
    "office",
    "zip",
    "postal",
]

def clean_line(line):
    return (
        line
        .replace("|", "I")
        .replace("—", "-")
        .strip()
    )

def is_email(line):
    return re.search(
        r"\S+@\S+\.\S+",
        line
    )

def is_phone(line):
    numbers = re.sub(
        r"\D",
        "",
        line
    )

    return len(numbers) >= 8


def is_website(line):
    text = line.lower()

    return (
        "www" in text
        or ".com" in text
        or ".net" in text
        or ".org" in text
    )

def is_designation(line):
    text = line.lower().strip()

    for item in DESIGNATIONS:
        if item in text:
            return True

    return False

def is_name_candidate(line):
    words = line.split()

    # Human names usually have 2-4 words
    if not (2 <= len(words) <= 4):
        return False

    # Reject obvious non-name lines
    blacklist = [
        "office",
        "address",
        "road",
        "street",
        "city",
        "bangladesh",
        "china",
        "email",
        "phone",
        "cell",
        "mobile",
        "corporate",
        "manager",
        "director",
        "company",
        "ltd"
    ]

    lower = line.lower()

    if any(
        word in lower
        for word in blacklist
    ):
        return False

    # Names normally contain alphabetic words
    if all(
        word.replace(".", "").isalpha()
        for word in words
    ):
        return True

    return False

def looks_like_address(line):
    text = line.lower()

    return any(
        word in text
        for word in ADDRESS_WORDS
    )

def merge_company_lines(lines):
    if not lines:
        return None

    company = []

    for line in lines:

        if line in ["/", "-", "&"]:
            continue

        company.append(line)

    return " ".join(company)

def parse_card_text(text):
    lines = [
        clean_line(x)
        for x in text.split("\n")
        if clean_line(x)
    ]

    data = {
        "name": None,
        "company": None,
        "designation": None,
        "phone": None,
        "email": None,
        "website": None,
        "address": None
    }

    remaining = []

    # -------------------------
    # Extract obvious fields
    # -------------------------
    for line in lines:
        if is_email(line):
            data["email"] = line
        elif is_website(line):
            data["website"] = line
        elif is_phone(line):
            data["phone"] = line
        elif is_designation(line):
            data["designation"] = line
        else:
            remaining.append(line)

    # -------------------------
    # Detect name
    # -------------------------
    for line in remaining:
        if is_name_candidate(line):
            data["name"] = line
            remaining.remove(line)
            break

    # -------------------------
    # Detect company
    # -------------------------
    company_candidates = []

    for line in remaining:
        text = line.lower()

        if any(
            word in text
            for word in COMPANY_WORDS
        ):
            company_candidates.append(line)

    if company_candidates:
        data["company"] = merge_company_lines(
            company_candidates
        )

        for item in company_candidates:
            if item in remaining:
                remaining.remove(item)

    # -------------------------
    # Address
    # -------------------------
    address_lines = []

    for line in remaining:
        if looks_like_address(line):
            address_lines.append(line)
        else:
            # leftover text after identification
            if len(line.split()) > 2:
                address_lines.append(line)

    if address_lines:
        data["address"] = ", ".join(
            address_lines
        )

    return data