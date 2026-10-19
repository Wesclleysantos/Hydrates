from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.metas import controller
from app.dependencies import obter_usuario_atual

router = APIRouter(
    prefix="/metas",
    tags=["Metas"],
)

class MetaEntrada(BaseModel):
    quantidade_ml: int = Field(gt=0)

@router.put("")
def definir_meta(
    dados: MetaEntrada,
    usuario_id: int = Depends(obter_usuario_atual),
):
    try:
        return controller.definir_meta(
            usuario_id=usuario_id,
            quantidade_ml=dados.quantidade_ml,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro),
        )

@router.get("/progresso")
def consultar_progresso(
    usuario_id: int = Depends(obter_usuario_atual),
):
    return controller.consultar_progresso(
        usuario_id=usuario_id,
    )
