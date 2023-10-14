from fastapi import APIRouter, Response, status, Request, Body #APIRouter: nos permite definir todas las rutas dentro de este archivo
from config.db import db
from bson import ObjectId
from models.reserva import *
from schemas.reserva import *
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from fastapi.encoders import jsonable_encoder
from routes.usuario import *

reserva = APIRouter()
db_reserva = "reserva"

#region ENCONTRAR TODAS LAS RESERVAS
@reserva.get('/reservas', response_model=List[Reserva], tags=["Reserva"])
async def find_all_reservas(request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        reservas = reservasEntity(db[db_reserva].find())
        return reservas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region CRUD Reserva
# CREAR RESERVA
@reserva.post('/reservas', tags=["Reserva"])
async def create_reserva(reserva: Reserva, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        nueva_reserva = jsonable_encoder(reserva)
        db[db_reserva].insert_one(nueva_reserva)
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

# MODIFICAR RESERVA
@reserva.put('/reservas/{id}', tags=["Reserva"])
async def update_reserva(id: str, reserva: Reserva, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        nueva_reserva = jsonable_encoder(reserva)
        db[db_reserva].find_one_and_update({"_id": ObjectId(id)}, {"$set": nueva_reserva })
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    
# BORRAR RESERVA
@reserva.delete('/reservas/{id}', tags=["Reserva"])
async def delete_reserva(id: str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        reservaEntity(db[db_reserva].find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region ENCONTRAR TODAS LAS RESERVAS DE UN USUARIO
@reserva.get('/reservas/todas/propietario', response_model=List[Reserva], tags=["Vivienda"])
async def find_reservas_by_propietario(request: Request):
    validez = check_token(request.headers["Authentication"])
    if validez:
        reservas = reservasEntity(db[db_reserva].find({"username": validez}))

        return reservas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion  