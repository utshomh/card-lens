"""Singleton, CPU-only zero-shot entity extraction engine."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from threading import Lock
from typing import Any

from gliner import GLiNER

from app.kie.labels import ENTITY_LABELS

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_ID = "gliner-community/gliner_small-v2.5"
DEFAULT_CACHE_DIR = PROJECT_ROOT / "models" / "gliner"


class KIEModelError(RuntimeError):
    """Raised when the local semantic extraction model cannot be loaded."""


class KIEEngine:
    """Load one GLiNER model and serialize CPU inference through it."""

    def __init__(self, model_id: str, cache_dir: Path) -> None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            # from_pretrained downloads on first setup and reuses the local cache
            # afterward. map_location keeps this deployment CPU-only.
            self._model = GLiNER.from_pretrained(
                model_id,
                cache_dir=str(cache_dir),
                map_location="cpu",
            )
            self._model.eval()
        except Exception as exc:
            raise KIEModelError(
                "Could not load the local KIE model. Run the model-download "
                "command in README.md once while connected to the internet."
            ) from exc

        self._lock = Lock()
        self._threshold = float(os.getenv("CARD_LENS_KIE_THRESHOLD", "0.30"))

    def predict(self, text: str) -> list[dict[str, Any]]:
        """Return semantic spans labelled with the seven card entity types."""

        if not text.strip():
            return []
        with self._lock:
            # Nested candidates let an email beat its embedded domain by score;
            # entities_to_card resolves the overlap during output conversion.
            return self._model.predict_entities(
                text,
                ENTITY_LABELS,
                threshold=self._threshold,
                flat_ner=False,
                multi_label=False,
            )


@lru_cache(maxsize=1)
def get_kie_engine() -> KIEEngine:
    """Return the process-wide model singleton; never reload per request."""

    model_id = os.getenv("CARD_LENS_KIE_MODEL", DEFAULT_MODEL_ID)
    cache_dir = Path(os.getenv("CARD_LENS_MODEL_CACHE", DEFAULT_CACHE_DIR))
    return KIEEngine(model_id, cache_dir.resolve())
