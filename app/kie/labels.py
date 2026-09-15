"""Semantic label definitions and stable API output conversion."""

from collections.abc import Iterable, Mapping

CARD_FIELDS = (
    "name",
    "company",
    "designation",
    "phone",
    "email",
    "website",
    "address",
)

LABEL_TO_FIELD = {
    "person name": "name",
    "company or organization": "company",
    "job title or designation": "designation",
    "phone number": "phone",
    "email address": "email",
    "website url": "website",
    "postal address": "address",
}
ENTITY_LABELS = tuple(LABEL_TO_FIELD)


def empty_card() -> dict[str, str]:
    return {field: "" for field in CARD_FIELDS}


def _overlaps(left: Mapping[str, object], right: Mapping[str, object]) -> bool:
    return int(left.get("start", 0)) < int(right.get("end", 0)) and int(
        right.get("start", 0)
    ) < int(left.get("end", 0))


def entities_to_card(items: Iterable[Mapping[str, object]]) -> dict[str, str]:
    """Convert GLiNER spans into the fixed business-card response object."""

    # Keep the strongest candidate when nested spans compete (for example, an
    # email address versus the website-like domain inside it).
    selected: list[Mapping[str, object]] = []
    for item in sorted(items, key=lambda value: float(value.get("score", 0)), reverse=True):
        if not any(_overlaps(item, other) for other in selected):
            selected.append(item)

    grouped: dict[str, list[str]] = {field: [] for field in CARD_FIELDS}
    for item in sorted(selected, key=lambda value: int(value.get("start", 0))):
        field = LABEL_TO_FIELD.get(str(item.get("label", "")).lower())
        text = str(item.get("text", "")).strip()
        if field and text and text.casefold() not in {
            existing.casefold() for existing in grouped[field]
        }:
            grouped[field].append(text)

    # Multiple values (for example, office and mobile phones) remain visible.
    return {field: " | ".join(values) for field, values in grouped.items()}
