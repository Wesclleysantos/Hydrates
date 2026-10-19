from app.metas import service

def definir_meta(usuario_id: int, quantidade_ml: int):
    return service.definir_meta(
        usuario_id=usuario_id,
        quantidade_ml=quantidade_ml,
    )

def calcular_meta_automatica(usuario_id: int):
    return service.calcular_meta_automatica(usuario_id)

def consultar_progresso(usuario_id: int):
    return service.consultar_progresso(
        usuario_id=usuario_id,
    )