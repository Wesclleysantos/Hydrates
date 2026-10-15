from fastapi import APIRouter
from app.bebidas import controller
from pydantic import BaseModel, Field

router = APIRouter(prefix="/bebidas", tags=["Bebidas"])

class CadastroBebida(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    fator_hidratacao: float = Field(gt=0, le=1)

@router.get("")
def listar_bebidas():
    return controller.listar_bebidas()

@router.post("", status_code=201)
def cadastrar_bebida(dados: CadastroBebida):
    return controller.cadastrar_bebida(
        nome = dados.nome,
        fator_hidratacao = dados.fator_hidratacao,
    )
