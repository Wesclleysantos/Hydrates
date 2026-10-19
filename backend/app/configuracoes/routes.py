from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.configuracoes import controller

router = APIRouter(
    prefix="/configuracoes",
    tags=["Configurações"],
)

class ConfiguracoesEntrada(BaseModel):
    lembretes_ativos: bool = True
    intervalo_lembrete_minutos: int = Field(default=60, gt=0)
    horario_inicio: str | None = None
    horario_fim: str | None = None

@router.get("/{usuario_id}")
def consultar_configuracoes(usuario_id: int):
    return controller.consultar_configuracoes(
        usuario_id=usuario_id,
    )

@router.put("/{usuario_id}")
def atualizar_configuracoes(
    usuario_id: int,
    dados: ConfiguracoesEntrada,
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
        raise HTTPException(
            status_code=400,
            detail=str(erro),
        )
