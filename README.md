# Card-Lens

Card-Lens is a microservice API that extracts information from visiting card images and returns structured JSON data.

## Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- OpenCV
- Pillow
- PaddleOCR

## Setup (Windows)

### 1. Create virtual environment

python -m venv venv

### 2. Activate virtual environment

venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run API

uvicorn app.main:app --reload

## API

Local API:

<http://127.0.0.1:8000>

Swagger Documentation:

<http://127.0.0.1:8000/docs>
