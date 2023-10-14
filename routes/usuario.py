from fastapi import APIRouter, Response, status, Request, Body
from starlette.status import *
from fastapi.encoders import jsonable_encoder
import time

usuario = APIRouter()
tokens = []

def check_token(nuevo_token: str):
    ts = time.time()

    if len(tokens) > 0:
        for token in tokens:
            if (token["id_token"] == nuevo_token) and (token["expires_at"] >= ts) :
                return token["email"]

    return False

#region TOKENS
# OBTENER TODOS LOS TOKENS
@usuario.get('/usuarios/tokens/todos')
async def token(request: Request):

    validez = check_token(request.headers["Authentication"])

    if validez:
        return jsonable_encoder(tokens)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

# CREAR TOKEN
@usuario.put('/usuarios/token/nuevo', tags=["Usuario"])
async def insert_token(token = Body(None)):
    nuevo_token = jsonable_encoder(token)
    tokens.append(nuevo_token)
    return Response(status_code=HTTP_204_NO_CONTENT)

# BORRAR TOKEN
@usuario.put('/usuarios/token/borrar', tags=["Usuario"])
async def delete_token(request: Request, token = Body(None)):

    nuevo_token = jsonable_encoder(token)

    encontrado = False
    indice = 0

    while not encontrado and indice < len(tokens):
        token = tokens[indice]
        if (token["id_token"] == nuevo_token) :
             encontrado = True
        else:
            indice = indice + 1
                
    tokens.pop(indice)

    return Response(status_code=HTTP_204_NO_CONTENT)
#endregion