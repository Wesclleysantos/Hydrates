from datetime import datetime, time, timedelta
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

def _converter_horario(valor) -> time:
    if isinstance(valor, time):
        return valor
    if isinstance(valor, timedelta):
        segundos = int(valor.total_seconds()) % (24 * 60 * 60)
        horas, resto = divmod(segundos, 60 * 60)
        minutos, segundos = divmod(resto, 60)
        return time(horas, minutos, segundos)
    return time.fromisoformat(str(valor))

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
        raise ValueError("Informe os horários de início e fim juntos.")

    if horario_inicio is not None and horario_fim is not None:
        try:
            inicio = _converter_horario(horario_inicio)
            fim = _converter_horario(horario_fim)
        except (TypeError, ValueError) as erro:
            raise ValueError("Informe horários válidos no formato HH:MM.") from erro

        if inicio >= fim:
            raise ValueError("O horário de início deve ser anterior ao horário de fim.")

    return repository.salvar_configuracoes(
        usuario_id=usuario_id,
        lembretes_ativos=lembretes_ativos,
        intervalo_lembrete_minutos=intervalo_lembrete_minutos,
        horario_inicio=horario_inicio,
        horario_fim=horario_fim,
    )

def consultar_agenda_lembretes(usuario_id: int):
    configuracoes = consultar_configuracoes(usuario_id)
    inicio_raw = configuracoes.get("horario_inicio")
    fim_raw = configuracoes.get("horario_fim")
    horarios = []

    if (
        configuracoes["lembretes_ativos"]
        and inicio_raw is not None
        and fim_raw is not None
    ):
        inicio = _converter_horario(inicio_raw)
        fim = _converter_horario(fim_raw)
        instante = datetime.combine(datetime.today(), inicio)
        limite = datetime.combine(datetime.today(), fim)
        intervalo = timedelta(minutes=configuracoes["intervalo_lembrete_minutos"])

        while instante <= limite:
            horarios.append(instante.strftime("%H:%M"))
            instante += intervalo

    return {
        "usuario_id": usuario_id,
        "lembretes_ativos": configuracoes["lembretes_ativos"],
        "intervalo_lembrete_minutos": configuracoes["intervalo_lembrete_minutos"],
        "horario_inicio": inicio_raw,
        "horario_fim": fim_raw,
        "horarios": horarios,
        "entrega_implementada": False,
    }
