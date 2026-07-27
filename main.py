from fastapi import FastAPI

app = FastAPI(title="AI Professional Profile")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
