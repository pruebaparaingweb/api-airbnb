from fastapi import APIRouter, Response, Body, Request #APIRouter: nos permite definir todas las rutas dentro de este archivo
from config.db import db
from bson import ObjectId
from models.vivienda import *
from schemas.vivienda import *
from starlette.status import *
from fastapi.encoders import jsonable_encoder
from typing import List
import cloudinary
from routes.usuario import *
from routes.reserva import *

cloudinary.config( 
  # cloud_name = "web2022", 
  # api_key = "758781561277471", 
  # api_secret = "QsVHbVQ5Z_K-_kNzJiJ94-fAuWk" 

  cloud_name = "canallcc",
  api_key = "576949413175551",
  api_secret = "wrvazJg3fAPO18hSUlQJMsTba6M" 

)
import cloudinary.uploader
import cloudinary.api

vivienda = APIRouter()
db_vivienda = "vivienda"

#region FIND ALL VIVIENDAS
# ENCONTRAR TODAS LAS VIVIENDAS
@vivienda.get('/viviendas', response_model=List[Vivienda], tags=["Vivienda"])
async def find_all_viviendas(request: Request):
    # validez = check_token(request.headers["Authentication"])
    validez = True

    if validez:
        viviendas = viviendasEntity(db[db_vivienda].find())
        return viviendas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region CRUD VIVIENDA
