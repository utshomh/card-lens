"""PaddleOCR text detection and recognition only."""

from functools import lru_cache
from threading import Lock
from typing import TypedDict

from paddleocr import PaddleOCR


class OCRLine(TypedDict):
    text: str
    confidence: float
    bbox: list[list[float]]


class _OCREngine:
    """Own the single CPU OCR predictor and serialize access to it."""

    def __init__(self) -> None:
        # Paddle predictors are expensive to create, so this happens once per process.
        self._predictor = PaddleOCR(lang="en", use_gpu=False, show_log=False)
        self._lock = Lock()

    def extract(self, image_path: str) -> list[OCRLine]:
        with self._lock:
            pages = self._predictor.ocr(image_path, cls=False)

        lines: list[OCRLine] = []
        for page in pages or []:
            for item in page or []:
                box, recognition = item
                text, confidence = recognition
                lines.append(
                    {
                        "text": text,
                        "confidence": float(confidence),
                        "bbox": [[float(x), float(y)] for x, y in box],
                    }
                )
        return lines


@lru_cache(maxsize=1)
def _get_ocr_engine() -> _OCREngine:
    return _OCREngine()


def extract_lines(image_path: str) -> list[OCRLine]:
    """Return OCR text, confidence, and quadrilateral bounding boxes."""

    return _get_ocr_engine().extract(image_path)
