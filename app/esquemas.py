from pydantic import BaseModel, Field


class ServicioBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=60)
    costo: int = Field(ge=5, le=1000)
    complejidad: int = Field(ge=1, le=5)
    requiere_repuesto: bool = False


class ServicioCrear(ServicioBase):
    codigo: str = Field(pattern=r"^[A-Z]{3}\d{3}$")


class ServicioActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=3, max_length=60)
    costo: int | None = Field(default=None, ge=5, le=1000)
    complejidad: int | None = Field(default=None, ge=1, le=5)
    requiere_repuesto: bool | None = None


class Servicio(ServicioCrear):
    """Lo que la API devuelve: los cinco campos completos."""