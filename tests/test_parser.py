from app.parser import parse_ocr_lines


def test_extracts_standard_card():
    ocr = [
        {"text": "Union Chemical Bangladesh Ltd.", "confidence": 0.96, "x": 220, "y": 40},
        {"text": "Rahim Uddin", "confidence": 0.94, "x": 210, "y": 150},
        {"text": "Managing Director", "confidence": 0.94, "x": 210, "y": 190},
        {"text": "+880 1712 345678", "confidence": 0.91, "x": 210, "y": 280},
        {"text": "rahim@example.com", "confidence": 0.93, "x": 210, "y": 315},
        {"text": "House 12, Road 4, Dhaka 1205", "confidence": 0.9, "x": 210, "y": 355},
    ]

    data = parse_ocr_lines(ocr)

    assert data["name"] == "Rahim Uddin"
    assert data["company"] == "Union Chemical Bangladesh Ltd."
    assert data["designation"] == "Managing Director"
    assert data["phone"] == "+880 1712 345678"
    assert data["email"] == "rahim@example.com"
    assert data["address"] == "House 12, Road 4, Dhaka 1205"


def test_merges_split_company_lines():
    ocr = [
        {"text": "Fashion", "confidence": 0.96, "x": 120, "y": 40},
        {"text": "Express", "confidence": 0.95, "x": 122, "y": 82},
        {"text": "Nadia Akter", "confidence": 0.95, "x": 170, "y": 180},
        {"text": "Sales Executive", "confidence": 0.94, "x": 170, "y": 220},
        {"text": "www.fashionexpress.com", "confidence": 0.9, "x": 170, "y": 330},
    ]

    data = parse_ocr_lines(ocr)

    assert data["company"] == "Fashion Express"
    assert data["name"] == "Nadia Akter"
    assert data["designation"] == "Sales Executive"
    assert data["website"] == "www.fashionexpress.com"


def test_finds_name_near_bottom():
    ocr = [
        {"text": "Global Trading Solutions", "confidence": 0.96, "x": 200, "y": 35},
        {"text": "Import Export and Supply Chain", "confidence": 0.88, "x": 200, "y": 82},
        {"text": "Road 8, Sector 3, Dhaka 1230", "confidence": 0.9, "x": 200, "y": 150},
        {"text": "info@gts.com", "confidence": 0.93, "x": 200, "y": 240},
        {"text": "+880-1811-222333", "confidence": 0.93, "x": 200, "y": 280},
        {"text": "Assistant Manager", "confidence": 0.94, "x": 200, "y": 380},
        {"text": "Shafiq Hasan", "confidence": 0.95, "x": 200, "y": 425},
    ]

    data = parse_ocr_lines(ocr)

    assert data["name"] == "Shafiq Hasan"
    assert data["company"] == "Global Trading Solutions"
    assert data["designation"] == "Assistant Manager"
    assert data["address"] == "Road 8, Sector 3, Dhaka 1230"
