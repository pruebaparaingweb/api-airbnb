def reservaEntity(reserva) -> dict:
    return {
        "fechaInicio" : reserva["fechaInicio"],
        "fechaFin" : reserva["fechaFin"],
        "username" : reserva["username"],
        "vivienda" : reserva["vivienda"],
        "precio" : reserva["precio"]
    }
    
def reservasEntity(reservas) -> list:
    return [reservaEntity(reserva) for reserva in reservas]
