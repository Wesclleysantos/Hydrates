from datetime import date
from unittest.mock import patch
import pytest
from app.consumos import service

def test_registrar_consumo_aplica_fator_e_verifica_conquistas():
    bebida = {"id": 2, "nome": "Café", "fator_hidratacao": 0.8, "activo": True}
    with (
        patch("app.consumos.service.bebidas_repository.buscar_por_id", return_value=bebida),
        patch("app.consumos.service.repository.criar_consumo", return_value=15) as criar,
        patch("app.consumos.service.conquistas_service.verificar_conquistas", return_value=[]) as verificar,
    ):
        resultado = service.registrar_consumo(7, 2, 250)

    assert resultado["hidratacao_ml"] == 200
    assert resultado["id"] == 15
    criar.assert_called_once_with(
        usuario_id=7,
        bebida_id=2,
        quantidade_ml=250,
        hidratacao_ml=200,
    )
    verificar.assert_called_once_with(7)

def test_registrar_consumo_rejeita_bebida_inativa():
    bebida = {"nome": "Água", "fator_hidratacao": 1, "activo": False}
    with patch("app.consumos.service.bebidas_repository.buscar_por_id", return_value=bebida):
        with pytest.raises(ValueError, match="inativa"):
            service.registrar_consumo(7, 1, 250)

def test_resumo_preenche_dias_sem_consumo():
    inicio = date(2026, 1, 1)
    fim = date(2026, 1, 3)
    registros = [{
        "data_consumo": date(2026, 1, 2),
        "quantidade_ml": 300,
        "hidratacao_ml": 270,
        "registros": 2,
    }]
    with patch("app.consumos.service.repository.resumir_consumos", return_value=registros):
        resultado = service.resumir_consumos(7, inicio, fim)

    assert [dia["registros"] for dia in resultado["dias"]] == [0, 2, 0]
    assert resultado["total_hidratacao_ml"] == 270

def test_resumo_exige_as_duas_datas():
    with pytest.raises(ValueError, match="juntas"):
        service.resumir_consumos(7, date(2026, 1, 1), None)
        