from datetime import time
from app.configuracoes import repository

def consultar_configuracoes(usuario_id: int):
    configuracoes = repository.buscar_configuracoes(usuario_id)

    if configuracoes:
        return configuracoes

    return {
        "usuario_id": usuario_id,
        "lembretes_ativos": True,
        "intervalo_lembrete_minutos": 60,
        "horario_inicio": None,
        "horario_fim": None,
    }

def atualizar_configuracoes(
    usuario_id: int,
    lembretes_ativos: bool,
    intervalo_lembrete_minutos: int,
    horario_inicio: str | None,
    horario_fim: str | None,
):
    if intervalo_lembrete_minutos <= 0:
        raise ValueError("O intervalo deve ser maior que zero.")

    if (horario_inicio is None) != (horario_fim is None):
        raise ValueError(
            "Informe os horários de início e fim juntos."
        )

    if horario_inicio is not None and horario_fim is not None:
        try:
            inicio = time.fromisoformat(horario_inicio)
            fim = time.fromisoformat(horario_fim)
        except ValueError:
            raise ValueError("Informe horários válidos no formato HH:MM.")

        if inicio >= fim:
            raise ValueError(
                "O horário de início deve ser anterior ao horário de fim."
            )

    return repository.salvar_configuracoes(
        usuario_id=usuario_id,
        lembretes_ativos=lembretes_ativos,
        intervalo_lembrete_minutos=intervalo_lembrete_minutos,
        horario_inicio=horario_inicio,
        horario_fim=horario_fim,
    )
