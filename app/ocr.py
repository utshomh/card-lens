from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(
    lang="en"
)

def extract_text(image_path):
    result = ocr_engine.ocr(image_path)
    
    texts = []
    
    for page in result:
        for item in page:
            texts.append(item[1][0])

    return "\n".join(texts)
