from fastapi import HTTPException, status
from app.consumos import service


def registrar_consumo(
    usuario_id: int,
    bebida_id: int,
    quantidade_ml: int,
):
    try:
        return service.registrar_consumo(
            usuario_id=usuario_id,
            bebida_id=bebida_id,
            quantidade_ml=quantidade_ml,
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )


def listar_consumos(usuario_id: int):
    return service.listar_consumos(usuario_id)
