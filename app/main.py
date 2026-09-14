from fastapi import FastAPI

app = FastAPI(
    title="CardLens API",
    version="0.0.1"
)

@app.get('/')
def home():
    return {
        "message": "CardLens API is running"
    }