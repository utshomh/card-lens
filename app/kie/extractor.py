"""End-to-end business-card extraction orchestration."""

from app.kie.engine import get_kie_engine
from app.kie.labels import empty_card, entities_to_card
from app.ocr.paddle import OCRLine, extract_lines


def _reading_order(lines: list[OCRLine]) -> list[OCRLine]:
    """Order OCR regions from top-to-bottom and then left-to-right."""

    return sorted(
        lines,
        key=lambda line: (
            min(point[1] for point in line["bbox"]),
            min(point[0] for point in line["bbox"]),
        ),
    )


def extract_card(image_path: str) -> dict[str, str]:
    """Run OCR, layout ordering, semantic inference, and output conversion."""

    ocr_lines = extract_lines(image_path)
    if not ocr_lines:
        return empty_card()

    # Bounding boxes establish document reading order. Newlines retain region
    # boundaries while the semantic model classifies spans from the OCR text.
    document = "\n".join(line["text"] for line in _reading_order(ocr_lines))
    entities = get_kie_engine().predict(document)
    return entities_to_card(entities)
