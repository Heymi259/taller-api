from fastapi import FastAPI

app = FastAPI(title="API del Taller Mecánico", version="1.0.0")


@app.get("/")
def raiz() -> dict:
    return {"api": "taller", "docs": "/docs"}