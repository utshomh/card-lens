import os
import shutil
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.background import BackgroundTasks

from app.cleanup import cleanup_uploads
from app.kie import extract_card
from app.kie.engine import KIEModelError

app = FastAPI(title="Card-Lens API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/scan-card")
async def scan_card(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # OCR, layout ordering, and local semantic entity recognition.
        data = extract_card(file_path)
    except KIEModelError as exc:
        # First-run download or cache problems should be actionable to API users.
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    background_tasks.add_task(cleanup_uploads)

    return {
        "success": True,
        "data": data,
    }
