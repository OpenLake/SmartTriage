from fastapi import FastAPI
from app.api.webhooks import router

app = FastAPI(title="SmartTriage")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}