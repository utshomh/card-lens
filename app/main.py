from fastapi import FastAPI, UploadFile, File
from fastapi.background import BackgroundTasks

import shutil
import uuid
import os

from app.ocr import extract_lines
from app.parser import parse_ocr_lines
from app.cleanup import cleanup_uploads

app = FastAPI(
    title="Card-Lens API"
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@app.post("/scan-card")
async def scan_card(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    filename = f"{uuid.uuid4()}.jpg"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # save image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # OCR
    ocr_lines = extract_lines(file_path)

    # Parse
    data = parse_ocr_lines(ocr_lines)

    # cleanup old uploads
    background_tasks.add_task(
        cleanup_uploads
    )

    return {
        "success": True,
        "data": data,
        "raw": ocr_lines
    }
