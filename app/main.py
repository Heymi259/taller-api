from fastapi import FastAPI

from app.servicios import router

app = FastAPI(title="API del Taller Mecánico", version="1.0.0")
app.include_router(router)


@app.get("/")
def raiz() -> dict:
    return {"api": "taller", "docs": "/docs"}