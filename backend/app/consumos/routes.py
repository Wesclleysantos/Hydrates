from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.consumos import controller
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/consumos", tags=["Consumos"])

class CadastroConsumo(BaseModel):
    bebida_id: int = Field(gt=0)
    quantidade_ml: int = Field(gt=0)

@router.post("", status_code=201)
def registrar_consumo(
    dados: CadastroConsumo,
    usuario_id: int = Depends(obter_usuario_atual)
):
    return controller.registrar_consumo(
        usuario_id=usuario_id,
        bebida_id=dados.bebida_id,
        quantidade_ml=dados.quantidade_ml,
    )


@router.get("")
def listar_consumos(
    usuario_id: int = Depends(obter_usuario_atual)
):
    return controller.listar_consumos(usuario_id=usuario_id)
