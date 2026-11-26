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

@router.get("", response_model=list[Servicio])
def listar_servicios(
    complejidad: Annotated[int | None, Query(ge=1, le=5)] = None,
    solo_con_repuesto: bool = False,
) -> list[dict]:
    resultado = SERVICIOS
    if complejidad is not None:
        resultado = [s for s in resultado if s["complejidad"] == complejidad]
    if solo_con_repuesto:
        resultado = [s for s in resultado if s["requiere_repuesto"]]
    return resultado


@router.post("", response_model=Servicio, status_code=status.HTTP_201_CREATED)
def crear_servicio(nueva: ServicioCrear) -> dict:
    if any(s["codigo"] == nueva.codigo for s in SERVICIOS):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El servicio '{nueva.codigo}' ya existe",
        )
    SERVICIOS.append(nueva.model_dump())
    return SERVICIOS[-1]