from fastapi import FastAPI, Request
from routes.vivienda import vivienda
from routes.usuario import usuario
from routes.reserva import reserva
from routes.conversacion import conversacion
from routes.datosAbiertos import datosAbiertos
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="A4ServidorRest",
    description="Servidor API REST para microservicios grupo A4",
    version="0.1.0"
)

appAbiertos = FastAPI(
    title="A4AbiertosRest",
    description="API REST para los datos abiertos",
    version="0.1.0"
)

app.include_router(vivienda) #me incluye todas las rutas definidas para la vivienda
app.include_router(usuario)
app.include_router(reserva)
app.include_router(conversacion)
app.include_router(datosAbiertos)

@app.get("/", include_in_schema=False)
async def redirect(request: Request):
    return RedirectResponse(request.url._url + "docs")
