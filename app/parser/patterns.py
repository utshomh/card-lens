import re

DESIGNATION_TERMS = {
    "ceo", "chief executive officer", "coo", "chief operating officer", "cfo",
    "chief financial officer", "cto", "chief technology officer", "chairman",
    "president", "vice president", "vp", "general manager",
    "assistant general manager", "deputy general manager", "managing director",
    "md", "executive director", "director", "manager", "assistant manager",
    "branch manager", "area manager", "operations manager", "project manager",
    "sales manager", "marketing manager", "business development manager",
    "business development executive", "sales executive", "sales representative",
    "sales officer", "account manager", "commercial manager", "engineer",
    "software engineer", "consultant", "architect", "developer", "advisor",
    "specialist", "analyst", "administrator", "coordinator", "officer",
    "executive", "associate", "assistant", "owner", "founder", "co-founder",
    "partner", "proprietor", "principal", "professor", "doctor", "dr",
}

DESIGNATION_WORDS = {
    word
    for term in DESIGNATION_TERMS
    for word in term.replace("-", " ").split()
}

COMPANY_KEYWORDS = {
    "ltd", "limited", "company", "co", "corp", "corporation", "group",
    "enterprise", "enterprises", "trading", "international", "industries",
    "industry", "technology", "technologies", "tech", "solutions", "systems",
    "services", "fashion", "express", "import", "export", "chemical",
    "chemicals", "agency", "associates", "global",
}

ADDRESS_KEYWORDS = {
    "address", "house", "road", "rd", "street", "st", "avenue", "ave",
    "lane", "block", "sector", "floor", "suite", "office", "building",
    "market", "city", "district", "zip", "postal", "dhaka", "bangladesh",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.I)
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{6,}\d)")
WEBSITE_RE = re.compile(r"(?:https?://)?(?:www\.)?[\w-]+(?:\.[\w-]+)+(?:/[^\s]*)?", re.I)
POSTAL_RE = re.compile(r"\b\d{4,6}\b")
ADDRESS_NUMBER_RE = re.compile(r"(?:house|road|rd|street|st|sector|block|suite|floor|#)\s*[-:#]?\s*\w+", re.I)
