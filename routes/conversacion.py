from fastapi import APIRouter, Response, status, Request, Body #APIRouter: nos permite definir todas las rutas dentro de este archivo
from config.db import db
from bson import ObjectId
from models.conversacion import *
from schemas.conversacion import *
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from fastapi.encoders import jsonable_encoder
from routes.usuario import *

conversacion = APIRouter()
db_conversacion = "conversacion"

@conversacion.get('/conversaciones', response_model=List[Conversacion], tags=["Conversacion"])
async def find_all_conversaciones(request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        conversaciones = conversacionesEntity(db[db_conversacion].find())
        return conversaciones
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)


@conversacion.post('/conversaciones', response_model=Conversacion, tags=["Conversacion"])
async def create_conversacion(conversacion: Conversacion, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        nueva_conversacion = jsonable_encoder(conversacion)
        id = db[db_conversacion].insert_one(nueva_conversacion).inserted_id
        conversacion = conversacionEntity(db[db_conversacion].find_one({"_id": id}))
        return conversacion
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

@conversacion.get('/conversaciones/{id}', response_model=Conversacion, tags=["Conversacion"])
async def find_conversacion_by_id(id: str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        return conversacionEntity(db[db_conversacion].find_one({"_id": ObjectId(id)}))
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)


@conversacion.put('/conversaciones/{id}', tags=["Conversacion"])
async def update_conversacion(id: str, conversacion: Conversacion, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        nueva_conversacion = jsonable_encoder(conversacion)
        db[db_conversacion].find_one_and_update({"_id": ObjectId(id)}, {"$set": nueva_conversacion })
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    

@conversacion.delete('/conversaciones/{id}', tags=["Conversacion"])
async def delete_conversaciones(id: str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        conversacionEntity(db[db_conversacion].find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

@conversacion.get('/conversaciones/todas/usuario', response_model=List[Conversacion], tags=["Conversacion"])
async def find_conversaciones_by_usuario(request: Request):
    validez = check_token(request.headers["Authentication"])
    if validez:

        filtro = conversacionesDe(validez)
        conversaciones = conversacionesEntity(db[db_conversacion].find({ '$or' : filtro}))

        return conversaciones
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

@conversacion.get('/conversaciones/usuario/propietario/{email}', response_model=Conversacion, tags=["Conversacion"])
async def find_conversaciones_by_usuario(email:str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        filtro = conversacionesEntre(validez, email)
        conversacion = db[db_conversacion].find_one({ '$and' : filtro})

        if conversacion is None:
            filtro = conversacionesEntre(email, validez)
            conversacion = db[db_conversacion].find_one({ '$and' : filtro})

            if conversacion is None:
                return None
            
            return conversacionEntity(conversacion)
        return conversacionEntity(conversacion)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)