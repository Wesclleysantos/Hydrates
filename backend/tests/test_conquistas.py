from unittest.mock import MagicMock, patch
import pytest
from app.conquistas import repository, service

def test_verificar_conquistas_desbloqueia_apenas_criterios_cumpridos():
    conquistas = [
        {"id": 1, "nome": "Primeiro consumo", "descricao": "...", "pontos": 10, "criterio": "primeiro_consumo"},
        {"id": 2, "nome": "Meta", "descricao": "...", "pontos": 20, "criterio": "meta_atingida"},
    ]
    with (
        patch("app.conquistas.service.repository.listar_conquistas_ativas", return_value=conquistas),
        patch("app.conquistas.service.obter_criterios_cumpridos", return_value={"primeiro_consumo"}),
        patch("app.conquistas.service.repository.desbloquear_conquista", return_value=99) as desbloquear,
    ):
        resultado = service.verificar_conquistas(7)

    assert [item["id"] for item in resultado] == [1]
    desbloquear.assert_called_once_with(usuario_id=7, conquista_id=1)

def _conexao_falsa(rowcount_insert):
    cursor = MagicMock()
    cursor.fetchone.return_value = (10,)
    cursor.rowcount = rowcount_insert
    connection = MagicMock()
    connection.cursor.return_value = cursor
    return connection, cursor

def test_desbloqueio_soma_pontos_apenas_na_primeira_vez():
    connection, cursor = _conexao_falsa(1)
    cursor.lastrowid = 42
    with patch("app.conquistas.repository.get_connection", return_value=connection):
        resultado = repository.desbloquear_conquista(7, 3)

    assert resultado == 42
    assert any(
        "UPDATE usuarios SET pontos = pontos + %s" in chamada.args[0]
        for chamada in cursor.execute.call_args_list
    )
    connection.commit.assert_called_once()

def test_desbloqueio_repetido_nao_soma_pontos():
    connection, cursor = _conexao_falsa(0)
    with patch("app.conquistas.repository.get_connection", return_value=connection):
        resultado = repository.desbloquear_conquista(7, 3)

    assert resultado is None
    assert cursor.execute.call_count == 2
    connection.commit.assert_called_once()
    