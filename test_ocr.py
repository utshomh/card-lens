from app.ocr import extract_text

image = "test_images/demo.jpg"

text = extract_text(image)

print(text)