from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.configuracoes import controller
from app.dependencies import obter_usuario_atual

router = APIRouter(
    prefix="/configuracoes",
    tags=["Configurações"],
)

class ConfiguracoesEntrada(BaseModel):
    lembretes_ativos: bool = True
    intervalo_lembrete_minutos: int = Field(default=60, gt=0)
    horario_inicio: str | None = None
    horario_fim: str | None = None

@router.get("")
def consultar_configuracoes(
    usuario_id: int = Depends(obter_usuario_atual),
):
    return controller.consultar_configuracoes(usuario_id=usuario_id)

@router.put("")
def atualizar_configuracoes(
    dados: ConfiguracoesEntrada,
    usuario_id: int = Depends(obter_usuario_atual),
):
    try:
        return controller.atualizar_configuracoes(
            usuario_id=usuario_id,
            lembretes_ativos=dados.lembretes_ativos,
            intervalo_lembrete_minutos=dados.intervalo_lembrete_minutos,
            horario_inicio=dados.horario_inicio,
            horario_fim=dados.horario_fim,
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

@router.get("/lembretes/agenda")
def consultar_agenda_lembretes(
    usuario_id: int = Depends(obter_usuario_atual),
):
    return controller.consultar_agenda_lembretes(usuario_id)
