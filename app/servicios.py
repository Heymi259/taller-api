from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.datos import SERVICIOS
from app.esquemas import Servicio, ServicioActualizar, ServicioCrear

router = APIRouter(prefix="/servicios", tags=["servicios"])


def obtener_servicio(codigo: str) -> dict:
    """Devuelve el diccionario del servicio o lanza 404."""
    for servicio in SERVICIOS:
        if servicio["codigo"] == codigo.upper():
            return servicio
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el servicio '{codigo}'",
    )


ServicioEncontrado = Annotated[dict, Depends(obtener_servicio)]