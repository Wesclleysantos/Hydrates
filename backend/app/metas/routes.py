from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.metas import controller

router = APIRouter(
    prefix="/metas",
    tags=["Metas"],
)

class MetaEntrada(BaseModel):
    quantidade_ml: int = Field(gt=0)

@router.put("/{usuario_id}")
def definir_meta(usuario_id: int, dados: MetaEntrada):
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

@router.get("/{usuario_id}/progresso")
def consultar_progresso(usuario_id: int):
    return controller.consultar_progresso(
        usuario_id=usuario_id,
    )
