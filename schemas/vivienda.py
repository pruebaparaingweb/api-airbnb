
def viviendaEntity(vivienda) -> dict:
    return {
        "id" : str(vivienda["_id"]),
        "nombre" : vivienda["nombre"],
        "descripcion" : vivienda["descripcion"],
        "precio" : vivienda["precio"],
        "capacidad" : vivienda["capacidad"],
        "localizacion" : vivienda["localizacion"],
        "propietario" : vivienda["propietario"],
        "reservas" : vivienda["reservas"],
        "fotos" : vivienda["fotos"],
        "valoracion" : vivienda["valoracion"],
        "reseñas" : vivienda["reseñas"]
    }

def viviendasEntity(viviendas) -> list:
    return [viviendaEntity(vivienda) for vivienda in viviendas]  

def localizacionFiltrar(localizacion) -> list:

    return [
        {"localizacion.pais" : { "$regex" : "(?i)" + localizacion["pais"]}},
        {"localizacion.provincia" : { "$regex" : "(?i)" + localizacion["provincia"]}},
        {"localizacion.municipio" : { "$regex" : "(?i)" + localizacion["municipio"]}},
        {"localizacion.cp" : { "$regex" : "(?i)" + localizacion["cp"]}},
        {"localizacion.calle" : { "$regex" : "(?i)" + localizacion["calle"]}},
        {"localizacion.numero" : { "$regex" : "(?i)" + localizacion["numero"]}},
        {"localizacion.numeroBloque" : { "$regex" : "(?i)" + localizacion["numeroBloque"]}}
    ]

def preciosFiltrar(menor, mayor) -> list:
    return [
        {"precio": {"$gte":menor}},
        {"precio": {"$lte":mayor}}
    ]

def filtroMultiplePrecio(menor,mayor,municipio) -> list:
    return [
        {"precio": {"$gte":menor}},
        {"precio": {"$lte":mayor}},
        {"localizacion.municipio" : { "$regex" : "(?i)" + municipio}} 
    ]
def filtroMultiple(menor,mayor,huespedes,municipio) -> list:
    return [
        {"precio": {"$gte":menor}},
        {"precio": {"$lte":mayor}},
        {"capacidad": {"$gte":huespedes}},
        {"localizacion.municipio" : { "$regex" : "(?i)" + municipio}} 
    ]

def filtroMultipleHuespedes(huespedes,municipio) -> list:
    return [
        {"capacidad": {"$gte":huespedes}},
        {"localizacion.municipio" : { "$regex" : "(?i)" + municipio}} 
    ]

#{ "reservas": { "$not": { "$elemMatch": { "username": { $ne: "pepe" } } } }, "reservas.username": "pepe" }