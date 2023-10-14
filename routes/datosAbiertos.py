from typing import List
import requests
from fastapi import APIRouter, Request, Response
from routes import usuario
import time
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

datosAbiertos = APIRouter()

def check_token(nuevo_token: str):
    ts = time.time()

    if len(usuario.tokens) > 0:
        for token in usuario.tokens:
            if (token["id_token"] == nuevo_token) and (token["expires_at"] >= ts) :
                return True

    return False

@datosAbiertos.get('/tiempo', response_model=List[dict], tags=["Tiempo"])
async def find_tiempo_by_municipio(nombreMunicipio: str, request: Request):

    validez = check_token(request.headers["Authentication"])

    if validez:
        # data1 = requests.get("https://www.el-tiempo.net/api/json/v2/provincias/29/municipios").json()
        # municipio = ""
        
        # for i in data1:
        #    if i['NOMBRE'].lower() == nombreMunicipio.lower():
        #        municipio = i['CODIGOINE'][0:5]
        

        data2 = requests.get("https://www.el-tiempo.net/api/json/v1/provincias/29/municipios/29001/weather")

        if data2.status_code == 404:
            return []

        data2 = data2.json()

        lista = []
    
        for x in data2['prediccion']['dia']:
            lista.append({
                "municipio": nombreMunicipio,
                "fecha": str(x['@attributes']['fecha']),
                "probabilidadPrecipitacion": str(x['prob_precipitacion']), 
                "humedadMaxima": str(x['humedad_relativa']['maxima']),
                "humedadMinima": str(x['humedad_relativa']['minima']),
                "temperaturaMaxima": str(x['temperatura']['maxima']),
                "temperaturaMinima": str(x['temperatura']['minima']),
                "viento": str(x['viento'])
            })

        return lista
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    
    

@datosAbiertos.get('/tiempo/{nMunicipio}/{fecha}', response_model=List[dict], tags=["Tiempo"])
async def find_tiempo_by_municipio_and_fecha(nMunicipio: str, fecha: str, request: Request):

    validez = check_token(request.headers["Authentication"])

    if validez:
        nombreMunicipio = nMunicipio

        data1 = requests.get("http://www.el-tiempo.net/api/json/v1/municipios").json()

        municipio = ""

        for i in data1:
            if i['NOMBRE'] == nombreMunicipio:
                municipio = i['CODIGOINE'][0:5]

        data2 = requests.get("http://www.el-tiempo.net/api/json/v1/municipios/" + str(municipio) + "/weather").json()

        lista = []

        for x in data2['prediccion']['dia']:
            if(str(x['@attributes']['fecha']) == fecha):
                lista.append({
                    "municipio": nombreMunicipio,
                    "fecha": str(x['@attributes']['fecha']),
                    "probabilidadPrecipitacion": str(x['prob_precipitacion']), 
                    "humedadMaxima": str(x['humedad_relativa']['maxima']),
                    "humedadMinima": str(x['humedad_relativa']['minima']),
                    "temperaturaMaxima": str(x['temperatura']['maxima']),
                    "temperaturaMinima": str(x['temperatura']['minima']),
                    "viento": str(x['viento'])}
                )
            
        return lista
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    


@datosAbiertos.get('/transporteMalaga/{latitud}/{longitud}', response_model=List[dict], tags=["Transporte"])
async def find_transporte_by_lat_and_long(latitud: float, longitud: float, request: Request):

    validez = check_token(request.headers["Authentication"])

    if validez:
        data1 = requests.get("http://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasYParadas/lineasyparadas.geojson").json()

        lista = []

        for i in data1:
            for x in i['paradas']:
                if((float(x['parada']['latitud']) - latitud).__abs__() <= 0.0033 and (float(x['parada']['longitud']) - longitud).__abs__() <= 0.0033):
                    lista.append(({"nombreParada": str(x['parada']['nombreParada']),
                                            "nombreLinea": str(i['nombreLinea']), 
                                            "codLinea": str(i['codLinea']),
                                            "latitud": str(x['parada']['latitud']),
                                            "longuitud": str(x['parada']['longitud'])}))

        return lista
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)