from app.conquistas import repository

def listar_conquistas_ativas():
    return repository.listar_conquistas_ativas()

def listar_conquistas_usuario(usuario_id: int):
    return repository.listar_conquistas_usuario(
        usuario_id=usuario_id,
    )

def desbloquear_conquista(usuario_id: int, conquista_id: int):
    try:
        return repository.desbloquear_conquista(
            usuario_id=usuario_id,
            conquista_id=conquista_id,
        )

    except ValueError:
        raise

    except Exception as erro:
        if getattr(erro, "errno", None) == 1062:
            raise ValueError(
                "Essa conquista já foi desbloqueada por este usuário."
            ) from erro

        raise
