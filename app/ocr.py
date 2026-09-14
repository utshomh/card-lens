from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(
    lang="en"
)


def extract_lines(image_path):
    result = ocr_engine.ocr(image_path)
    lines = []

    for page in result:
        for item in page:
            box = item[0]
            text, confidence = item[1]
            x = sum(point[0] for point in box) / len(box)
            y = sum(point[1] for point in box) / len(box)
            lines.append({
                "text": text,
                "confidence": float(confidence),
                "x": x,
                "y": y,
            })

    return lines


def extract_text(image_path):
    return "\n".join(line["text"] for line in extract_lines(image_path))
