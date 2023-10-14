from typing import Union, List, Optional
from pydantic import BaseModel, AnyUrl

class Localizacion(BaseModel):
    pais : str
    provincia : str
    municipio : str 
    cp : str 
    calle : str
    numero : str
    numeroBloque : str
    lat : float
    lon : float

class ReseñaVivienda(BaseModel):
    username : str
    comentario : str
    puntuacion : float
    fecha : str

class ReservaVivienda(BaseModel):
    fechaInicio : str
    fechaFin : str
    username : str

class Vivienda(BaseModel):
    id : Optional[str]
    nombre: str
    descripcion: str
    precio : float
    capacidad : int
    localizacion : Union[Localizacion, None] = None
    propietario : str
    reservas : Optional[Union[List[ReservaVivienda], None]] = None 
    fotos : Union[List[AnyUrl],None] = None
    valoracion : float
    reseñas : Optional[Union[List[ReseñaVivienda], None]] = None 