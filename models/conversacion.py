from datetime import date
from typing import Union, List, Optional
from pydantic import BaseModel, AnyUrl

class Mensaje(BaseModel):
    emisor : str
    receptor : str
    contenido : str
    fecha : str

class Conversacion(BaseModel):
    id : Optional[str]
    participante1 : str
    participante2 : str
    mensajes : Optional[Union[List[Mensaje], None]] = None