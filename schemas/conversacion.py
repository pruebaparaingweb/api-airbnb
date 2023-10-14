def conversacionEntity(conversacion) -> dict:
    return {
        "id" : str(conversacion["_id"]),
        "participante1" : conversacion["participante1"],
        "participante2" : conversacion["participante2"],
        "mensajes" : conversacion["mensajes"]
    }
    
def conversacionesEntity(conversaciones) -> list:
    return [conversacionEntity(conversacion) for conversacion in conversaciones]

def mensajeEntity(mensaje) -> dict:
    return {
        "emisor" : mensaje["emisor"],
        "receptor" : mensaje["receptor"],
        "contenido" : mensaje["contenido"],
        "fecha": mensaje["fecha"]
    }
    
def mensajesEntity(mensajes) -> list:
    return [mensajeEntity(mensaje) for mensaje in mensajes]

def conversacionesDe(usuario) -> list:

    return [
        {"participante1" : { "$regex" : "(?i)" + usuario}},
        {"participante2" : { "$regex" : "(?i)" + usuario}}
    ]

def conversacionesEntre(usuario1, usuario2) -> list:

    return [
        {"participante1" : { "$regex" : "(?i)" + usuario1}},
        {"participante2" : { "$regex" : "(?i)" + usuario2}}
    ]