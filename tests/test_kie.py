"""Unit and real-image tests for local semantic card extraction."""

from pathlib import Path

import pytest

from app.kie.extractor import _reading_order
from app.kie.labels import CARD_FIELDS, entities_to_card


def test_converts_semantic_predictions_to_card() -> None:
    semantic_output = [
        {"text": "Ada Lovelace", "label": "person name", "score": 0.99, "start": 0, "end": 12},
        {"text": "Chief Scientist", "label": "job title or designation", "score": 0.95, "start": 13, "end": 28},
        {"text": "Analytical Engines Ltd", "label": "company or organization", "score": 0.98, "start": 29, "end": 51},
        {"text": "ada@example.com", "label": "email address", "score": 0.92, "start": 52, "end": 67},
        {"text": "example.com", "label": "website url", "score": 0.80, "start": 56, "end": 67},
        {"text": "+44 20 1234 5678", "label": "phone number", "score": 0.90, "start": 68, "end": 84},
        {"text": "example.com", "label": "website url", "score": 0.91, "start": 85, "end": 96},
        {"text": "12 Computing Lane", "label": "postal address", "score": 0.93, "start": 97, "end": 114},
    ]

    entities = entities_to_card(semantic_output)
    print("Extracted entities:", entities)

    assert entities == {
        "name": "Ada Lovelace",
        "company": "Analytical Engines Ltd",
        "designation": "Chief Scientist",
        "phone": "+44 20 1234 5678",
        "email": "ada@example.com",
        "website": "example.com",
        "address": "12 Computing Lane",
    }


def test_ocr_regions_are_put_in_reading_order() -> None:
    lower = {"text": "second", "confidence": 1.0, "bbox": [[10.0, 40.0], [20.0, 40.0], [20.0, 50.0], [10.0, 50.0]]}
    upper = {"text": "first", "confidence": 1.0, "bbox": [[10.0, 10.0], [20.0, 10.0], [20.0, 20.0], [10.0, 20.0]]}
    assert [line["text"] for line in _reading_order([lower, upper])] == ["first", "second"]


@pytest.mark.integration
def test_sample_card_images() -> None:
    """Run real CPU extraction and print entities for every bundled card."""

    from app.kie.extractor import extract_card

    sample_dir = Path(__file__).parent / "sample_cards"
    images = sorted(
        path
        for pattern in ("*.jpg", "*.jpeg", "*.png", "*.bmp")
        for path in sample_dir.glob(pattern)
    )
    assert images, "Add at least one image to tests/sample_cards"

    for image in images:
        entities = extract_card(str(image))
        print(f"{image.name}: {entities}")
        assert tuple(entities) == CARD_FIELDS
        assert any(entities.values()), f"No entities extracted from {image.name}"
