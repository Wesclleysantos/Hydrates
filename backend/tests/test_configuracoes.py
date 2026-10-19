from unittest.mock import patch
import pytest
from app.configuracoes import service

def test_agenda_lembretes_gera_horarios_no_intervalo():
    configuracoes = {
        "usuario_id": 7,
        "lembretes_ativos": True,
        "intervalo_lembrete_minutos": 30,
        "horario_inicio": "08:00",
        "horario_fim": "09:00",
    }
    with patch("app.configuracoes.service.repository.buscar_configuracoes", return_value=configuracoes):
        agenda = service.consultar_agenda_lembretes(7)

    assert agenda["horarios"] == ["08:00", "08:30", "09:00"]
    assert agenda["entrega_implementada"] is False

def test_agenda_nao_cria_horarios_quando_lembretes_estao_desativados():
    configuracoes = {
        "usuario_id": 7,
        "lembretes_ativos": False,
        "intervalo_lembrete_minutos": 30,
        "horario_inicio": "08:00",
        "horario_fim": "09:00",
    }
    with patch("app.configuracoes.service.repository.buscar_configuracoes", return_value=configuracoes):
        agenda = service.consultar_agenda_lembretes(7)

    assert agenda["horarios"] == []

def test_atualizacao_rejeita_janela_invertida():
    with pytest.raises(ValueError, match="anterior"):
        service.atualizar_configuracoes(7, True, 30, "10:00", "09:00")
        