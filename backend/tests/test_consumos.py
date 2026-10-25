from datetime import date
from unittest.mock import patch

import pytest

from app.consumos import service


def test_registrar_consumo_aplica_fator_e_verifica_conquistas():
    bebida = {"id": 2, "nome": "Café", "fator_hidratacao": 0.8, "activo": True}
    with (
        patch(
            "app.consumos.service.bebidas_repository.buscar_por_id",
            return_value=bebida,
        ) as buscar_bebida,
        patch(
            "app.consumos.service.repository.criar_consumo",
            return_value=15,
        ) as criar,
        patch(
            "app.consumos.service.conquistas_service.verificar_conquistas",
            return_value=[],
        ) as verificar,
    ):
        resultado = service.registrar_consumo(7, 2, 250)

    assert resultado["hidratacao_ml"] == 200
    assert resultado["id"] == 15
    buscar_bebida.assert_called_once_with(bebida_id=2, usuario_id=7)
    criar.assert_called_once_with(
        usuario_id=7,
        bebida_id=2,
        quantidade_ml=250,
        hidratacao_ml=200,
    )
    verificar.assert_called_once_with(7)


def test_registrar_consumo_rejeita_bebida_inativa():
    bebida = {"nome": "Água", "fator_hidratacao": 1, "activo": False}
    with patch(
        "app.consumos.service.bebidas_repository.buscar_por_id",
        return_value=bebida,
    ):
        with pytest.raises(ValueError, match="inativa"):
            service.registrar_consumo(7, 1, 250)


def test_resumo_separa_bebidas_e_preenche_dias_sem_consumo():
    inicio = date(2026, 1, 1)
    fim = date(2026, 1, 3)
    registros = [{
        "data_consumo": date(2026, 1, 2),
        "bebida_id": 2,
        "bebida": "Café",
        "quantidade_ml": 300,
        "hidratacao_ml": 270,
        "registros": 2,
    }]

    with patch(
        "app.consumos.service.repository.resumir_consumos_diario_por_bebida",
        return_value=registros,
    ) as resumir:
        resultado = service.resumir_consumos(7, inicio, fim)

    resumir.assert_called_once_with(
        usuario_id=7,
        data_inicio=inicio,
        data_fim=fim,
        bebida_id=None,
    )
    assert resultado["datas"] == [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
    ]
    assert resultado["bebidas"][0]["bebida"] == "Café"
    assert [
        dia["registros"]
        for dia in resultado["bebidas"][0]["dias"]
    ] == [0, 2, 0]
    assert [
        dia["hidratacao_ml"]
        for dia in resultado["bebidas"][0]["dias"]
    ] == [0, 270, 0]
    assert resultado["total_hidratacao_ml"] == 270


def test_resumo_diario_filtra_bebida_do_usuario_e_preenche_dias():
    inicio = date(2026, 1, 1)
    fim = date(2026, 1, 3)
    bebida = {"id": 2, "nome": "Café", "fator_hidratacao": 0.8, "activo": True}
    registros = [{
        "data_consumo": date(2026, 1, 2),
        "bebida_id": 2,
        "bebida": "Café",
        "quantidade_ml": 250,
        "hidratacao_ml": 200,
        "registros": 1,
    }]

    with (
        patch(
            "app.consumos.service.bebidas_repository.buscar_por_id",
            return_value=bebida,
        ) as buscar_bebida,
        patch(
            "app.consumos.service.repository.resumir_consumos_diario_por_bebida",
            return_value=registros,
        ) as resumir,
    ):
        resultado = service.resumir_consumos_diario_por_bebida(
            usuario_id=7,
            bebida_id=2,
            data_inicio=inicio,
            data_fim=fim,
        )

    buscar_bebida.assert_called_once_with(bebida_id=2, usuario_id=7)
    resumir.assert_called_once_with(
        usuario_id=7,
        data_inicio=inicio,
        data_fim=fim,
        bebida_id=2,
    )
    assert len(resultado["bebidas"]) == 1
    assert resultado["bebidas"][0]["bebida_id"] == 2
    assert [
        dia["quantidade_ml"]
        for dia in resultado["bebidas"][0]["dias"]
    ] == [0, 250, 0]
    assert resultado["bebidas"][0]["total_hidratacao_ml"] == 200


def test_resumo_diario_rejeita_bebida_de_outro_usuario():
    with (
        patch(
            "app.consumos.service.bebidas_repository.buscar_por_id",
            return_value=None,
        ),
        patch(
            "app.consumos.service.repository.resumir_consumos_diario_por_bebida",
        ) as resumir,
    ):
        with pytest.raises(LookupError, match="Bebida não encontrada"):
            service.resumir_consumos_diario_por_bebida(
                usuario_id=7,
                bebida_id=99,
                data_inicio=date(2026, 1, 1),
                data_fim=date(2026, 1, 3),
            )

    resumir.assert_not_called()


def test_resumo_exige_as_duas_datas():
    with pytest.raises(ValueError, match="juntas"):
        service.resumir_consumos(7, date(2026, 1, 1), None)