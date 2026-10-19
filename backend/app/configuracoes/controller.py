from app.configuracoes import service

def consultar_configuracoes(usuario_id: int):
    return service.consultar_configuracoes(
        usuario_id=usuario_id,
    )

def atualizar_configuracoes(
    usuario_id: int,
    lembretes_ativos: bool,
    intervalo_lembrete_minutos: int,
    horario_inicio: str | None,
    horario_fim: str | None,
):
    return service.atualizar_configuracoes(
        usuario_id=usuario_id,
        lembretes_ativos=lembretes_ativos,
        intervalo_lembrete_minutos=intervalo_lembrete_minutos,
        horario_inicio=horario_inicio,
        horario_fim=horario_fim,
    )
