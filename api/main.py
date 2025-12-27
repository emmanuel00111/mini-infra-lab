from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="mini-infra-lab")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "mini-infra-lab",
        "time": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/")
def root():
    return {"message": "mini-infra-lab is running"}
