from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

class Genero(Enum):
    FEMENINO = "Femenino"
    MASCULINO = "Masculino"

class Planes(Enum):
    Gratuito = "Gratuito"
    Intermedio = "Intermedio"
    Premium = "Premium"

class TipoIdentificacion(Enum):
    CC = "Cédula de ciudadanía"
    TI = "arjeta de identidad"
    CE = "Cédula de extranjería"
    Pasaporte = 'Pasaporte'
    NIT = 'NIT'
    
@dataclass
class DeportistaModel:
    id_usuario: str
    nombre: str
    apellido: str
    tipo_identificacion: TipoIdentificacion
    numero_identificacion: str
    genero: Genero
    edad: int
    peso_inicial: float
    peso_actual: float
    altura: float
    pais_recidencia: str
    ciudad_recidencia: str
    deporte_practicar: str
    plan: Planes
    fecha_creacion: datetime
