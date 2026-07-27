from enum import Enum

from pydantic import BaseModel, Field


class NivelDeCriticidad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class ExtraccionTecnica(BaseModel):
    """Contrato de salida del pipeline de extracción de entidades técnicas."""

    tecnologias: list[str] = Field(
        ...,
        min_length=1,
        description="Lista de tecnologías detectadas en el texto (no vacía)",
    )
    nivel_de_criticidad: NivelDeCriticidad = Field(
        ...,
        description="Nivel de criticidad: baja, media o alta",
    )
    resumen_tecnico: str = Field(
        ...,
        min_length=1,
        description="Resumen técnico conciso del contenido analizado",
    )
