import re

def parse_card_text(text):
    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    result = {
        "name": None,
        "company": None,
        "designation": None,
        "phone": None,
        "email": None,
        "website": None,
        "address": None
    }


    for line in lines:

        lower = line.lower()

        # email
        if "@" in line:
            result["email"] = line


        # phone
        elif re.search(r"\+?\d[\d\s\-]{7,}", line):
            result["phone"] = line


        # website
        elif "www" in lower or ".com" in lower:
            result["website"] = line


    # naive assumption:
    # first line = name
    if len(lines) > 0:
        result["name"] = lines[0]


    # second line = company
    if len(lines) > 1:
        result["company"] = lines[1]


    return result