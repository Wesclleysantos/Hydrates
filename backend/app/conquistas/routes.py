from fastapi import APIRouter, Depends, HTTPException
from app.conquistas import controller
from app.dependencies import obter_usuario_atual

router = APIRouter(
    prefix="/conquistas",
    tags=["Conquistas"],
)

@router.get("/")
def listar_conquistas_ativas():
    return controller.listar_conquistas_ativas()

@router.get("/usuario")
def listar_conquistas_usuario(
    usuario_id: int = Depends(obter_usuario_atual),
):
    return controller.listar_conquistas_usuario(
        usuario_id=usuario_id,
    )

@router.post("/desbloquear/{conquista_id}")
def desbloquear_conquista(
    conquista_id: int,
    usuario_id: int = Depends(obter_usuario_atual),
):
    try:
        conquista = controller.desbloquear_conquista(
            usuario_id=usuario_id,
            conquista_id=conquista_id,
        )

        if conquista is None:
            raise HTTPException(
                status_code=409,
                detail="Esta conquista já foi desbloqueada.",
            )

        return {
            "mensagem": "Conquista desbloqueada com sucesso.",
            "id": conquista,
            "usuario_id": usuario_id,
            "conquista_id": conquista_id,
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro),
        )
