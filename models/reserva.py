from datetime import date
from typing import Union, List, Optional
from pydantic import BaseModel, AnyUrl

class Reserva(BaseModel):
    fechaInicio : str
    fechaFin : str
    precio : float
    username : str
    vivienda : str