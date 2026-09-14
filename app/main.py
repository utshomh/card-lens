from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI(
    title="CardLens API",
    version="0.0.1"
)

UPLOAD_DIR = "upload"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get('/')
def home():
    return {
        "message": "CardLens API is running"
    }

@app.post('/upload')
async def upload_card(
    file: UploadFile = File(...)
):
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "filename": file.filename,
        "status": "uploaded"
    }