"""Business-card key information extraction."""


def extract_card(image_path: str) -> dict[str, str]:
    """Load the heavyweight Paddle runtime only when extraction is requested."""

    from app.kie.extractor import extract_card as _extract_card

    return _extract_card(image_path)


__all__ = ["extract_card"]
