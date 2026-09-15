# Card-Lens

CPU-only FastAPI service that extracts business-card fields with PaddleOCR and
local zero-shot semantic entity recognition. 

## Setup

Python 3.11 is required. From a fresh clone on Windows PowerShell:

```powershell
git clone <repository-url>
cd card-lens
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install paddleocr==2.7.0.0 --no-deps
python -c "from app.kie.engine import get_kie_engine; get_kie_engine(); print('KIE model ready')"
```

The separate PaddleOCR command avoids its obsolete optional PDF dependencies,
which do not support this Python version and are not used for image scanning.
The final command downloads `gliner-community/gliner_small-v2.5` once into
`models/gliner`; the cache is reused afterward. PaddleOCR similarly downloads
its English OCR weights on the first scan. Internet access is needed only for
these initial downloads. No paths or environment variables must be configured.

On macOS/Linux, create the environment with `python3.11 -m venv venv` and
activate it with `source venv/bin/activate`; the remaining commands are the same.

## Run

```powershell
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> and call `POST /scan-card` with an image.

## Test

```powershell
pytest -s tests/test_kie.py
```

The integration test scans every image in `tests/sample_cards` and prints the
extracted entities. See [explanation.md](explanation.md) for the design details.
