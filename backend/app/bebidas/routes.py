from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.bebidas import controller
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/bebidas")

class CadastroBebida(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    fator_hidratacao: float = Field(gt=0, le=1)

class AtualizacaoBebida(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    fator_hidratacao: float = Field(gt=0, le=1)

@router.get("", tags=["Bebidas"])
def listar_bebidas(
    usuario_id: int = Depends(obter_usuario_atual),
):
    return controller.listar_bebidas(usuario_id=usuario_id)

@router.post("", status_code=201, tags=["Bebidas"])
def cadastrar_bebida(
    dados: CadastroBebida,
    usuario_id: int = Depends(obter_usuario_atual),
):
    try:
        return controller.cadastrar_bebida(
            usuario_id=usuario_id,
            nome=dados.nome,
            fator_hidratacao=dados.fator_hidratacao,
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))

@router.put("/{bebida_id}", tags=["Bebidas"])
def atualizar_bebida(
    bebida_id: int,
    dados: AtualizacaoBebida,
    usuario_id: int = Depends(obter_usuario_atual),
):
    try:
        return controller.atualizar_bebida(
            usuario_id=usuario_id,
            bebida_id=bebida_id,
            nome=dados.nome,
            fator_hidratacao=dados.fator_hidratacao,
        )
    except LookupError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    