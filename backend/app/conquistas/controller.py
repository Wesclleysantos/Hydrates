from app.conquistas import service

def listar_conquistas_ativas():
    return service.listar_conquistas_ativas()

def listar_conquistas_usuario(usuario_id: int):
    return service.listar_conquistas_usuario(
        usuario_id=usuario_id,
    )

def desbloquear_conquista(usuario_id: int, conquista_id: int):
    return service.desbloquear_conquista(
        usuario_id=usuario_id,
        conquista_id=conquista_id,
    )