# ENCONTRAR VIVIENDA POR ID
@vivienda.get('/viviendas/{id}', response_model=Vivienda, tags=["Vivienda"])
async def find_vivienda_by_id(id: str, request: Request):
    # validez = check_token(request.headers["Authentication"])
    validez = True

    if validez:
        return viviendaEntity(db[db_vivienda].find_one({"_id": ObjectId(id)}))
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    
# CREAR VIVIENDA
@vivienda.post('/viviendas', response_model=Vivienda, tags=["Vivienda"])
async def create_vivienda(vivienda: Vivienda, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        nueva_vivienda = jsonable_encoder(vivienda)   
        del nueva_vivienda["id"]
        id = db[db_vivienda].insert_one(nueva_vivienda).inserted_id
        vivienda = viviendaEntity(db[db_vivienda].find_one({"_id": id}))
        return vivienda
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    
# ACTUALIZAR VIVIENDA
@vivienda.put('/viviendas/{id}', tags=["Vivienda"])
async def update_vivienda(id: str, vivienda: Vivienda, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        nueva_vivienda = jsonable_encoder(vivienda) 
        db[db_vivienda].find_one_and_update({"_id": ObjectId(id)}, {"$set": nueva_vivienda })
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

# BORRAR VIVIENDA
@vivienda.delete('/viviendas/{id}', tags=["Vivienda"])
async def delete_vivienda(id: str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        vivienda = viviendaEntity(db[db_vivienda].find_one_and_delete({"_id": ObjectId(id)}))

        for url in vivienda["fotos"]:
            url = url.split("/")
            idFoto = url[len(url) - 1]
            idFoto = idFoto.split(".")[0]
            cloudinary.uploader.destroy(idFoto)

        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region ENCONTRAR VIVIENDAS DE UN PROPIETARIO
@vivienda.get('/viviendas/misviviendas/propietario', response_model=List[Vivienda], tags=["Vivienda"])
async def find_viviendas_by_propietario(request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        return viviendasEntity(db[db_vivienda].find({"propietario": validez}))
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region ENCONTRAR VIVIENDAS POR PRECIO, FECHAS Y MUNICIPIO
@vivienda.post('/viviendas/filtro/precio',response_model=List[Vivienda],tags=["Vivienda"])
async def find_viviendas_by_precio_municipio_y_fecha(menor:float,mayor:float,municipio:str,fechaInicio:str,fechaFin:str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        filtro = filtroMultiplePrecio(menor,mayor,municipio)
        viviendas = viviendasEntity(db[db_vivienda].find({'$and': filtro}).sort("precio"))
        viviendasFiltradas = []

        for v in viviendas:
            cumple = True
            i = 0
            while i in range(len(v["reservas"])) and cumple:
                if not (v["fechaInicio"] >= fechaFin or v["fechaFin"] <= fechaInicio):
                    cumple = False
                i = i + 1
            if(cumple):
                viviendasFiltradas.append(v)

        return viviendasFiltradas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region ENCONTRAR VIVIENDAS POR HUESPEDES, FECHAS Y MUNICIPIO
@vivienda.post('/viviendas/filtro/huespedes',response_model=List[Vivienda],tags=["Vivienda"])
async def find_viviendas_by_huespedes_municipio_y_fecha(huespedes:int,municipio:str,fechaInicio:str,fechaFin:str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        filtro = filtroMultipleHuespedes(huespedes,municipio)
        viviendas = viviendasEntity(db[db_vivienda].find({'$and': filtro}).sort("precio"))
        viviendasFiltradas = []

        for v in viviendas:
            cumple = True
            i = 0
            while i in range(len(v["reservas"])) and cumple:
                if not (v["fechaInicio"] >= fechaFin or v["fechaFin"] <= fechaInicio):
                    cumple = False
                i = i + 1
            if(cumple):
                viviendasFiltradas.append(v)

        return viviendasFiltradas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region ENCONTRAR VIVIENDAS POR HUESPEDES, FECHAS, MUNICIPIO Y PRECIOS
@vivienda.post('/viviendas/filtro/multiple',response_model=List[Vivienda],tags=["Vivienda"])
async def find_viviendas_by_huespedes_municipio_y_fecha(menor:float,mayor:float,huespedes:int,municipio:str,fechaInicio:str,fechaFin:str, request: Request):
    validez = check_token(request.headers["Authentication"])
    if validez:
        filtro = filtroMultiple(menor,mayor,huespedes,municipio)
        viviendas = viviendasEntity(db[db_vivienda].find({'$and': filtro}).sort("precio"))
        viviendasFiltradas = []
        
        for v in viviendas:
            cumple = True
            i = 0
            
            if v["reservas"] != None:
                while i in range(len(v["reservas"])) and cumple:
                    
                    if not (v["reservas"][i]["fechaInicio"] >= fechaFin or v["reservas"][i]["fechaFin"] <= fechaInicio):
                        cumple = False
                    i = i + 1
            if(cumple):
                viviendasFiltradas.append(v)

        return viviendasFiltradas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region CREAR Y BORRAR IMAGEN    
# CREAR NUEVA IMAGEN PARA UNA VIVIENDA
@vivienda.post('/viviendas/{id}/imagen/', tags=["Vivienda"])
async def new_imagen_for_vivienda(id: str, request: Request, url: str = Body(None)):
    validez = check_token(request.headers["Authentication"])

    if validez:
        try :
            vivienda = viviendaEntity(db[db_vivienda].find_one({"_id": ObjectId(id)}))
            vivienda["fotos"].append(url)
            db[db_vivienda].find_one_and_update({"_id": ObjectId(id)}, {"$set": vivienda })
        except Exception as e :
            print(e)

        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

# BORRAR IMAGEN DE UNA VIVIENDA
@vivienda.put('/viviendas/{id}/imagen/{indice}/delete', tags=["Vivienda"])
async def delete_image_from_vivienda(id:str, indice: int, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        vivienda = viviendaEntity(db[db_vivienda].find_one({"_id": ObjectId(id)}))
        urlActual = vivienda["fotos"].pop(indice)
        db[db_vivienda].find_one_and_update({"_id": ObjectId(id)}, {"$set": vivienda })
        urlActual = urlActual.split("/")
        idFoto = urlActual[len(urlActual) - 1]
        idFoto = idFoto.split(".")[0]

        cloudinary.uploader.destroy(idFoto)

        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region ENCONTRAR TODAS LAS LOCALIZACIONES DE TODAS LAS VIVIENDAS
@vivienda.get('/viviendas/localizaciones/latlon', tags=["Vivienda"])
async def find_all_localizaciones(request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        localizaciones = db[db_vivienda].find({},{'_id':0,'localizacion':1})
        coordenadas = []
        for l in localizaciones:
            coordenadas.append((l["localizacion"]["lat"],l["localizacion"]["lon"]))
        return coordenadas
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion

#region NO USADAS EN JINJA
###########################################
# ENCONTRAR RESERVAS DE VIVIENDA POR NOMBRE
@vivienda.get('/viviendas/viviendaNombre/{nombreVivienda}', response_model=List[ReservaVivienda], tags=["Vivienda"])
async def find_reservas_by_nombreVivienda(nombreVivienda: str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        vivienda = viviendaEntity(db[db_vivienda].find_one({"nombre": nombreVivienda}))
        return vivienda["reservas"]
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

# ENCONTRAR TODOS LOS HUESPEDES DE UN PROPIETARIO
@vivienda.get('/viviendas/huespedesPropietario/{propietario}', response_model=List[str], tags=["Vivienda"])
async def find_huespedes_by_propietarioId(propietario: str, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        viviendas = viviendasEntity(db[db_vivienda].find({"propietario": propietario}))
        lista = []
        for v in viviendas:
            for r in v["reservas"]:
                lista.append(r["username"])
        return lista
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)

# ENCONTRAR VIVIENDAS EN UNA LOCALIZACION
@vivienda.post('/viviendas/localizacion', response_model=List[Vivienda], tags=["Vivienda"])
async def find_vivienda_by_localizacion(request: Request, l : Localizacion = Body(None)):
    validez = check_token(request.headers["Authentication"])

    if validez:
        localizacion = jsonable_encoder(l)

        filtro = localizacionFiltrar(localizacion)
        viviendas = db[db_vivienda].find({ '$and' : filtro})
    
        return viviendasEntity(viviendas)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    
# ENCONTRAR VIVIENDAS EN UN RANGO DE PRECIOS
@vivienda.post('/viviendas/rangoPrecios', response_model=List[Vivienda],tags=["Vivienda"])
async def find_viviendas_by_PrecioRange(menor: float , mayor:float, request: Request):
    validez = check_token(request.headers["Authentication"])

    if validez:
        filtro = preciosFiltrar(menor,mayor)
        return viviendasEntity(db[db_vivienda].find({ '$and' : filtro}).sort("precio"))
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
#endregion