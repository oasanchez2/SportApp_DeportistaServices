from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

class Genero(Enum):
    FEMENINO = "Femenino"
    MASCULINO = "Masculino"
    

@dataclass
class DeportistaModel:
    id_usuario: str
    genero: Genero
    edad: int
    peso_inicial: float
    peso_actual: float
    altura: float
    deporte_practicar: str
    fecha_creacion: datetime
