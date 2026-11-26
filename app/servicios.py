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

@router.get("/cotizar-flota")
def cotizar_flota(
    vehiculos: Annotated[int, Query(ge=1, le=50)],
    complejidad: Annotated[int | None, Query(ge=1, le=5)] = None,
) -> dict:
    seleccion = [s for s in SERVICIOS if complejidad is None or s["complejidad"] == complejidad]
    if not seleccion:
        raise HTTPException(404, f"No hay servicios con complejidad {complejidad}")
    costo_servicios = sum(s["costo"] for s in seleccion)
    con_repuesto = sum(1 for s in seleccion if s["requiere_repuesto"])
    costo_base = costo_servicios * vehiculos
    descuento = vehiculos >= 10
    costo_estimado = costo_base * 0.82 if descuento else costo_base
    return {
        "servicios": len(seleccion),
        "vehiculos": vehiculos,
        "costo_promedio": round(costo_servicios / len(seleccion), 2),
        "costo_base": costo_base,
        "descuento_aplicado": descuento,
        "costo_estimado": round(costo_estimado, 2),
        "porcentaje_con_repuesto": round(con_repuesto * 100 / len(seleccion), 1),
    }

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


@router.get("/cotizar-flota")
def cotizar_flota(
    vehiculos: Annotated[int, Query(ge=1, le=50)],
    complejidad: Annotated[int | None, Query(ge=1, le=5)] = None,
) -> dict:
    seleccion = [s for s in SERVICIOS if complejidad is None or s["complejidad"] == complejidad]
    if not seleccion:
        raise HTTPException(404, f"No hay servicios con complejidad {complejidad}")
    costo_servicios = sum(s["costo"] for s in seleccion)
    con_repuesto = sum(1 for s in seleccion if s["requiere_repuesto"])
    costo_base = costo_servicios * vehiculos
    descuento = vehiculos >= 10
    costo_estimado = costo_base * 0.82 if descuento else costo_base
    return {
        "servicios": len(seleccion),
        "vehiculos": vehiculos,
        "costo_promedio": round(costo_servicios / len(seleccion), 2),
        "costo_base": costo_base,
        "descuento_aplicado": descuento,
        "costo_estimado": round(costo_estimado, 2),
        "porcentaje_con_repuesto": round(con_repuesto * 100 / len(seleccion), 1),
    }

@router.get("/progreso-orden")
def progreso_orden(ejecutados: Annotated[list[str] | None, Query()] = None) -> dict:
    codigos = {c.upper() for c in (ejecutados or [])}
    total = costo_pendiente = 0
    hechos = pendientes = 0
    mas_economico = None
    menor_costo = None
    for servicio in SERVICIOS:
        total += 1
        if servicio["codigo"] in codigos:
            hechos += 1
        else:
            pendientes += 1
            costo_pendiente += servicio["costo"]
            if menor_costo is None or servicio["costo"] < menor_costo:
                menor_costo = servicio["costo"]
                mas_economico = servicio["codigo"]
    if total == 0:
        raise HTTPException(404, "No hay servicios registrados")
    return {
        "total": total,
        "ejecutados": hechos,
        "pendientes": pendientes,
        "porcentaje_avance": round(hechos * 100 / total, 1),
        "costo_pendiente": costo_pendiente,
        "pendiente_mas_economico": mas_economico,
    }